from fastapi import APIRouter
from pydantic import BaseModel

from app.services.triage_service import TriageService


router = APIRouter()

triage_service = TriageService()


# -------------------------
# Request schema
# -------------------------
class TriageRequest(BaseModel):
    patient_id: str
    current_issue: str


# -------------------------
# Triage API endpoint
# -------------------------
@router.post("/triage")
def run_triage(request: TriageRequest):

    result = triage_service.run_triage(
        patient_id=request.patient_id,
        current_issue=request.current_issue
    )

    return result

@router.get("/patients")
def get_patients():
    return triage_service.get_all_patient_ids()
