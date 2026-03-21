from database.patient_db import PatientDatabase


class HistoryRetriever:

    def __init__(self):
        self.db = PatientDatabase()

    def get_all_patient_ids(self):
        return self.db.get_all_patient_ids()

    def get_patient_history(self, patient_id):
        """
        Retrieve patient history from patient database
        """

        patient = self.db.get_patient(patient_id)

        if patient is None:
            return None

        history = {
            "patient_id": patient["patient_id"],
            "age": patient.get("anchor_age"),
            "gender": patient.get("gender"),
            "diagnoses": patient.get("diagnoses", []),
            "medications": patient.get("medications", []),
            "procedures": patient.get("procedures", []),
            "labs": patient.get("labs", []),
            "admissions": patient.get("admissions", [])
        }

        return history
