from pydantic import BaseModel
from typing import Optional

class FlowProfileBase(BaseModel):
    parent_id: Optional[int]

class FlowProfileCreate(FlowProfileBase):
    time: float
    value: float

class FlowProfileUpdate(FlowProfileBase):
    ...