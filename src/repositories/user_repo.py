from typing import List
from supabase import AClient as Client
from src.models.users import User, UserUpdate


class UserRepository:
    def __init__(self, supabase: Client):
        self._db = supabase

    async def get_all(self) -> List[User] | None:
        res = await self._db.table("users").select("*").execute()
        return res.data if res.data else None

    async def get_by_id(self, id: str) -> User | None:
        res = await self._db.table("users").select("*").eq("id", id).execute()
        return res.data[0] if res.data else None

    async def update(self, id: str, data: UserUpdate) -> User | None:
        payload = data.model_dump(exclude_none=True)
        if not payload:
            return await self.get_by_id(id)
        res = await self._db.table("users").update(payload).eq("id", id).execute()
        return res.data[0] if res.data else None

    async def delete(self, id: str) -> bool:
        res = await self._db.table("users").delete().eq("id", id).execute()
        return len(res.data) > 0
