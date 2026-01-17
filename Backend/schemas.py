from pydantic import BaseModel

class UserForm(BaseModel):
    name: str
    address: str


class SubmissionResponse(BaseModel):
    id: int
    name_trans: str
    address_trans: str
