import requests
import json
import os
import re
from datetime import datetime

# Constants
ENDPOINT = "https://data.austintexas.gov/resource/3syk-w9eu.json"
LIMIT = 40000

OUTPUT_DIR = "outputs"
LOG_DIR = "logs"

def safe_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return None

def parse_date(val):
    return val.split("T")[0] if val and isinstance(val, str) and "T" in val else val

# --- Validation logic ---
def validate_row(record):
    errors = []

    permit_number = record.get("permit", {}).get("number")
    if not permit_number:
        errors.append("Missing permit_id")

    return errors

# --- Record transformation ---
def transform_record(raw):
    return {
        "permit": {
            "number": raw.get("permit_number"),
            "type": raw.get("permit type"),
            "type_desc": raw.get("permit_type_desc"),
            "class_mapped": raw.get("permit_class_mapped"),
            "class": raw.get("permit_class"),
            "work_class": raw.get("work_class"),
            "condominium": raw.get("condominium"),
            "master_number": raw.get("master permit number"),
            "link": raw.get("link"),
            "certificate_of_occupancy": raw.get("certificate_of_occupancy"),
            "issue_method": raw.get("issue_method")
        },
        "project": {
            "name": raw.get("permit_location"),
            "description": raw.get("description"),
            "tcad_id": raw.get("tcad_id"),
            "legal_description": raw.get("legal_description")
        },
        "dates": {
            "applied": parse_date(raw.get("applieddate")),
            "issued": parse_date(raw.get("issue_date")),
            "day_issued": raw.get("day_issued"),
            "calendar_year": raw.get("calendar_year_issued"),
            "fiscal_year": raw.get("fiscal_year_issued"),
            "status": parse_date(raw.get("status date")),
            "completed": parse_date(raw.get("completed_date")),
            "expires": parse_date(raw.get("expiresdate"))
        },
        "status": {
            "current": raw.get("status_current")
        },
        "flags": {
            "issued_last_30": raw.get("issued_in_last_30_days")
        },
        "area": {
            "existing": safe_float(raw.get("total_existing_building_sqft")),
            "remodel": safe_float(raw.get("remodel_repair_sqft")),
            "addition": safe_float(raw.get("total_new_add_sqft")),
            "lot": safe_float(raw.get("total_lot_sq_ft"))
        },
        "building": {
            "num_floors": safe_float(raw.get("number_of_floors")),
            "housing_units": safe_float(raw.get("housing_units"))
        },
        "valuation": {
            "total_job": safe_float(raw.get("total_job_valuation")),
            "remodel_total": safe_float(raw.get("total_valuation_remodel")),
            "building": safe_float(raw.get("building_valuation")),
            "building_remodel": safe_float(raw.get("building_valuation_remodel")),
            "electrical": safe_float(raw.get("electrical_valuation")),
            "electrical_remodel": safe_float(raw.get("electrical_valuation_remodel")),
            "mechanical": safe_float(raw.get("mechanical_valuation")),
            "mechanical_remodel": safe_float(raw.get("mechanical_valuation_remodel")),
            "plumbing": safe_float(raw.get("plumbing_valuation")),
            "plumbing_remodel": safe_float(raw.get("plumbing_valuation_remodel")),
            "medgas": safe_float(raw.get("medgas_valuation")),
            "medgas_remodel": safe_float(raw.get("medgas_valuation_remodel"))
        },
        "coordinates": {
            "latitude": safe_float(raw.get("latitude")),
            "longitude": safe_float(raw.get("longitude"))
        },
        "location": {
            "council_district": raw.get("council_district"),
            "jurisdiction": raw.get("jurisdiction"),
            "description": raw.get("location"),
            "geo": None,
            "original": {
                "street_address": raw.get("original_address1"),
                "city": raw.get("original_city"),
                "state": raw.get("original_state") or "TX",
                "zip": str(raw.get("original_zip")) if raw.get("original_zip") else None
            }
        },
        "contractor": {
            "trade": raw.get("contractor_trade"),
            "company_name": raw.get("contractor_company_name"),
            "name": raw.get("contractor_full_name"),
            "phone": raw.get("contractor_phone"),
            "address": {
                "street": raw.get("contractor_address1"),
                "unit": raw.get("contractor_address2"),
                "city": raw.get("contractor_city"),
                "zip": raw.get("contractor_zip")
            }
        },
        "applicant": {
            "full_name": raw.get("applicant_full_name"),
            "organization": raw.get("applicant_org"),
            "phone": raw.get("applicant_phone"),
            "address": {
                "street": raw.get("applicant_address1"),
                "unit": raw.get("applicant_address2"),
                "city": raw.get("applicant_city"),
                "zip": raw.get("applicantzip")
            }
        }
    }

def run_batches():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    offset = 0
    total_clean = 0
    total_anomalies = 0

    while True:
        print(f"Fetching batch {offset} to {offset + LIMIT}")
        resp = requests.get(
            ENDPOINT,
            params={"$limit": LIMIT, "$offset": offset},
            headers={"Accept": "application/json"}
        )
        if resp.status_code != 200:
            print(f"Error {resp.status_code}: {resp.text}")
            break
        try:
            data = resp.json()
        except Exception as e:
            print(f"JSON Decode Error: {e}")
            break
        if not data:
            print("No more data.")
            break

        clean_path = f"{OUTPUT_DIR}/clean_batch_{offset}.jsonl"
        log_path = f"{LOG_DIR}/anomalies_batch_{offset}.jsonl"
        with open(clean_path, "w") as clean_f, open(log_path, "w") as log_f:
            for idx, raw in enumerate(data):
                record = transform_record(raw)
                errors = validate_row(record)
                if errors:
                    log_f.write(json.dumps({"row": offset+idx, "errors": errors, "data": record}) + "\n")
                    total_anomalies += 1
                else:
                    clean_f.write(json.dumps(record) + "\n")
                    total_clean += 1
        offset += LIMIT

    print(f"✅ Done. Clean: {total_clean}, Anomalies: {total_anomalies}")

run_batches()
