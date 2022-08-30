from pydantic import BaseModel
from typing import Optional, Sequence

class LoadSplitProfileBase(BaseModel):
    time: float
    value: Sequence[float]


class LoadSplitProfileCreate(LoadSplitProfileBase):
    parent_id: Optional[int]
    with_tes:  Optional[bool]

class LoadSplitProfileInDb(LoadSplitProfileBase):
    class Config:
        orm_mode = True

class LoadSplitProfileUpdate(LoadSplitProfileCreate):
    ...