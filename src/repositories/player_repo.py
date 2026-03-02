from typing import List
from supabase import AClient as Client
from src.models.players import Player, PlayerCreate, PlayerUpdate


class PlayerRepository:
    def __init__(self, supabase: Client):
        self._db = supabase

    async def get_all(self) -> List[Player] | None:
        res = await self._db.table("players").select("*").execute()
        return res.data if res.data else None

    async def get_by_id(self, id: str) -> Player | None:
        res = await self._db.table("players").select("*").eq("id", id).maybe_single().execute()
        return res.data if res.data else None

    async def get_by_name(self, name: str) -> List[Player] | None:
        res = await self._db.table("players").select("*").ilike("name", f"%{name}%").execute()
        return res.data if res.data else None

    async def create(self, data: PlayerCreate) -> Player | None:
        res = await self._db.table("players").insert({
            "avatar_id": data.avatar_id,
            "name": data.name,
            "age": data.age,
            "nationality": data.nationality,
            "league": data.league.value,
            "club": data.club,
            "position": data.position.value,
            "shirt_number": data.shirt_number,
            "height": data.height,
            "weight": data.weight,
            "right_foot": data.right_foot.value,
            "left_foot": data.left_foot.value,
            "skill": data.skill.value,
            "appearances": data.appearances,
            "minutes_played": data.minutes_played,
            "goals": data.goals,
            "assists": data.assists,
            "clearances": data.clearances,
            "yellow_cards": data.yellow_cards,
            "red_cards": data.red_cards,
            "max_speed": data.max_speed,
        }).select("*").execute()
        return res.data[0] if res.data else None

    async def update(self, id: str, data: PlayerUpdate) -> Player | None:
        payload = data.model_dump(exclude_none=True)
        if not payload:
            return await self.get_by_id(id)
        # serialize enum values
        for key in ("league", "position", "right_foot", "left_foot", "skill"):
            if key in payload:
                payload[key] = payload[key].value
        res = await self._db.table("players").update(payload).eq("id", id).select("*").execute()
        return res.data[0] if res.data else None

    async def delete(self, id: str) -> bool:
        res = await self._db.table("players").delete().eq("id", id).execute()
        return len(res.data) > 0
    