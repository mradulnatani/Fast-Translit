from pydantic import BaseModel, EmailStr


class CompanyCreate(BaseModel):
    name: str
    email: EmailStr
    secret: str


class CompanyResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

