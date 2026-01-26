from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from Backend.db import get_db
from Backend.models import Company, JWTToken
from Backend.auth.security import SECRET_KEY, ALGORITHM

security = HTTPBearer()


def get_current_company(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Company:
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        company_id: str = payload.get("sub")
        jti: str = payload.get("jti")

        if company_id is None or jti is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    token_entry = (
        db.query(JWTToken)
        .filter(JWTToken.jti == jti, JWTToken.is_revoked == False)
        .first()
    )

    if not token_entry:
        raise HTTPException(status_code=401, detail="Token revoked")

    company = db.query(Company).filter(Company.id == int(company_id)).first()

    if not company or not company.is_active:
        raise HTTPException(status_code=401, detail="Inactive company")

    return company

