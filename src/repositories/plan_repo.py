from typing import List
from supabase import AClient as Client
from src.models.plans import Plan, PlanCreate, PlanUpdate


class PlanRepository:
    def __init__(self, supabase: Client):
        self._db = supabase

    async def get_all(self) -> List[Plan] | None:
        res = await self._db.table("plans").select("*").execute()
        return res.data if res.data else None

    async def get_by_id(self, id: str) -> Plan | None:
        res = await self._db.table("plans").select("*").eq("id", id).maybe_single().execute()
        return res.data if res.data else None

    async def get_by_user_id(self, user_id: str) -> List[Plan] | None:
        res = await self._db.table("plans").select("*").eq("user_id", user_id).execute()
        return res.data if res.data else None

    async def create(self, data: PlanCreate) -> Plan | None:
        res = await self._db.table("plans").insert({
            "plan_name": data.plan_name,
            "user_id": data.user_id,
            "age": data.age,
            "position": data.position.value,
            "height": data.height,
            "weight": data.weight,
            "strength": data.strength,
            "weakness": data.weakness,
            "note": data.note,
            "frequency": data.frequency.value,
            "training_sessions": data.training_sessions,
            "cost_per_meal": data.cost_per_meal,
            "nutrition_plan": data.nutrition_plan,
            "training_plan": data.training_plan,
        }).select("*").execute()
        return res.data[0] if res.data else None

    async def delete(self, id: str) -> bool:
        res = await self._db.table("plans").delete().eq("id", id).execute()
        return len(res.data) > 0
    
    
    