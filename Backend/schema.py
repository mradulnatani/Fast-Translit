from pydantic import BaseModel,EmailStr
from typing import List

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str
    target_api_url: str
    fields: List[str]
    endpoint_key: str


class CompanyResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True
