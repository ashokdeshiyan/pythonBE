from fastapi import FastAPI
# create FastaPI application 
app = FastAPI()

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