from app.crud.base import CRUDBase
from app.models.result import ElectricSplitProfile
from app.schemas.electricsplit_profile import ElectricSplitProfileCreate, ElectricSplitProfileUpdate

class CRUDLoadSplitProfile(CRUDBase[ElectricSplitProfile, ElectricSplitProfileCreate, ElectricSplitProfileUpdate]):
    ...


electricsplitprofile = CRUDLoadSplitProfile(ElectricSplitProfile)
