from fastapi import FastAPI
import uvicorn

app = FastAPI()
users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]  # Sample data


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/users")
def get_users():
    return users


@app.post("/users")
def create_user(user: dict):
    users.append(user)
    return user

@app.put("/users/{user_id}")
def update_user(user_id: int, user: dict):
    for i, u in enumerate(users):
        if u["id"] == user_id:
            users[i] = user
            return user
    return {"error": "User not found"}


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for i, u in enumerate(users):
        if u["id"] == user_id:
            return users.pop(i)
    return {"error": "User not found"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)