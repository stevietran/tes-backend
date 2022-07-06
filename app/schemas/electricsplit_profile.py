from pydantic import BaseModel
from typing import Optional

class ElectricSplitProfileBase(BaseModel):
    time: float
    value: float
    

class ElectricSplitProfileCreate(ElectricSplitProfileBase):
    parent_id: Optional[int]

class ElectricSplitProfileInDb(ElectricSplitProfileBase):
    class Config:
        orm_mode = True

class ElectricSplitProfileUpdate(ElectricSplitProfileCreate):
    ...