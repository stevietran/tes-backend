from pydantic import BaseModel

from typing import Any, List, Sequence, Optional
from datetime import datetime
from app.schemas.caseparams import CaseParamsCreate, CaseParamsCreate_2, CaseParamsGet_2, CaseParamsRequest_2
from app.schemas.flowprofile import FlowProfileCreate

APP_TYPE = ['LNG Cold Recovery', 'Cooling Peak Load Shifting']
LOAD_DATA = ['PROFILE', 'NOMIAL']
CASE_STATUS = ['SUBMITTED', 'FINISHED']

class CaseBase(BaseModel):
    case_id: Optional[int]

class CaseRequest(BaseModel):
    params: CaseParamsCreate
    flowrate: Sequence[FlowProfileCreate]

class CaseCreate(BaseModel):
    submitter_id: int
    app_type: Optional[str]

class CaseUpdate(CaseBase):
    status: str

# Properties shared by models stored in DB
class CaseInDBBase(BaseModel):
    id: int
    status: str
    submit_time: datetime

    class Config:
        orm_mode = True

# Properties to return to client
class Case(CaseInDBBase):
    ...

class CaseCelery(BaseModel):
    celery_id : str

class CaseStatusResults(BaseModel):
    result: List[Case]


# APP 2
class LoadDataRequest_2(BaseModel):
    load_type: str
    load_selection: Optional[str]
    load_value: Optional[float]
    load_profiles: Optional[Sequence[FlowProfileCreate]]

class CaseRequest_2(BaseModel):
    params: CaseParamsRequest_2
    type: str
    load_data: LoadDataRequest_2

class CaseGet_2(BaseModel):
    params: CaseParamsGet_2
    load_data: LoadDataRequest_2


