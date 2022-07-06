from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from app import crud
from app.api import deps
from app import schemas
from app.models.user import User

router = APIRouter()

"""
Fetch result by Case_ID
"""
@router.get("/{case_id}", response_model=schemas.Result)
def fetch_result(
    *,
    user: User = Depends(deps.get_current_user),
    case_id: int,
    db: Session = Depends(deps.get_db),
) -> schemas.Result:
    """
    Fetch a case status by ID
    """
    result = crud.result.get(db=db, id=case_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Case with ID {case_id} not yet has result"
        )

    return result

"""
Update Case Result
"""
@router.post("/{case_id}", response_model=schemas.Result, status_code=201)
def create_case(
    *,
    user: User = Depends(deps.get_current_active_superuser),
    case_id: int,
    result_in: schemas.ResultCreate, db: Session = Depends(deps.get_db)
) -> Any:
    # Check if result is available, if yes ask user to use update route
    result = crud.result.get(db=db, id=case_id)
    if result:
        message = f"Case with ID {case_id} already exist. If you want to update, contact admin!"
        raise HTTPException(
            status_code=404, detail=message
        )

    """
    Create a new result in the database.
    """
    result_in.case_id = case_id
    result = crud.result.create(db=db, obj_in=result_in)

    return result