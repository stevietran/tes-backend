from app.crud.base import CRUDBase
from app.models.case import FlowProfile
from app.schemas.flowprofile import FlowProfileCreate, FlowProfileUpdate

class CRUDCaseFlowProfile(CRUDBase[FlowProfile, FlowProfileCreate, FlowProfileUpdate]):
    ...


flowprofile = CRUDCaseFlowProfile(FlowProfile)
