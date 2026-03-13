from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from src.repositories import PlayerRepository
from src.models.players import Player, PlayerCreate, PlayerUpdate
from src.core.dependencies import get_player_repo

router = APIRouter(prefix="/players", tags=["Players"])


@router.get("/", response_model=List[Player])
async def get_all_players(repo: PlayerRepository = Depends(get_player_repo)):
    players = await repo.get_all()
    return players or []


@router.get("/{player_id}", response_model=Player)
async def get_player_by_id(
    player_id: str,
    repo: PlayerRepository = Depends(get_player_repo),
):
    player = await repo.get_by_id(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.get("/search/{name}", response_model=List[Player])
async def get_players_by_name(
    name: str,
    repo: PlayerRepository = Depends(get_player_repo),
):
    players = await repo.get_by_name(name)
    if not players:
        raise HTTPException(status_code=404, detail="No players found")
    return players


@router.post("/", response_model=Player, status_code=status.HTTP_201_CREATED)
async def create_player(
    data: PlayerCreate,
    repo: PlayerRepository = Depends(get_player_repo),
):
    result = await repo.create(data)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create player")
    return result


@router.patch("/{player_id}", response_model=Player)
async def update_player(
    player_id: str,
    data: PlayerUpdate,
    repo: PlayerRepository = Depends(get_player_repo),
):
    player = await repo.get_by_id(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return await repo.update(player_id, data)


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(
    player_id: str,
    repo: PlayerRepository = Depends(get_player_repo),
):
    success = await repo.delete(player_id)
    if not success:
        raise HTTPException(status_code=404, detail="Player not found")
