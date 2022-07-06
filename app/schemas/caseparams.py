from pydantic import BaseModel
from typing import Optional, Sequence

from app.schemas.flowprofile import FlowProfileCreate

class CaseParamsBase(BaseModel):
    case_id: Optional[int]

class CaseParamsCreate(CaseParamsBase):
    app: str
    accuracy_level: str
    pressure: float
    upper_temperature: float
    lower_temperature: float

class CaseParamsUpdate(CaseParamsBase):
    ...

# APP 2
class CaseParamsBase_2(BaseModel):
    app: str
    accuracy_level: str
    country_selection: str
    safety_factor: float

class CaseParamsRequest_2(CaseParamsBase_2):
    ...

class CaseParamsCreate_2(CaseParamsBase_2):
    case_id: Optional[int]
    load_selection: Optional[str]
    load_value: Optional[float]
    has_profiles: Optional[bool]
    
    class Config:
        orm_mode = True

class CaseParamsGet_2(CaseParamsBase_2):
    class Config:
        orm_mode = True

class CaseParamsUpdate_2(CaseParamsBase):
    ...