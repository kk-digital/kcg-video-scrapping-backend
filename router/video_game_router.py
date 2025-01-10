from typing import List, Optional
from fastapi import APIRouter, Query, Request
from h11 import Response

from controller import video_game_controller
from schema.response_schema import ResponseSchema
from schema.video_game_schema import (
    VideoGameCreateSchema,
    VideoGameIdsRequest,
    VideoGameSchema,
    VideoGameUpdateSchema,
)

router = APIRouter(prefix="/video-games", tags=["video-games"])


@router.get(
    "/list-video-games",
    status_code=200,
    description="Get all video games",
    response_model=ResponseSchema[List[VideoGameSchema]],
)
async def list_video_games(
    request: Request,
    offset: int = Query(default=0),
    limit: int = Query(default=20),
    title: str = Query(default=None),
    order_by: str = Query(default="created_at"),
    is_ascending: bool = Query(default=False),
):
    # TODO: Investiage why offset is not specified in the query
    if offset < 0:
        offset = 0
    video_games = video_game_controller.get_all_video_games(
        request.app.video_game_collection, offset, limit, title, order_by, is_ascending
    )

    return ResponseSchema(
        success=True, message="Video games retrieved successfully", data=video_games
    )


@router.get(
    "/get-video-game-by-game-id",
    status_code=200,
    description="Get video game by given game id",
    response_model=ResponseSchema[VideoGameSchema],
)
async def get_video_game_by_game_id(request: Request, game_id: str):
    video_game = video_game_controller.get_video_game_by_game_id(
        request.app.video_game_collection, game_id
    )

    return ResponseSchema(
        success=True, message="Video game retrieved successfully", data=video_game
    )


@router.get(
    "/get-video-games-count",
    status_code=200,
    description="Get the count of search queries",
    response_model=ResponseSchema[int],
)
async def get_video_games_count(
    request: Request,
):
    count = video_game_controller.get_video_games_count(
        request.app.video_game_collection
    )
    return ResponseSchema(success=True, data=count)


@router.post(
    "/add-video-game",
    status_code=200,
    description="Get all video games",
    response_model=ResponseSchema[VideoGameSchema],
)
async def add_video_game(reqeust: Request, video_game: VideoGameCreateSchema):
    added_video_game = video_game_controller.add_video_game(
        reqeust.app.video_game_collection, video_game.model_dump()
    )

    return ResponseSchema(
        success=True, message="Video game added successfully", data=added_video_game
    )


@router.put(
    "/update-video-game",
    status_code=200,
    description="Update video game with given game id and updates",
    response_model=ResponseSchema[None],
)
async def update_video_game(request: Request, video_game: VideoGameUpdateSchema):
    video_game_controller.update_video_game(
        request.app.video_game_collection, video_game.model_dump()
    )

    return ResponseSchema(success=True, message="Video game updated successfully")


@router.delete(
    "/delete-video-game",
    status_code=200,
    description="Delete video game with given game id",
    response_model=ResponseSchema[None],
)
async def delete_video_game(request: Request, game_id: str):
    video_game_controller.delete_video_game(request.app.video_game_collection, game_id)

    return ResponseSchema(success=True, message="Video game deleted successfully")


@router.delete(
    "/delete-video-games",
    status_code=200,
    description="Delete video games with given game id",
    response_model=ResponseSchema[None],
)
async def delete_video_game(request: Request, game_ids: VideoGameIdsRequest):
    print("34567890-", game_ids)
    video_game_controller.delete_video_games(
        request.app.video_game_collection, game_ids.ids
    )

    return ResponseSchema(success=True, message="Video game deleted successfully")
