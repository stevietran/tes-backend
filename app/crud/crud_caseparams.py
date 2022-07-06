from app.crud.base import CRUDBase
from app.models.case import CaseParams
from app.schemas.caseparams import CaseParamsCreate, CaseParamsUpdate


class CRUDCaseParams(CRUDBase[CaseParams, CaseParamsCreate, CaseParamsUpdate]):
    ...


caseparams = CRUDCaseParams(CaseParams)
