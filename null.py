from collections import defaultdict
import json

null_counts = defaultdict(int)
total = 0

with open("outputs/austin_cleaned_merged.json") as f:
    data = json.load(f)
    total = len(data)
    for row in data:
        for top_level_key in row:
            if row[top_level_key] is None:
                null_counts[top_level_key] += 1

print(f"Total records: {total}")
for k, v in null_counts.items():
    print(f"{k}: {v} nulls ({(v / total):.2%})")
