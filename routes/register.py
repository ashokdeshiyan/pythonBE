# routes/register.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from models import User
from schemas import UserResponse, UserCreate
from utils.token import create_access_token
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
router = APIRouter()


@router.post(
    "/registerusers",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    # Hash the password
    hashed_password = password_hash.hash(user_data.password)

    # Create user object
    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        email=str(user_data.email),
        password_hash=hashed_password
    )

    # Save user to PostgreSQL
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or phone number already registered"
        )

    return new_user