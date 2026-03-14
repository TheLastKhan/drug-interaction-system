"""
Generate manual-review suggestions for unmatched TWOSIDES drug names.
"""
from __future__ import annotations

import difflib
from pathlib import Path

import pandas as pd


UNMATCHED_PATH = Path("data/processed/vocabulary_twosides_unmatched.csv")
VOCAB_PATH = Path("data/processed/drugbank_vocabulary_clean.csv")
OUT_PATH = Path("data/processed/vocabulary_twosides_unmatched_suggestions.csv")


def top_matches(value: str, pool: list[str], n: int = 3, cutoff: float = 0.75) -> str:
    matches = difflib.get_close_matches(value, pool, n=n, cutoff=cutoff)
    return " | ".join(matches)


def main() -> None:
    unmatched = pd.read_csv(UNMATCHED_PATH)
    vocab = pd.read_csv(VOCAB_PATH, usecols=["common_name", "name_norm"])

    name_norms = sorted(set(vocab["name_norm"].dropna().astype(str)))
    common_names = sorted(set(vocab["common_name"].dropna().astype(str)))

    rows = []
    for _, row in unmatched.iterrows():
        rows.append(
            {
                "source_name": row["source_name"],
                "name_norm": row["name_norm"],
                "norm_suggestions": top_matches(str(row["name_norm"]), name_norms),
                "common_name_suggestions": top_matches(str(row["source_name"]), common_names),
            }
        )

    suggestions = pd.DataFrame(rows)
    suggestions.to_csv(OUT_PATH, index=False)
    print(f"Saved suggestions: {OUT_PATH}")
    print(f"Rows: {len(suggestions):,}")


if __name__ == "__main__":
    main()
