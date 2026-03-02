from supabase import AClient as Client

class LogRepository:
    def __init__(self, supabase: Client):
        self._db = supabase

    async def insert_log(self, level: str, component: str, message: str, metadata: dict | None):
        payload = {
            "level": level,
            "component": component,
            "message": message,
            "metadata": metadata or {}
        }
        return await self._db.table("system_logs").insert(payload).execute()