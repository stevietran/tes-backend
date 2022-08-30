from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.result import ElectricSplitProfile
from app.schemas.electricsplit_profile import ElectricSplitProfileCreate, ElectricSplitProfileUpdate

class CRUDLoadSplitProfile(CRUDBase[ElectricSplitProfile, ElectricSplitProfileCreate, ElectricSplitProfileUpdate]):
    def get_items_tes(self, db: Session,*, parent_id: int) -> List[ElectricSplitProfile]:
        return db.query(ElectricSplitProfile).filter(ElectricSplitProfile.parent_id == parent_id, ElectricSplitProfile.with_tes == True).all()

    def get_items_no_tes(self, db: Session,*, parent_id: int) -> List[ElectricSplitProfile]:
        return db.query(ElectricSplitProfile).filter(ElectricSplitProfile.parent_id == parent_id, ElectricSplitProfile.with_tes == False).all()


electricsplitprofile = CRUDLoadSplitProfile(ElectricSplitProfile)
