from fastapi import HTTPException
from pymongo.collection import Collection


def get_all_video_games(collection: Collection, offset: int, limit: int):
    return list(collection.find({}, {"_id": 0}).skip(offset).limit(limit))


def get_video_game_by_game_id(collection: Collection, game_id: str):
    result = collection.find_one({"game_id": game_id}, {"_id": 0})

    if result is None:
        raise HTTPException(status_code=404, detail="Video game not found")

    return dict(result)


def add_video_game(collection: Collection, video_game: dict):
    if get_video_game_by_game_id(collection, video_game["game_id"]):
        raise HTTPException(status_code=422, detail="Video game already exists")

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


def exists_video_game_by_game_id(collection: Collection, game_id: str):
    return collection.find_one({"game_id": game_id}) is not None
