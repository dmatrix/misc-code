from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

BOLD = '\033[1m'
END = '\033[0m'

class User(BaseModel):
    id: int = Field(description="Unique identifier for the person")
    name: str = Field(description="Name of the person")
    age: int = Field(description="Age of the person")
    signup_ts: Optional[datetime] = Field(description="Signup timestamp")

user_data = {
    "id": 123,
    "name": "John Doe",
    "age": 30,
    "signup_ts": "2021-01-01 12:22"
}

# Create a User object by passing a dictionary to the User class.
# Pydantic will validate the data and parse the datetime string.
user = User(**user_data)

print(f"{BOLD}user{END}: {user}")
print(f"{BOLD}user signup date{END}: {user.signup_ts}")
