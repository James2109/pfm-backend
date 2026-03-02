from typing import List
from supabase import AClient as Client
from src.models.messages import Message, MessageCreate


class MessageRepository:
    def __init__(self, supabase: Client):
        self._db = supabase

    async def get_all(self) -> List[Message] | None:
        res = await self._db.table("messages").select("*").execute()
        return res.data if res.data else None

    async def get_by_id(self, id: str) -> Message | None:
        res = await self._db.table("messages").select("*").eq("id", id).maybe_single().execute()
        return res.data if res.data else None

    async def get_by_conversation_id(self, conversation_id: str) -> List[Message] | None:
        res = await self._db.table("messages").select("*").eq("conversation_id", conversation_id).execute()
        return res.data if res.data else None

    async def create(self, data: MessageCreate) -> Message | None:
        res = await self._db.table("messages").insert({
            "conversation_id": data.conversation_id,
            "message_from": data.message_from.value,
            "message": data.message,
            "reason": data.reason,
        }).select("*").execute()
        return res.data[0] if res.data else None

    async def delete(self, id: str) -> bool:
        res = await self._db.table("messages").delete().eq("id", id).execute()
        return len(res.data) > 0
    