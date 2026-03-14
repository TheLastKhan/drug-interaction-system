"""
Build normalized DrugBank vocabulary lookup tables for drug-name standardization.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from typing import Iterable

import pandas as pd


RAW_PATH = Path("data/raw/drugbank vocabulary.csv")
OUT_DIR = Path("data/processed")
VARIANTS_PATH = OUT_DIR / "drugbank_vocabulary_variants.csv"
CLEAN_PATH = OUT_DIR / "drugbank_vocabulary_clean.csv"
AMBIGUOUS_PATH = OUT_DIR / "drugbank_vocabulary_ambiguous_norms.csv"
SUMMARY_PATH = OUT_DIR / "drugbank_vocabulary_summary.json"

SOURCE_PRIORITY = {"common_name": 0, "synonym": 1}


def clean_text(value: object) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip()
    if text.lower() == "nan":
        return ""
    return text


def normalize_name(text: object) -> str:
    raw = clean_text(text)
    if not raw:
        return ""

    # Normalize accents so "Cetuximab" and "Cetuximab" with diacritics match.
    raw = unicodedata.normalize("NFKD", raw)
    raw = "".join(ch for ch in raw if not unicodedata.combining(ch))
    raw = raw.lower()
    raw = re.sub(r"[^a-z0-9]+", " ", raw)
    return " ".join(raw.split()).strip()


def split_pipe_values(value: object) -> list[str]:
    text = clean_text(value)
    if not text:
        return []
    return [part.strip() for part in text.split(" | ") if clean_text(part)]


def iter_variant_rows(df: pd.DataFrame) -> Iterable[dict[str, object]]:
    for _, row in df.iterrows():
        drugbank_id = clean_text(row["DrugBank ID"])
        common_name = clean_text(row["Common name"])
        accession_numbers = split_pipe_values(row["Accession Numbers"])
        seen_variants: set[str] = set()

        candidates = [(common_name, "common_name")]
        candidates.extend((synonym, "synonym") for synonym in split_pipe_values(row["Synonyms"]))

        for variant, variant_source in candidates:
            variant = clean_text(variant)
            if not variant:
                continue
            if variant in seen_variants:
                continue
            seen_variants.add(variant)

            name_norm = normalize_name(variant)
            if not name_norm:
                continue

            yield {
                "drugbank_id": drugbank_id,
                "common_name": common_name,
                "accession_numbers": " | ".join(accession_numbers),
                "name_variant": variant,
                "name_norm": name_norm,
                "variant_source": variant_source,
                "variant_source_rank": SOURCE_PRIORITY[variant_source],
            }


def build_variants() -> pd.DataFrame:
    df = pd.read_csv(RAW_PATH, low_memory=False)
    required = {
        "DrugBank ID",
        "Accession Numbers",
        "Common name",
        "Synonyms",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in DrugBank vocabulary file: {sorted(missing)}")

    variants_df = pd.DataFrame(iter_variant_rows(df))
    if variants_df.empty:
        raise ValueError("No vocabulary variants were generated.")

    variants_df = variants_df.drop_duplicates(
        subset=["drugbank_id", "name_variant", "name_norm"]
    ).reset_index(drop=True)
    return variants_df


def build_clean_lookup(variants_df: pd.DataFrame) -> pd.DataFrame:
    # Keep one canonical row per (drugbank_id, normalized_name), preferring common names.
    ordered = variants_df.sort_values(
        by=["drugbank_id", "name_norm", "variant_source_rank", "name_variant"],
        kind="stable",
    ).reset_index(drop=True)

    clean_df = ordered.drop_duplicates(subset=["drugbank_id", "name_norm"], keep="first")
    counts = (
        ordered.groupby(["drugbank_id", "name_norm"], as_index=False)
        .agg(
            variants_per_norm=("name_variant", "count"),
            variant_examples=("name_variant", lambda items: " | ".join(sorted(set(items))[:10])),
        )
    )
    clean_df = clean_df.merge(counts, on=["drugbank_id", "name_norm"], how="left")
    return clean_df


def build_ambiguous_lookup(clean_df: pd.DataFrame) -> pd.DataFrame:
    ambiguous = (
        clean_df.groupby("name_norm", as_index=False)
        .agg(
            drugbank_id_count=("drugbank_id", "nunique"),
            drugbank_ids=("drugbank_id", lambda items: " | ".join(sorted(set(items)))),
            common_names=("common_name", lambda items: " | ".join(sorted(set(items))[:10])),
        )
    )
    ambiguous = ambiguous[ambiguous["drugbank_id_count"] > 1].sort_values(
        by=["drugbank_id_count", "name_norm"], ascending=[False, True]
    )
    return ambiguous.reset_index(drop=True)


def write_summary(variants_df: pd.DataFrame, clean_df: pd.DataFrame, ambiguous_df: pd.DataFrame) -> None:
    summary = {
        "source_file": str(RAW_PATH),
        "variant_rows": int(len(variants_df)),
        "clean_rows": int(len(clean_df)),
        "unique_drugbank_ids": int(clean_df["drugbank_id"].nunique()),
        "unique_name_norm": int(clean_df["name_norm"].nunique()),
        "ambiguous_name_norm_rows": int(len(ambiguous_df)),
        "common_name_rows": int((variants_df["variant_source"] == "common_name").sum()),
        "synonym_rows": int((variants_df["variant_source"] == "synonym").sum()),
        "avg_variants_per_drug": round(float(variants_df.groupby("drugbank_id").size().mean()), 2),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    variants_df = build_variants()
    clean_df = build_clean_lookup(variants_df)
    ambiguous_df = build_ambiguous_lookup(clean_df)

    variants_df.to_csv(VARIANTS_PATH, index=False)
    clean_df.to_csv(CLEAN_PATH, index=False)
    ambiguous_df.to_csv(AMBIGUOUS_PATH, index=False)
    write_summary(variants_df, clean_df, ambiguous_df)

    print(f"Saved variants lookup: {VARIANTS_PATH}")
    print(f"Saved clean lookup: {CLEAN_PATH}")
    print(f"Saved ambiguous norms: {AMBIGUOUS_PATH}")
    print(f"Saved summary: {SUMMARY_PATH}")
    print(f"Variant rows: {len(variants_df):,}")
    print(f"Clean rows: {len(clean_df):,}")
    print(f"Unique DrugBank IDs: {clean_df['drugbank_id'].nunique():,}")
    print(f"Unique normalized names: {clean_df['name_norm'].nunique():,}")
    print(f"Ambiguous normalized names: {len(ambiguous_df):,}")


if __name__ == "__main__":
    main()
