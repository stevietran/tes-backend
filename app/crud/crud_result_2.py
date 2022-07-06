from typing import List, Optional
from app.crud.base import CRUDBase
from app.models.result import CostProfile, ElectricSplitProfile, LoadSplitProfile, Result_2
from app.schemas.result import ResultCreate_2, ResultUpdate_2
from sqlalchemy.orm import Session

class CRUDResult_2(CRUDBase[Result_2, ResultCreate_2, ResultUpdate_2]):
    def get_result_by_caseid(self, db: Session,*, case_id: int) -> Optional[Result_2]:
        return db.query(Result_2).filter(Result_2.case_id == case_id).first()

result_2 = CRUDResult_2(Result_2)
