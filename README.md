# Austin Permit Data - Staging Pipeline

## 🎯 Objective

Prepare a cleaned and schema-aligned staging file (`austin_cleaned.json`) for the City of Austin building permits dataset, which plugs directly into the ConstructIQ normalization engine owned by Umar.

---

## 📁 Output

- `austin_cleaned.json`: Cleaned JSON array of ~2.3M permit records, validated against the `PermitRecord` Pydantic model (`models.py`).
- `models.py`: Contains all nested Pydantic classes and type constraints used to validate each record.
- `load_austin.py`: Main ETL script that fetches, transforms, validates, and stores the data.

---

## 🧰 Tooling

| Tool       | Purpose                          |
|------------|----------------------------------|
| Python     | Scripting language               |
| Pydantic   | Schema validation (`models.py`)  |
| requests   | API calls to Socrata endpoint    |
| JSONL/JSON | Intermediate + final output formats |
| GitHub Codespaces / Colab | Development environments |

---

## 🧪 Transformations & Assumptions

- All date fields are normalized to `YYYY-MM-DD` using simple split logic.
- All numeric fields (e.g., area, valuation) are parsed using `safe_float()`.
- Empty strings, invalid floats, and missing fields are converted to `None`.
- Boolean fields default to `False` only when clearly appropriate.
- Default `state` is `TX` when missing.
- Coordinates and complex addresses are nested appropriately.
- Validation skips records missing `permit.number` or with clearly malformed data.

---

## 📊 Summary

- Total records processed: **2,315,095**
- Total records written: **2,315,095**
- Anomalies dropped: **0** (due to strict filtering on `permit.number`)
- Output file size: **~4GB**

---

## 🔁 Pipeline Flow

1. Fetch raw records from Socrata API (`3syk-w9eu.json`)
2. Chunk into batches (40,000 per request)
3. Transform each record into nested structure
4. Validate with `PermitRecord` model
5. Write clean records to `.jsonl` files
6. Merge `.jsonl` files into final `austin_cleaned.json`

---

## ✅ Next Steps

- Pass cleaned file into ConstructIQ normalization engine
- Finalize Sprint 2 goals (possibly deduping, enrichments, or joining with additional datasets)

