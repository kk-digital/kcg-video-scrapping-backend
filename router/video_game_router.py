from typing import List
from fastapi import APIRouter, Query, Request
from h11 import Response

from controller import video_game_controller
from schema.response_schema import ResponseSchema
from schema.video_game_schema import (
    VideoGameCreateSchema,
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
    request: Request, offset: int = Query(default=0), limit: int = Query(default=20)
):
    video_games = video_game_controller.get_all_video_games(
        request.app.video_game_collection, offset, limit
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
