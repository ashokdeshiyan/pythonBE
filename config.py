
import os
from dotenv import load_dotenv

load_dotenv()
# Server settings: defined on main
APP_NAME = os.getenv("APP_NAME", "MyFastAPIApp")
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "9000"))

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "mydb01")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")