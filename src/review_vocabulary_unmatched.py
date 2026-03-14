"""
Classify unmatched TWOSIDES names into review buckets so we only override safe cases.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd


UNMATCHED_PATH = Path("data/processed/vocabulary_twosides_unmatched.csv")
SUGGESTIONS_PATH = Path("data/processed/vocabulary_twosides_unmatched_suggestions.csv")
OUT_CSV = Path("data/processed/vocabulary_twosides_unmatched_review.csv")
OUT_JSON = Path("data/processed/vocabulary_twosides_unmatched_review_summary.json")


def classify_name(source_name: str) -> tuple[str, str]:
    lower = source_name.lower()

    if lower in {"drug_1_concept_name", "drug_2_concept_name"}:
        return "data_artifact", "exclude_from_pipeline"

    if re.search(r"vaccine|virus|strain|influenza|varicella|hepatitis", lower):
        return "vaccine_or_biologic", "manual_review"

    if re.search(r"immunoglobulin|immune globulin|globulin|insulin", lower):
        return "biologic_family", "manual_review"

    if re.search(
        r"juice|oil|leaf|grape|ginger|garlic|tea|wheat|rice|cranberry|orange|salmon|cinnamon|alfalfa",
        lower,
    ):
        return "food_or_herbal", "leave_unmatched"

    if re.search(r"usp|liposomal|liposome|human|pork|live attenuated|inactivated", lower):
        return "formulation_or_label_variant", "manual_review"

    if re.search(
        r"alkaloids|polyethylene|glycols|heparinoids|estrogens|fiber|collagen|amylases|lipase|lactobacillus|bismuth|sulfur|placebo",
        lower,
    ):
        return "broad_class_or_group", "leave_unmatched"

    if re.search(
        r"sodium|potassium|calcium|lithium|sulfate|phosphate|acetate|succinate|oxalate|bromide|thiosulfate|selenate|gluconate|fumarate",
        lower,
    ):
        return "salt_or_component_variant", "manual_review"

    return "possible_alias_or_missing_vocab", "manual_review"


def main() -> None:
    unmatched = pd.read_csv(UNMATCHED_PATH)
    suggestions = pd.read_csv(SUGGESTIONS_PATH)
    review = unmatched.merge(suggestions, on=["source_name", "name_norm"], how="left")

    categories: list[str] = []
    actions: list[str] = []
    for source_name in review["source_name"].astype(str):
        category, action = classify_name(source_name)
        categories.append(category)
        actions.append(action)

    review["review_category"] = categories
    review["recommended_action"] = actions
    review.to_csv(OUT_CSV, index=False)

    summary = {
        "rows": int(len(review)),
        "category_counts": review["review_category"].value_counts().to_dict(),
        "action_counts": review["recommended_action"].value_counts().to_dict(),
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"Saved review CSV: {OUT_CSV}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
