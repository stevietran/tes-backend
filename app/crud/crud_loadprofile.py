from app.crud.base import CRUDBase
from app.models.case import LoadProfile
from app.schemas.flowprofile import FlowProfileCreate, FlowProfileUpdate

class CRUDCaseLoadProfile(CRUDBase[LoadProfile, FlowProfileCreate, FlowProfileUpdate]):
    ...


loadprofile = CRUDCaseLoadProfile(LoadProfile)
