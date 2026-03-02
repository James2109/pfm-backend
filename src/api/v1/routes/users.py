from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from src.repositories import UserRepository
from src.models.users import UserCreate, UserUpdate, UserPasswordUpdate, UserResponse
from src.core.dependencies import get_user_repo

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
async def get_all_users(repo: UserRepository = Depends(get_user_repo)):
    users = await repo.get_all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    repo: UserRepository = Depends(get_user_repo),
):
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/username/{username}", response_model=UserResponse)
async def get_user_by_username(
    username: str,
    repo: UserRepository = Depends(get_user_repo),
):
    user = await repo.get_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    repo: UserRepository = Depends(get_user_repo),
):
    existing = await repo.get_by_username(data.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    result = await repo.create(data)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create user")
    return result


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    data: UserUpdate,
    repo: UserRepository = Depends(get_user_repo),
):
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await repo.update(user_id, data)


@router.patch("/{user_id}/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_password(
    user_id: str,
    data: UserPasswordUpdate,
    repo: UserRepository = Depends(get_user_repo),
):
    success = await repo.update_password(user_id, data.password)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    repo: UserRepository = Depends(get_user_repo),
):
    success = await repo.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")