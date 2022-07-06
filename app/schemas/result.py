from pydantic import BaseModel, Json

from typing import Optional, Sequence
from app.schemas.cost_profile import CostProfileCreate
from app.schemas.electricsplit_profile import ElectricSplitProfileCreate

from app.schemas.loadsplit_profile import LoadSplitProfileCreate

class ResultBase(BaseModel):
    case_id: int

class ResultCreate(ResultBase):
    type: str
    htf: str
    material: str
    cost: float
    run_time: float

class ResultUpdate(ResultBase):
    ...

# Properties shared by models stored in DB
class ResultInDBBase(BaseModel):
    type: str
    htf: str
    material: str
    cost: float
    run_time: float

    class Config:
        orm_mode = True

# Properties to return to client
class Result(ResultInDBBase):
    ...

class ResultBase_2(BaseModel):
    tes_type: str
    tes_attr: dict
    tes_op_attr: dict
    chiller: str
    chiller_no_tes: str
    capex: float
    capex_no_tes: float
    lcos: float
    lcos_no_tes: float
    htf: str
    htf_attr: dict
    material: str
    material_attr: dict
    cost: float
    run_time: float

class ResultInDBBase_2(ResultBase_2):
    id: int
    case_id: int

    class Config:
        orm_mode = True    

class ResultCreate_2(ResultBase_2):
    case_id: Optional[int]

class ResultUpdate_2(ResultBase_2):
    ...

# Properties to return to client
class ResultReturn_2(ResultInDBBase_2):
    load_split_profile: Optional[Sequence[LoadSplitProfileCreate]]
    electric_split_profile: Optional[Sequence[ElectricSplitProfileCreate]]
    cost_profile: Optional[Sequence[CostProfileCreate]]

class ResultRequest_2(BaseModel):
    result_data: ResultCreate_2
    load_split_profile: Sequence[LoadSplitProfileCreate]
    electric_split_profile: Sequence[ElectricSplitProfileCreate]
    cost_profile: Sequence[CostProfileCreate]