from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any

from app import schemas
from app.api import deps
from app import crud
from app.core.auth import authenticate, create_access_token

from app.models.user import User

router = APIRouter()


@router.post("/login")
def login(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """
    user = authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer",
    }

@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: User = Depends(deps.get_current_user)):
    """
    Fetch the current logged in user.
    """

    user = current_user
    return user

@router.post("/signup", response_model=schemas.User, status_code=201)  # a Pydantic response_model which shapes the endpoint JSON response
def create_user_signup(
    *,
    db: Session = Depends(deps.get_db),  # the database as a dependency of the endpoint via FastAPI’s dependency injection capabilities
    user_in: schemas.UserCreate,  # the UserCreate pydantic schema
) -> Any:
    
    """
    Create new user without the need to be logged in.
    """

    user = db.query(User).filter(User.email == user_in.email).first()  # Check if the user email is existed
    if user:
        raise HTTPException(  # Error Handling
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = crud.user.create(db=db, obj_in=user_in)  # Create a new user

    return user