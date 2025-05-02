from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class UserCreate(BaseModel):
    email: str
    name: str
    password: str

class HouseholdCreate(BaseModel):
    name: str

class ChoreCreate(BaseModel):
    name: str
    frequency: str

class ExpenseCreate(BaseModel):
    amount: float
    description: str
    date: date
    payer_id: int
    household_id: int

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    email: str
    password: str


class HouseholdOut(BaseModel):
    id: int
    name: str
    invite_token: str
    class Config:
        orm_mode = True

from uuid import uuid4


