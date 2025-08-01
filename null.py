import ijson
from collections import defaultdict

null_counts = defaultdict(int)
total = 0

with open("outputs/austin_cleaned_merged.json", "rb") as f:
    parser = ijson.items(f, "item")
    for row in parser:
        total += 1
        for k, v in row.items():
            if v is None:
                null_counts[k] += 1

print(f"Total records: {total}")
for k, v in null_counts.items():
    print(f"{k}: {v} nulls ({(v / total):.2%})")
