from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Any

from app import crud
from app.api import deps
from app import schemas
from app.clients.worker_v1 import send_celery
from app.models.user import User
from app.schemas.case import LOAD_DATA

router = APIRouter()

"""
Fetch a case status by ID
"""
@router.get("/{case_id}")
def get_case_status(
    *,
    user: User = Depends(deps.get_current_user),
    case_id: int,
    db: Session = Depends(deps.get_db)
) -> schemas.Case:

    result = crud.case.get(db=db, id=case_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Case with ID {case_id} not found"
        )
    return result

@router.put("/{case_id}")
def update_case(
    *,
    user: User = Depends(deps.get_current_user),
    case_id,
    case_in: schemas.CaseUpdate,
    db: Session = Depends(deps.get_db),
) -> schemas.Case:
    # get db item
    case_db = crud.case.get(db=db, id=case_id)

    if not case_db:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Case with ID {case_id} not found"
        )
    result = crud.case.update(db=db, db_obj=case_db, obj_in=case_in)
    return result    

@router.delete("/{case_id}")
def remove_case(
    *,
    user: User = Depends(deps.get_current_user),
    case_id: int,
    db: Session = Depends(deps.get_db)
) -> schemas.Case:

    result = crud.case.remove(db=db, id=case_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Case with ID {case_id} not found"
        )
    return result

@router.post("/all", response_model=schemas.CaseStatusResults)
def get_status_all(
    user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    """
    Search for recipes based on label keyword
    """
    cases = crud.case.get_cases_by_user_id(db=db, user_id=user.id)
    if not cases:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Case with USER_ID {user.id} not found"
        )

    return {"result": cases}

"""
Create a new case (LNG Cold Recovery)
"""
@router.post("/lcr", response_model=schemas.Case, status_code=201)
def create_case(
    *,
    user: User = Depends(deps.get_current_user),
    case_in: schemas.CaseRequest, 
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Create a new case in the database.
    """
    case = crud.case.create(db=db, obj_in=schemas.CaseCreate(submitter_id=user.id))
    
    case_in.params.case_id = case.id
    param = crud.caseparams.create(db=db, obj_in=case_in.params)
    
    for item in case_in.flowrate:
        item.params_id = param.id
        crud.flowprofile.create(db=db, obj_in=item)

    # trigger task from core
    
    res = celery_app.send_task("opt_snt")
    id = res.task_id
    print(f"task id = {id}")

    return case

"""
Create a new case (Peak Load Shifting)
"""
@router.post("/pls", response_model=schemas.Case, status_code=201)
def create_case_app_2(
    *,
    user: User = Depends(deps.get_current_user),
    case_in: schemas.CaseRequest_2, 
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Create a new case in the database.
    """
    # Check data:
    load_data = case_in.load_data

    if not load_data.load_type in LOAD_DATA:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Value Error. Check load_data/app_type variable!!!"
        )
    
    case = crud.case.create(db=db, obj_in=schemas.CaseCreate(submitter_id=user.id, app_type=case_in.type))
    
    params = schemas.CaseParamsCreate_2.from_orm(case_in.params)
    params.case_id = case.id

    if load_data.load_type == LOAD_DATA[0]:
        params.has_profiles = True
        param = crud.caseparams_2.create(db=db, obj_in=params)
    
        for item in load_data.load_profiles:
            item.parent_id = param.id
            crud.loadprofile.create(db=db, obj_in=item)
    
    elif load_data.load_type == LOAD_DATA[1]:
        params.has_profiles = False
        params.load_selection = load_data.load_selection
        params.load_value = load_data.load_value
        param = crud.caseparams_2.create(db=db, obj_in=params)

    return case

"""
Send to celery (Peak Load Shifting, Demo only)
"""
@router.post("/pls/celery", response_model=schemas.CaseCelery, status_code=201)
def send_case_app_2(
    *,
    user: User = Depends(deps.get_current_user),
    case_id: int, 
    db: Session = Depends(deps.get_db)
) -> Any:

    # SEND TASK
    id = send_celery(case_id)

    return {"celery_id": id}

@router.get("/pls/{case_id}", response_model=schemas.CaseGet_2)
def fetch_case_app_2(
    *,
    user: User = Depends(deps.get_current_user),
    case_id: int,
    db: Session = Depends(deps.get_db),
) -> schemas.Case:

    # See if the case exists
    result = crud.case.get(db=db, id=case_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Case with ID {case_id} not found"
        )

    # Get params
    param_db = crud.caseparams_2.get_params_by_caseid(db=db, case_id=case_id)
    param = schemas.CaseParamsGet_2.from_orm(param_db)

    load_data = schemas.LoadDataRequest_2.parse_obj({'load_type': LOAD_DATA[0]})
    
    if param_db.has_profiles:
        # Get profile
        load_db = crud.loadprofile.get_by_parent_id(db=db, parent_id=param_db.id)
        load_profile = []
        for item in load_db:
            load_profile.append(schemas.LoadSplitProfileInDb.from_orm(item))
        load_data.load_profiles = load_profile
    else:
        load_data.load_type = LOAD_DATA[1]
        load_data.load_selection = param_db.load_selection
        load_data.load_value = param_db.load_value

    # Return
    return {'params': param,'load_data': load_data}
