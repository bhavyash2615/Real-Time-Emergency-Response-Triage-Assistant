import pandas as pd
import os

from database.patient_db import PatientDatabase

DATA_PATH = "data/patients"


def ingest_mimic():

    print("Loading MIMIC data...")

    patients = pd.read_csv(os.path.join(DATA_PATH, "patients.csv"))
    admissions = pd.read_csv(os.path.join(DATA_PATH, "admissions.csv"))
    diagnoses = pd.read_csv(os.path.join(DATA_PATH, "diagnoses_icd.csv"))
    prescriptions = pd.read_csv(os.path.join(DATA_PATH, "prescriptions.csv"))
    procedures = pd.read_csv(os.path.join(DATA_PATH, "procedures_icd.csv"))
    labevents = pd.read_csv(os.path.join(DATA_PATH, "labevents.csv"))

    # NEW: dictionary tables
    d_icd_diagnoses = pd.read_csv(os.path.join(DATA_PATH, "d_icd_diagnoses.csv"))
    d_icd_procedures = pd.read_csv(os.path.join(DATA_PATH, "d_icd_procedures.csv"))
    d_labitems = pd.read_csv(os.path.join(DATA_PATH, "d_labitems.csv"))

    # -------------------------
    # Build lookup dictionaries
    # -------------------------

    diagnosis_map = dict(zip(
        d_icd_diagnoses["icd_code"],
        d_icd_diagnoses["long_title"]
    ))

    procedure_map = dict(zip(
        d_icd_procedures["icd_code"],
        d_icd_procedures["long_title"]
    ))

    lab_map = dict(zip(
        d_labitems["itemid"],
        d_labitems["label"]
    ))

    db = PatientDatabase()

    patient_records = {}

    # -------------------------
    # Base patient info
    # -------------------------
    for _, row in patients.iterrows():

        pid = row["subject_id"]

        patient_records[pid] = {
            "patient_id": pid,
            "gender": row["gender"],
            "anchor_age": row["anchor_age"],
            "diagnoses": [],
            "medications": [],
            "procedures": [],
            "labs": [],
            "admissions": []
        }

    # -------------------------
    # Admissions
    # -------------------------
    for _, row in admissions.iterrows():

        pid = row["subject_id"]

        if pid in patient_records:
            patient_records[pid]["admissions"].append({
                "admission_type": row["admission_type"],
                "admit_time": str(row["admittime"])
            })

    # -------------------------
    # Diagnoses (CODE → TEXT)
    # -------------------------
    for _, row in diagnoses.iterrows():

        pid = row["subject_id"]
        code = row["icd_code"]

        if pid in patient_records:

            diagnosis_text = diagnosis_map.get(code, code)

            patient_records[pid]["diagnoses"].append(diagnosis_text)

    # -------------------------
    # Medications
    # -------------------------
    for _, row in prescriptions.iterrows():

        pid = row["subject_id"]

        if pid in patient_records:

            drug = row["drug"]

            if isinstance(drug, str):
                patient_records[pid]["medications"].append(drug)

    # -------------------------
    # Procedures (CODE → TEXT)
    # -------------------------
    for _, row in procedures.iterrows():

        pid = row["subject_id"]
        code = row["icd_code"]

        if pid in patient_records:

            procedure_text = procedure_map.get(code, code)

            patient_records[pid]["procedures"].append({
                "procedure": procedure_text,
                "procedure_date": str(row["chartdate"]) if "chartdate" in row else None
            })

    # -------------------------
    # Lab events (ITEMID → LAB NAME)
    # -------------------------
    for _, row in labevents.iterrows():

        pid = row["subject_id"]

        if pid in patient_records:

            itemid = row["itemid"]
            value = row["valuenum"]

            lab_name = lab_map.get(itemid, str(itemid))

            patient_records[pid]["labs"].append({
                "lab_test": lab_name,
                "value": value,
                "time": str(row["charttime"]) if "charttime" in row else None
            })

    # -------------------------
    # Save to patient DB
    # -------------------------
    for pid, record in patient_records.items():
        db.insert_patient(record)

    print("MIMIC ingestion completed")


if __name__ == "__main__":
    ingest_mimic()
