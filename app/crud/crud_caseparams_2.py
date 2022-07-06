from typing import Optional
from app.crud.base import CRUDBase
from app.models.case import CaseParams_2
from app.schemas.caseparams import CaseParamsCreate_2, CaseParamsUpdate_2

from sqlalchemy.orm import Session

class CRUDCaseParams(CRUDBase[CaseParams_2, CaseParamsCreate_2, CaseParamsUpdate_2]):
    def get_params_by_caseid(self, db: Session,*, case_id: int) -> Optional[CaseParams_2]:
        return db.query(CaseParams_2).filter(CaseParams_2.case_id == case_id).first()


caseparams_2 = CRUDCaseParams(CaseParams_2)
