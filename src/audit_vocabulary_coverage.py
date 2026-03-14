"""
Audit DrugBank vocabulary coverage against Kaggle DDI and TWOSIDES drug names.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import pandas as pd


VOCAB_PATH = Path("data/processed/drugbank_vocabulary_clean.csv")
OVERRIDES_PATH = Path("config/vocabulary_overrides.json")
OUT_DIR = Path("data/processed")
SUMMARY_PATH = OUT_DIR / "vocabulary_coverage_summary.json"
KAGGLE_UNMATCHED_PATH = OUT_DIR / "vocabulary_kaggle_unmatched.csv"
TWOSIDES_UNMATCHED_PATH = OUT_DIR / "vocabulary_twosides_unmatched.csv"

KAGGLE_PATH = Path("data/raw/db_drug_interactions.csv")
TWOSIDES_GZ_PATH = Path("data/raw/TWOSIDES.csv.gz")
TWOSIDES_CSV_PATH = Path("data/raw/TWOSIDES.csv")


def normalize_name(text: object) -> str:
    if pd.isna(text):
        return ""
    text = str(text).strip()
    if not text or text.lower() == "nan":
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split()).strip()


def load_vocab_norms() -> set[str]:
    if not VOCAB_PATH.exists():
        raise FileNotFoundError(
            f"Vocabulary file not found: {VOCAB_PATH}. Run src/build_vocabulary.py first."
        )
    vocab = pd.read_csv(VOCAB_PATH, usecols=["name_norm"])
    return set(vocab["name_norm"].dropna().astype(str))


def load_overrides() -> dict[str, str]:
    if not OVERRIDES_PATH.exists():
        return {}
    data = json.loads(OVERRIDES_PATH.read_text(encoding="utf-8"))
    return {str(key): normalize_name(value) for key, value in data.items() if normalize_name(value)}


def audit_kaggle(vocab_norms: set[str], overrides: dict[str, str]) -> tuple[dict[str, object], pd.DataFrame]:
    kaggle = pd.read_csv(KAGGLE_PATH, usecols=["Drug 1", "Drug 2"], low_memory=False)
    names = pd.concat([kaggle["Drug 1"], kaggle["Drug 2"]], ignore_index=True).dropna().astype(str)
    unique_names = pd.DataFrame({"source_name": sorted(set(name.strip() for name in names if name.strip()))})
    unique_names["name_norm"] = unique_names["source_name"].map(normalize_name)
    unique_names["override_norm"] = unique_names["source_name"].map(lambda name: overrides.get(name, ""))
    unique_names["matched"] = unique_names["name_norm"].isin(vocab_norms) | unique_names["override_norm"].isin(vocab_norms)
    unique_names["matched_via"] = "unmatched"
    unique_names.loc[unique_names["name_norm"].isin(vocab_norms), "matched_via"] = "direct"
    unique_names.loc[
        (~unique_names["name_norm"].isin(vocab_norms)) & unique_names["override_norm"].isin(vocab_norms),
        "matched_via",
    ] = "override"
    unmatched = unique_names[~unique_names["matched"]].reset_index(drop=True)

    summary = {
        "unique_names": int(len(unique_names)),
        "matched_names": int(unique_names["matched"].sum()),
        "unmatched_names": int((~unique_names["matched"]).sum()),
        "match_rate": round(float(unique_names["matched"].mean()), 4),
        "override_matches": int((unique_names["matched_via"] == "override").sum()),
    }
    return summary, unmatched


def audit_twosides(vocab_norms: set[str], overrides: dict[str, str]) -> tuple[dict[str, object], pd.DataFrame]:
    twosides_path = TWOSIDES_GZ_PATH if TWOSIDES_GZ_PATH.exists() else TWOSIDES_CSV_PATH
    if not twosides_path.exists():
        raise FileNotFoundError("No TWOSIDES source file found in data/raw.")

    unique_names: set[str] = set()
    read_kwargs = {"low_memory": False, "chunksize": 250000}
    if twosides_path.suffix == ".gz":
        read_kwargs["compression"] = "gzip"

    for chunk in pd.read_csv(
        twosides_path,
        usecols=["drug_1_concept_name", "drug_2_concept_name"],
        **read_kwargs,
    ):
        for col in ("drug_1_concept_name", "drug_2_concept_name"):
            values = chunk[col].dropna().astype(str)
            unique_names.update(name.strip() for name in values if name.strip())

    unique_df = pd.DataFrame({"source_name": sorted(unique_names)})
    unique_df["name_norm"] = unique_df["source_name"].map(normalize_name)
    unique_df["override_norm"] = unique_df["source_name"].map(lambda name: overrides.get(name, ""))
    unique_df["matched"] = unique_df["name_norm"].isin(vocab_norms) | unique_df["override_norm"].isin(vocab_norms)
    unique_df["matched_via"] = "unmatched"
    unique_df.loc[unique_df["name_norm"].isin(vocab_norms), "matched_via"] = "direct"
    unique_df.loc[
        (~unique_df["name_norm"].isin(vocab_norms)) & unique_df["override_norm"].isin(vocab_norms),
        "matched_via",
    ] = "override"
    unmatched = unique_df[~unique_df["matched"]].reset_index(drop=True)

    summary = {
        "unique_names": int(len(unique_df)),
        "matched_names": int(unique_df["matched"].sum()),
        "unmatched_names": int((~unique_df["matched"]).sum()),
        "match_rate": round(float(unique_df["matched"].mean()), 4),
        "override_matches": int((unique_df["matched_via"] == "override").sum()),
    }
    return summary, unmatched


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    vocab_norms = load_vocab_norms()
    overrides = load_overrides()
    kaggle_summary, kaggle_unmatched = audit_kaggle(vocab_norms, overrides)
    twosides_summary, twosides_unmatched = audit_twosides(vocab_norms, overrides)

    kaggle_unmatched.to_csv(KAGGLE_UNMATCHED_PATH, index=False)
    twosides_unmatched.to_csv(TWOSIDES_UNMATCHED_PATH, index=False)

    summary = {
        "vocabulary_unique_norms": len(vocab_norms),
        "override_entries": len(overrides),
        "kaggle": kaggle_summary,
        "twosides": twosides_summary,
        "outputs": {
            "kaggle_unmatched": str(KAGGLE_UNMATCHED_PATH),
            "twosides_unmatched": str(TWOSIDES_UNMATCHED_PATH),
        },
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
