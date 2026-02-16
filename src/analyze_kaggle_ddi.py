"""
Print analysis report in smaller chunks to avoid terminal truncation
"""
import pandas as pd
import os
import json

DATA_PATH = os.path.join("data", "raw", "db_drug_interactions.csv")
df = pd.read_csv(DATA_PATH)

# Save summary stats as JSON for easy reading
stats = {}
stats['total_interactions'] = len(df)
stats['columns'] = list(df.columns)
stats['unique_drug1'] = int(df['Drug 1'].nunique())
stats['unique_drug2'] = int(df['Drug 2'].nunique())
all_drugs = set(df['Drug 1'].unique()) | set(df['Drug 2'].unique())
stats['total_unique_drugs'] = len(all_drugs)
stats['null_values'] = {col: int(df[col].isnull().sum()) for col in df.columns}

# Duplicate check
dupes = int(df.duplicated().sum())
df_sorted = df.copy()
df_sorted['pair'] = df_sorted.apply(
    lambda r: tuple(sorted([r['Drug 1'], r['Drug 2']])), axis=1
)
bidir_dupes = int(df_sorted['pair'].duplicated().sum())
unique_pairs = int(df_sorted['pair'].nunique())
stats['exact_duplicates'] = dupes
stats['bidirectional_duplicates'] = bidir_dupes
stats['unique_drug_pairs'] = unique_pairs

# Top drugs
stats['top20_drug1'] = {k: int(v) for k, v in df['Drug 1'].value_counts().head(20).items()}
stats['top20_drug2'] = {k: int(v) for k, v in df['Drug 2'].value_counts().head(20).items()}

# Keyword analysis
desc = df['Interaction Description'].str.lower()
keyword_map = {
    'increase': 'increase',
    'decrease': 'decrease',
    'risk': 'risk',
    'toxic': 'toxic',
    'adverse': 'adverse',
    'serum_concentration': 'serum concentration',
    'therapeutic_efficacy': 'therapeutic efficacy',
    'metabolism': 'metabolism',
    'qtc_prolongation': 'qtc',
    'serotonin': 'serotonin',
    'bleeding': 'bleeding',
    'hypotension': 'hypotension',
    'contraindicated': 'contraindicated',
    'avoid': 'avoid',
}
stats['keyword_counts'] = {}
for label, keyword in keyword_map.items():
    count = int(desc.str.contains(keyword).sum())
    stats['keyword_counts'][label] = {
        'count': count,
        'percentage': round(count / len(df) * 100, 1)
    }

# Description length stats
lengths = df['Interaction Description'].str.len()
stats['desc_length'] = {
    'mean': round(float(lengths.mean()), 0),
    'min': int(lengths.min()),
    'max': int(lengths.max()),
    'median': round(float(lengths.median()), 0),
}

# Sample interactions
stats['sample_interactions'] = []
for i, row in df.head(10).iterrows():
    stats['sample_interactions'].append({
        'drug1': row['Drug 1'],
        'drug2': row['Drug 2'],
        'description': row['Interaction Description']
    })

# Save as JSON
output_path = os.path.join("data", "processed", "kaggle_ddi_stats.json")
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)

print(f"Analysis saved to {output_path}")
print(f"Total interactions: {stats['total_interactions']:,}")
print(f"Total unique drugs: {stats['total_unique_drugs']:,}")
print(f"Unique drug pairs: {stats['unique_drug_pairs']:,}")
print(f"Exact duplicates: {stats['exact_duplicates']}")
print(f"Bidirectional duplicates: {stats['bidirectional_duplicates']}")
