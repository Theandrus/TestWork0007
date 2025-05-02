from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'

class TokenData(BaseModel):
    user_id: Optional[int] = None

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = 'pending'
    priority: Optional[int] = 1

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None

class TaskOut(TaskBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        orm_mode = True