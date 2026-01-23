from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from Backend.db import get_db
from Backend.models import Company, JWTToken
from Backend.auth.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_company(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        company_id: str = payload.get("sub")
        jti: str = payload.get("jti")

        if not company_id or not jti:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    token_db = db.query(JWTToken).filter(
        JWTToken.jti == jti,
        JWTToken.is_revoked == False
    ).first()

    if not token_db:
        raise HTTPException(status_code=401, detail="Token revoked")

    company = db.query(Company).filter(Company.id == int(company_id)).first()

    if not company or not company.is_active:
        raise HTTPException(status_code=403, detail="Inactive company")

    return company

