from typing import List
from supabase import AClient as Client
from src.models.conversations import Conversation, ConversationCreate


class ConversationRepository:
    def __init__(self, supabase: Client):
        self._db = supabase

    async def get_all(self) -> List[Conversation] | None:
        res = await self._db.table("conversations").select("*").execute()
        return res.data if res.data else None

    async def get_by_id(self, id: str) -> Conversation | None:
        res = await self._db.table("conversations").select("*").eq("id", id).execute()
        return res.data[0] if res.data else None

    async def get_by_user_id(self, user_id: str) -> List[Conversation] | None:
        res = await self._db.table("conversations").select("*").eq("user_id", user_id).execute()
        return res.data if res.data else None

    async def create(self, data: ConversationCreate) -> Conversation | None:
        res = await self._db.table("conversations").insert({
            "user_id": data.user_id,
            "title": data.title,
            "message_count": 0,
        }).execute()
        return res.data[0] if res.data else None

    async def update_message_count(self, id: str, message_count: int) -> bool:
        res = await self._db.table("conversations").update({
            "message_count": message_count
        }).eq("id", id).execute()
        return len(res.data) > 0

    async def delete(self, id: str) -> bool:
        res = await self._db.table("conversations").delete().eq("id", id).execute()
        return len(res.data) > 0
    