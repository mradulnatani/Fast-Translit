from pydantic import BaseModel

class UserForm(BaseModel):
    pin_code: int
    state: str
    city: str
    locality: str
    landmark: str


class SubmissionResponse(BaseModel):
    id: int
    state_trans: str
    city_trans: str
    locality_trans: str
    landmark_trans: str


class NormalizedResponse(BaseModel):
    id: int
    state_normalized: str
    city_normalized: str
    locality_normalized: str
    landmark_normalized: str
    pin_code: int

