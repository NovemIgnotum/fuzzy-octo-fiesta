from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import Optional
from datetime import datetime
from app.models.user import User, UserCreate, UserUpdate, UserResponse
import hashlib

class UserService:

    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database["users"]

    def _hash_password(self, password: str) ->str:
        return hashlib.sha256(password.encode()).hexdigest()

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        existing_user = await self.collection.find_one({"email": user_data.email})
        if existing_user:
            raise ValueError("Email already registered")

        user_dict = user_data.model_dump(exclude={'password'})
        user_dict['hashed_password'] = self._hash_password(user_data.password)
        user_dict['created_at'] = datetime.now()
        user_dict['updated_at'] = datetime.now()

        result = await self.collection.insert_one(user_dict)

        created_user = await self.collection.find_one({"_id": result.inserted_id})
        if not created_user:
            raise ValueError("Failed to create user")

        return UserResponse.model_validate(created_user)