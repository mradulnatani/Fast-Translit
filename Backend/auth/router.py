from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from Backend.db import get_db
from Backend.models import Company, TargetApi, JWTToken
from Backend.schema import CreateUser, CompanyResponse
from Backend.auth.security import create_access_token
router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
def company_login(name: str,secret: str,email: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.email == email).first()
    if not company or not pwd_context.verify(secret, company.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token, jti, exp = create_access_token(company.id)

    db.add(
        JWTToken(
            company_id=company.id,
            jti=jti,
            expires_at=exp
        )
    )
    db.commit()

    return {
        "access_token": token,
        "token_type": "bearer"
    }



@router.post("/signup", response_model=CompanyResponse)
def company_signup(data: CreateUser, db: Session = Depends(get_db)):
    existing = db.query(Company).filter(Company.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Company is already registered"
        )

    hashed_password = pwd_context.hash(data.password)

    company = Company(
        name=data.name,
        email=data.email,
        hashed_password=hashed_password,
    )

    target_api = TargetApi(
        target_api_url=data.target_api_url,
        transliteration_fields=data.fields,
        endpoint_key=data.endpoint_key
    )

    company.target_apis.append(target_api)

    db.add(company)
    db.commit()
    db.refresh(company)

    return company

