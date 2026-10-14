
import uvicorn
from fastapi import FastAPI, HTTPException
import config
from sqlalchemy.exc import SQLAlchemyError

from fastapi import status, Depends  # main: FastAPI/HTTPException already imported above
# create FastaPI application 

from schemas import UserResponse, UserCreate
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from pwdlib import PasswordHash
from models import User, Base
from sqlalchemy.exc import IntegrityError
app = FastAPI()

# ✅ YE LINE ADD KARO - Table automatically banega PostgreSQL mein
User.metadata.create_all(bind=engine)

password_hash = PasswordHash.recommended()


# Database session dependency
def get_db():
    database = SessionLocal()  # main
    try:
        yield database
    finally:
        database.close()

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

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True
    )
