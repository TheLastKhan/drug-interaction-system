"""
TWOSIDES Dataset - Analysis
Reads gzipped CSV and produces summary statistics
"""
import pandas as pd
import json
import os

DATA_PATH = os.path.join("data", "raw", "TWOSIDES.csv.gz")
OUTPUT_PATH = os.path.join("data", "processed", "twosides_stats.json")

print("Loading TWOSIDES dataset (first 500K rows)...")
# Read with all columns as string first to avoid type issues
df = pd.read_csv(DATA_PATH, compression='gzip', nrows=500000, low_memory=False)

print(f"Loaded {len(df):,} rows")
print(f"Columns: {list(df.columns)}")
print(f"Dtypes:")
for col in df.columns:
    print(f"  {col}: {df[col].dtype}")

stats = {}
stats['columns'] = list(df.columns)
stats['sample_rows_loaded'] = len(df)
stats['dtypes'] = {col: str(dtype) for col, dtype in df.dtypes.items()}
stats['null_counts'] = {col: int(df[col].isnull().sum()) for col in df.columns}

# Find drug name columns dynamically
drug1_col = None
drug2_col = None
condition_col = None
for col in df.columns:
    col_lower = col.lower()
    if 'drug_1' in col_lower and 'concept' in col_lower:
        drug1_col = col
    elif 'drug_2' in col_lower and 'concept' in col_lower:
        drug2_col = col
    elif 'condition' in col_lower and 'concept' in col_lower:
        condition_col = col

if drug1_col and drug2_col:
    stats['drug1_column'] = drug1_col
    stats['drug2_column'] = drug2_col
    stats['unique_drug1'] = int(df[drug1_col].nunique())
    stats['unique_drug2'] = int(df[drug2_col].nunique())
    all_drugs = set(df[drug1_col].dropna().unique()) | set(df[drug2_col].dropna().unique())
    stats['total_unique_drugs'] = len(all_drugs)
    stats['top10_drug1'] = {str(k): int(v) for k, v in df[drug1_col].value_counts().head(10).items()}

if condition_col:
    stats['condition_column'] = condition_col
    stats['unique_conditions'] = int(df[condition_col].nunique())
    stats['top10_conditions'] = {str(k): int(v) for k, v in df[condition_col].value_counts().head(10).items()}

# PRR stats - convert to numeric first
if 'PRR' in df.columns:
    prr = pd.to_numeric(df['PRR'], errors='coerce').dropna()
    stats['prr_stats'] = {
        'count': int(len(prr)),
        'mean': round(float(prr.mean()), 2),
        'median': round(float(prr.median()), 2),
        'min': round(float(prr.min()), 4),
        'max': round(float(prr.max()), 2),
        'std': round(float(prr.std()), 2),
    }

# Sample rows (convert all values to str for JSON serialization)
sample = df.head(3).copy()
for col in sample.columns:
    sample[col] = sample[col].astype(str)
stats['sample_data'] = sample.to_dict(orient='records')

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)

print(f"\nAnalysis saved to {OUTPUT_PATH}")
print(f"Unique drugs (in 500K sample): {stats.get('total_unique_drugs', 'N/A')}")
print(f"Unique conditions: {stats.get('unique_conditions', 'N/A')}")
if 'prr_stats' in stats:
    print(f"PRR - mean: {stats['prr_stats']['mean']}, median: {stats['prr_stats']['median']}, max: {stats['prr_stats']['max']}")
