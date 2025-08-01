import glob
import json

def merge_jsonl_stream(folder, pattern, output_file):
    files = sorted(glob.glob(f"{folder}/{pattern}"))
    print(f"📦 Merging {len(files)} files from '{folder}'...")

    with open(output_file, "w", encoding="utf-8") as out:
        out.write("[\n")
        first = True
        for file in files:
            print(f"🔄 Reading: {file}")
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    if not first:
                        out.write(",\n")
                    out.write(line.strip())
                    first = False
        out.write("\n]\n")

    print(f"✅ Done. Merged output saved to: {output_file}")

merge_jsonl_stream("outputs", "clean_batch_*.jsonl", "outputs/austin_cleaned_merged.json")
