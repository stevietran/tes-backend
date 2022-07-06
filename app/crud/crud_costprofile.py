from app.crud.base import CRUDBase
from app.models.result import CostProfile
from app.schemas.cost_profile import CostProfileCreate, CostProfileUpdate

class CRUDLoadSplitProfile(CRUDBase[CostProfile, CostProfileCreate, CostProfileUpdate]):
    ...


costprofile = CRUDLoadSplitProfile(CostProfile)
