from Backend.schemas import CompanyCreate, CompanyResponse
from sqlalchemy.exc import IntegrityError

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from Backend.db import get_db
from Backend.models import Company, JWTToken
from Backend.auth.security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/token")
def issue_token(email: str, secret: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.email == email).first()

    if not company or not pwd_context.verify(secret, company.hashed_secret):
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
def signup_company(data: CompanyCreate, db: Session = Depends(get_db)):
    existing = db.query(Company).filter(Company.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company already registered")

    hashed_secret = pwd_context.hash(data.secret)

    company = Company(
        name=data.name,
        email=data.email,
        hashed_secret=hashed_secret
    )

    db.add(company)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Registration failed")

    db.refresh(company)
    return company

