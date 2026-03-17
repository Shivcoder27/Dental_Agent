from pydantic import BaseModel


class PatientCreate(BaseModel):
    name: str
    phone: str
    age: int
    gender: str


class PatientResponse(BaseModel):
    id: int
    name: str
    phone: str
    age: int
    gender: str

    class Config:
        orm_mode = True