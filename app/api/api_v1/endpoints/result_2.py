from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from app import crud
from app.api import deps
from app import schemas
from app.models.user import User
from app.schemas.case import CASE_STATUS

router = APIRouter()

"""
Fetch result by Case_ID
"""
@router.get("/{case_id}", response_model=schemas.ResultReturn_2)
def fetch_result(
    *,
    user: User = Depends(deps.get_current_user),
    case_id: int,
    db: Session = Depends(deps.get_db),
) -> schemas.Result:
    """
    Fetch a case status by ID
    """
    result = crud.result_2.get_result_by_caseid(db=db, case_id=case_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Case with ID {case_id} not yet has result"
        )
    else:
        db_result = schemas.ResultInDBBase_2.from_orm(result)
        final_result = schemas.ResultReturn_2.from_orm(db_result)
        # Get profiles
        profile_1 = crud.loadsplitprofile.get_by_parent_id(db=db, parent_id = final_result.id)
        load_split_profile = []
        for item in profile_1:
            load_split_profile.append(schemas.LoadSplitProfileInDb.from_orm(item))

        final_result.load_split_profile = load_split_profile
        
        profile_2 = crud.electricsplitprofile.get_by_parent_id(db=db, parent_id = final_result.id)
        electric_split_profile = []
        for item in profile_2:
            electric_split_profile.append(schemas.ElectricSplitProfileInDb.from_orm(item))        
        final_result.electric_split_profile = electric_split_profile
        
        profile_3 = crud.costprofile.get_by_parent_id(db=db, parent_id = final_result.id)
        cost_profile = []
        for item in profile_3:
            cost_profile.append(schemas.ElectricSplitProfileInDb.from_orm(item))
        final_result.cost_profile = cost_profile
        
        return final_result

"""
Update Case Result for APP 2
"""
@router.post("/{case_id}", response_model=schemas.MessageBase, status_code=201)
def create_result(
    *,
    user: User = Depends(deps.get_current_active_superuser),
    case_id: int,
    result_in: schemas.ResultRequest_2, db: Session = Depends(deps.get_db)
) -> Any:
    # Check if result is available, if yes ask user to use update route
    result = crud.result_2.get(db=db, id=case_id)
    if result:
        message = f"Case with ID {case_id} already exist or the end_point is incorrect. If you want to update, contact admin!"
        raise HTTPException(
            status_code=404, detail=message
        )

    # Update case status:
    case_db = crud.case.get(db=db, id=case_id)

    if not case_db:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Case with ID {case_id} not found"
        )
    
    case_in = schemas.CaseUpdate(case_id=case_id, status=CASE_STATUS[1])
    
    result = crud.case.update(db=db, db_obj=case_db, obj_in=case_in) 
    
    """
    Create a new result in the database.
    """
    result_data = result_in.result_data
    result_data.case_id = case_id
    res = crud.result_2.create(db=db, obj_in=result_data)
    result_id = res.id

    # Create child tables
    for item in result_in.load_split_profile:
        item.parent_id = result_id
        crud.loadsplitprofile.create(db=db, obj_in=item)

    for item in result_in.electric_split_profile:
        item.parent_id = result_id
        crud.electricsplitprofile.create(db=db, obj_in=item)

    for item in result_in.cost_profile:
        item.parent_id = result_id
        crud.costprofile.create(db=db, obj_in=item)

    return schemas.MessageBase.parse_obj({'message': "Create result data successfully!!!"})