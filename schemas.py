from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class UserCreate(BaseModel):
    displayName: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    displayName: str
    email: str
    createdAt: datetime
    updatedAt: Optional[datetime]

    class Config:
        from_attributes = True