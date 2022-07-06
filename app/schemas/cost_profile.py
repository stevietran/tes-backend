from pydantic import BaseModel
from typing import Optional

class CostProfileBase(BaseModel):
    parent_id: Optional[int]

class CostProfileCreate(CostProfileBase):
    time: float
    value: float

class CostProfileUpdate(CostProfileBase):
    ...