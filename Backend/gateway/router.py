from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backend.db import SessionLocal
from Backend.auth.dependencies import get_current_company
from Backend.models import APIEndpoint
from Backend.gateway.service import process_request

router = APIRouter(prefix="/gateway", tags=["Gateway"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{endpoint_key}")
def gateway_handler(
    endpoint_key: str,
    payload: dict,
    company=Depends(get_current_company),
    db: Session = Depends(get_db)
):
    api = db.query(ApiEndpoint).filter(
        APIEndpoint.endpoint_key == endpoint_key,
        APIEndpoint.company_id == company.id
    ).first()

    if not api:
        raise HTTPException(status_code=404, detail="Invalid endpoint")

    return process_request(db, company, api, payload)

