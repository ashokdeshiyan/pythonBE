
import uvicorn
from fastapi import FastAPI, HTTPException
import config
from sqlalchemy.exc import SQLAlchemyError

from database import check_db_connection
app = FastAPI(title=config.APP_NAME)


@app.get("/")
def home():
    return {
        "message": "Welcome to the chat application!",
        "app_name": config.APP_NAME
    }

@app.get("/db-check")
def db_check():
    try:
        result = check_db_connection()

        return {
            "database": "connected",
            "test_query_result": result
        }

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True
    )
