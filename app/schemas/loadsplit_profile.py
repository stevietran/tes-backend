from pydantic import BaseModel
from typing import Optional

class LoadSplitProfileBase(BaseModel):
    time: float
    value: float

class LoadSplitProfileCreate(LoadSplitProfileBase):
    parent_id: Optional[int]

class LoadSplitProfileInDb(LoadSplitProfileBase):
    class Config:
        orm_mode = True

class LoadSplitProfileUpdate(LoadSplitProfileCreate):
    ...