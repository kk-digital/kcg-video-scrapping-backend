from typing import List
from fastapi import HTTPException
import pymongo
from pymongo.collection import Collection

from schema.video_game_schema import VideoGameSchema


def get_all_video_games(collection: Collection, offset: int, limit: int, title: str):
    query = {"title": {"$regex": f".*{title}.*", "$options": "i"}} if title else {}
    return list(
        collection.find(query, {"_id": 0})
        .sort("created_at", pymongo.DESCENDING)
        .skip(offset)
        .limit(limit)
    )


def get_video_game_by_game_id(collection: Collection, game_id: str):
    result = collection.find_one({"game_id": game_id}, {"_id": 0})

    if result is None:
        raise HTTPException(status_code=404, detail="Video game not found")

    return dict(result)


def get_video_games_count(collection: Collection):
    return collection.count_documents({})


def add_video_game(collection: Collection, video_game: dict):
    if exists_video_game_by_game_id(collection, video_game["game_id"]):
        raise HTTPException(status_code=422, detail="Video game already exists")
    video_game = VideoGameSchema(**video_game).model_dump()
    collection.insert_one(video_game)

    return video_game


def update_video_game(collection: Collection, video_game: dict):
    if not exists_video_game_by_game_id(collection, video_game["game_id"]):
        raise HTTPException(status_code=404, detail="Video game not found")

    # remove key in which value is None
    video_game = {k: v for k, v in video_game.items() if v is not None}

    return collection.update_one(
        {"game_id": video_game["game_id"]}, {"$set": video_game}
    )


def delete_video_game(collection: Collection, game_id: str):
    if not exists_video_game_by_game_id(collection, game_id):
        raise HTTPException(status_code=404, detail="Video game not found")

    return collection.delete_one({"game_id": game_id})


def delete_video_games(collection: Collection, game_ids: List[str]):
    # Check if all games exist before deleting
    for game_id in game_ids:
        if not exists_video_game_by_game_id(collection, game_id):
            raise HTTPException(
                status_code=404, detail=f"Video game with id {game_id} not found"
            )

    return collection.delete_many({"game_id": {"$in": game_ids}})


def exists_video_game_by_game_id(collection: Collection, game_id: str):
    return collection.find_one({"game_id": game_id}) is not None
