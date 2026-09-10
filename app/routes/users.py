from playwright.sync_api import expect
from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Optional
from app.core.database import get_database
from app.models.user import UserCreate, UserResponse, User
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

def get_user_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> UserService:
    return UserService(db)

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user_data: UserCreate, user_service:UserService= Depends(get_user_service)):
    try:
        return await user_service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    