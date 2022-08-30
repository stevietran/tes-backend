from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.result import CostProfile
from app.schemas.cost_profile import CostProfileCreate, CostProfileUpdate

class CRUDCostProfile(CRUDBase[CostProfile, CostProfileCreate, CostProfileUpdate]):
    def get_items_tes(self, db: Session,*, parent_id: int) -> List[CostProfile]:
        return db.query(CostProfile).filter(CostProfile.parent_id == parent_id, CostProfile.with_tes == True).all()

    def get_items_no_tes(self, db: Session,*, parent_id: int) -> List[CostProfile]:
        return db.query(CostProfile).filter(CostProfile.parent_id == parent_id, CostProfile.with_tes == False).all()


costprofile = CRUDCostProfile(CostProfile)
