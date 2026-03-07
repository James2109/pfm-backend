from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from src.repositories import PlanRepository
from src.models.plans import Plan, PlanCreate, PlanUpdate, PlanLLmInput, PlanLLmOutput
from src.services.llm_service import GeminiService
from src.core.dependencies import get_plan_repo, get_gemini_service

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.get("/", response_model=List[Plan])
async def get_all_plans(repo: PlanRepository = Depends(get_plan_repo)):
    plans = await repo.get_all()
    if not plans:
        raise HTTPException(status_code=404, detail="No plans found")
    return plans


@router.get("/{plan_id}", response_model=Plan)
async def get_plan_by_id(
    plan_id: str,
    repo: PlanRepository = Depends(get_plan_repo),
):
    plan = await repo.get_by_id(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@router.get("/user/{user_id}", response_model=List[Plan])
async def get_plans_by_user(
    user_id: str,
    repo: PlanRepository = Depends(get_plan_repo),
):
    plans = await repo.get_by_user_id(user_id)
    if not plans:
        raise HTTPException(status_code=404, detail="No plans found")
    return plans


@router.post("/", response_model=Plan, status_code=status.HTTP_201_CREATED)
async def create_plan(
    data: PlanCreate,
    repo: PlanRepository = Depends(get_plan_repo),
):
    result = await repo.create(data)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create plan")
    return result


@router.post("/generate", response_model=PlanLLmOutput)
async def generate_plan(
    data: PlanLLmInput,
    gemini_service: GeminiService = Depends(get_gemini_service),
):
    result = await gemini_service.generate_plan(data)
    return result


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan(
    plan_id: str,
    repo: PlanRepository = Depends(get_plan_repo),
):
    success = await repo.delete(plan_id)
    if not success:
        raise HTTPException(status_code=404, detail="Plan not found")
