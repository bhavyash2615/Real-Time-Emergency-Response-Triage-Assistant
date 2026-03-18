from fastapi import FastAPI
from app.api.triage_routes import router
# from api.triage import router as triage_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Emergency Triage Assistant",
    description="Real-time emergency response triage system",
    version="1.0"
)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)