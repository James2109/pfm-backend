from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from src.repositories import UserRepository
from src.models.users import User, UserUpdate
from src.core.dependencies import get_user_repo, get_current_user

router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(get_current_user)])


@router.get("/me", response_model=User)
async def get_my_profile(
    current_user: dict = Depends(get_current_user),
    repo: UserRepository = Depends(get_user_repo),
):
    user = await repo.get_by_id(current_user["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/me", response_model=User)
async def update_my_profile(
    data: UserUpdate,
    current_user: dict = Depends(get_current_user),
    repo: UserRepository = Depends(get_user_repo),
):
    user = await repo.get_by_id(current_user["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await repo.update(current_user["user_id"], data)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_account(
    current_user: dict = Depends(get_current_user),
    repo: UserRepository = Depends(get_user_repo),
):
    success = await repo.delete(current_user["user_id"])
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
