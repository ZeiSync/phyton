from typing import List
import datetime as _dt
from unicodedata import decimal
import pydantic as _pydantic


class _PatientBase(_pydantic.BaseModel):
    first_name: str
    last_name: str
    age: int
    temp: float


class PatientCreate(_PatientBase):
    pass


class Patient(_PatientBase):
    id: int
    owner_id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        orm_mode = True


class _UserBase(_pydantic.BaseModel):
    email: str


class UserCreate(_UserBase):
    password: str


class User(_UserBase):
    id: int
    is_active: bool
    patients: List[Patient] = []

    class Config:
        orm_mode = True