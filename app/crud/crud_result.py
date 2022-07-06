from typing import List, Optional
from app.crud.base import CRUDBase
from app.models.result import Result
from app.schemas.result import ResultCreate, ResultUpdate
from sqlalchemy.orm import Session

class CRUDResult(CRUDBase[Result, ResultCreate, ResultUpdate]):
    def get_result_by_caseid(self, db: Session,*, case_id: int) -> Optional[Result]:
        return db.query(Result).filter(Result.case_id == case_id).all()

result = CRUDResult(Result)
