from fastapi import FastAPI, status, Depends, HTTPException
# create FastaPI application 

from schemas import UserResponse, UserCreate
from sqlalchemy.orm import Session
from database import SessionLocal
from pwdlib import PasswordHash
from models import User
from sqlalchemy.exc import IntegrityError
app = FastAPI()

password_hash = PasswordHash.recommended()


# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#endpoint 
@app.get("/")
def home():
    return {"message": " Hello world"}

# Get users endpoint
@app.get("/users")
def get_users():
    return [
        {"id": 1, "name": "Rahul"},
        {"id": 2, "name": "Priya"}
    ]

# Get a specific user by ID
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id,
        "message": "User fetched successfully"
    }

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
