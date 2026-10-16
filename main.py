# main.py

import uvicorn
import config
from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pwdlib import PasswordHash

from database import engine, get_db
from models import User
from schemas import UserResponse, UserCreate
from routes.auth import router as auth_router

# ✅ Create FastAPI app
app = FastAPI()

# ✅ Register Routes
app.include_router(auth_router)

# ✅ Create tables if not exists
User.metadata.create_all(bind=engine)

# ✅ Password hashing
password_hash = PasswordHash.recommended()


@app.get("/")
def health_check():
    return {"status": "Server is running ✅"}


@app.post(
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


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.HOST,
        #port=config.PORT,
        reload=True
    )