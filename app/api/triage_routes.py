from fastapi import APIRouter
from pydantic import BaseModel

from app.services.triage_service import TriageService


router = APIRouter()

triage_service = None

def get_triage_service():
    global triage_service
    if triage_service is None:
        triage_service = TriageService()
    return triage_service


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

    service = get_triage_service()

    result = service.run_triage(
        patient_id=request.patient_id,
        current_issue=request.current_issue
    )

    return result

@router.get("/patients")
def get_patients():
    service = get_triage_service()
    return service.get_all_patient_ids()


