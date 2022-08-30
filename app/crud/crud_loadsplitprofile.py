from typing import List
from app.crud.base import CRUDBase
from app.models.result import LoadSplitProfile
from app.schemas.loadsplit_profile import LoadSplitProfileCreate, LoadSplitProfileUpdate

from sqlalchemy.orm import Session

class CRUDLoadSplitProfile(CRUDBase[LoadSplitProfile, LoadSplitProfileCreate, LoadSplitProfileUpdate]):
    def get_items_tes(self, db: Session,*, parent_id: int) -> List[LoadSplitProfile]:
        return db.query(LoadSplitProfile).filter(LoadSplitProfile.parent_id == parent_id, LoadSplitProfile.with_tes == True).all()

    def get_items_no_tes(self, db: Session,*, parent_id: int) -> List[LoadSplitProfile]:
        return db.query(LoadSplitProfile).filter(LoadSplitProfile.parent_id == parent_id, LoadSplitProfile.with_tes == False).all()


loadsplitprofile = CRUDLoadSplitProfile(LoadSplitProfile)
