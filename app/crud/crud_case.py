from app.crud.base import CRUDBase
from typing import Any, Dict, Generic, List, Optional, Union
from app.models.case import Case
from app.schemas.case import CaseCreate, CaseUpdate
from sqlalchemy.orm import Session

class CRUDCase(CRUDBase[Case, CaseCreate, CaseUpdate]):
    def get_cases_by_user_id(self, db: Session,*, user_id: int) -> List[Case]:
        return db.query(Case).filter(Case.submitter_id == user_id).all()
    
    def update(
        self, db: Session, *, db_obj: Case, obj_in: Union[CaseUpdate, Dict[str, Any]]
    ) -> Case:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

case = CRUDCase(Case)
