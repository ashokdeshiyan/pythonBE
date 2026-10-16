# routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from models import User
from schemas import UserLogin, LoginResponse
from utils.token import create_access_token, create_refresh_token
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
router = APIRouter()


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK
)
def login_user(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    # Step 1: Check if user exists
    user = db.query(User).filter(User.email == str(login_data.email)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Step 2: Verify password
    if not password_hash.verify(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    # Step 3: Generate tokens
    token_data = {"sub": str(user.id), "email": user.email}

    access_token = create_access_token(data=token_data)
   # refresh_token = create_refresh_token(data=token_data)

    # Step 4: Save tokens to DB
    user.access_token = access_token
    #user.refresh_token = refresh_token
    db.commit()
    db.refresh(user)

    # Step 5: Return response
    return LoginResponse(
        access_token=access_token,
        #refresh_token=refresh_token,
        token_type="bearer",
        user=user
    )