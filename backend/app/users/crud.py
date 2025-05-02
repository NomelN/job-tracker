from app.users.models import UserInDB
from app.database import users_collection

def get_user(email: str) -> UserInDB | None:
    user_data = users_collection.find_one({"email": email})
    if user_data:
        return UserInDB(**user_data)
    return None
