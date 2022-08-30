from pydantic import BaseModel
from typing import Optional, Sequence

class CostProfileBase(BaseModel):
    time: float
    value: Sequence[float]

class CostProfileCreate(CostProfileBase):
    parent_id: Optional[int]
    with_tes:  Optional[bool]

class CostProfileUpdate(CostProfileBase):
    ...