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
from routes.register import router as register_router

# ✅ Create FastAPI app
app = FastAPI()

app.include_router(register_router)
# ✅ Register Routes
app.include_router(auth_router)

# ✅ Create tables if not exists
User.metadata.create_all(bind=engine)

# ✅ Password hashing
password_hash = PasswordHash.recommended()


@app.get("/")
def health_check():
    return {"status": "Server is running ✅"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.HOST,
        #port=config.PORT,
        reload=True
    )