import sqlite3
import json
import os

DB_PATH = "database/patients.db"


class PatientDatabase:

    def __init__(self):
        os.makedirs("database", exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            data TEXT
        )
        """)

        self.conn.commit()

    # -----------------------------
    # Insert patient
    # -----------------------------
    def insert_patient(self, patient_record):

        cursor = self.conn.cursor()

        patient_id = str(patient_record["patient_id"])

        data_json = json.dumps(patient_record)

        cursor.execute("""
        INSERT OR REPLACE INTO patients (patient_id, data)
        VALUES (?, ?)
        """, (patient_id, data_json))

        self.conn.commit()

    # -----------------------------
    # Retrieve patient
    # -----------------------------
    def get_patient(self, patient_id):

        cursor = self.conn.cursor()

        cursor.execute("""
        SELECT data FROM patients WHERE patient_id = ?
        """, (str(patient_id),))

        row = cursor.fetchone()

        if row:
            return json.loads(row[0])

        return None

    # -----------------------------
    # Close connection
    # -----------------------------
    def close(self):
        self.conn.close()
