from pydantic import BaseModel
from typing import Optional, Sequence

class ElectricSplitProfileBase(BaseModel):
    time: float
    value: Sequence[float]
    

class ElectricSplitProfileCreate(ElectricSplitProfileBase):
    parent_id: Optional[int]
    with_tes:  Optional[bool]

class ElectricSplitProfileInDb(ElectricSplitProfileBase):
    class Config:
        orm_mode = True

class ElectricSplitProfileUpdate(ElectricSplitProfileCreate):
    ...