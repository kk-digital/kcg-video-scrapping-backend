from typing import List, Optional
from fastapi import APIRouter, Query, Request

from enums import INGRESS_VIDEO_STATUS
from schema.ingress_video_schema import (
    IngressVideoCreateSchema,
    IngressVideoSchema,
    IngressVideoUpdateSchema,
    IngressVideoIdsSchema,
    IngressVideoIdsExistenceResultSchema,
)
from controller import ingress_video_controller
from schema.response_schema import ResponseSchema

router = APIRouter(prefix="/ingress-videos", tags=["ingress-videos"])


@router.get(
    "/list-ingress-videos",
    status_code=200,
    description="Get all ingress videos",
    response_model=ResponseSchema[List[IngressVideoSchema]],
)
async def list_ingress_videos(
    request: Request,
    offset: int = Query(default=0),
    limit: int = Query(default=20),
    status: Optional[INGRESS_VIDEO_STATUS] = Query(default=None),
    title: Optional[str] = Query(default=None),
    order_by: str = Query(default="created_at"),
    is_ascending: bool = Query(default=False),
):
    if offset < 0:
        offset = 0

    ingress_videos = ingress_video_controller.get_list_ingress_videos(
        request.app.ingress_video_collection, offset, limit, status, title, order_by, is_ascending
    )

    return ResponseSchema(success=True, data=ingress_videos)


@router.get(
    "/get-ingress-video-by-video-id",
    status_code=200,
    description="Get an ingress video by given id",
    response_model=ResponseSchema[IngressVideoSchema],
)
async def get_ingress_video_by_video_id(request: Request, video_id: str = Query()):
    result = ingress_video_controller.get_ingress_video_by_video_id(
        request.app.ingress_video_collection, video_id
    )
    return ResponseSchema(success=True, data=result)


@router.get(
    "/get-ingress-videos-count",
    status_code=200,
    description="Get the count of ingress videos",
    response_model=ResponseSchema[int],
)
async def get_ingress_videos_count(
    request: Request, 
    status: str = Query(default=None),
    title: Optional[str] = Query(default=None),
):
    count = ingress_video_controller.get_ingress_videos_count(
        request.app.ingress_video_collection, status, title
    )
    return ResponseSchema(success=True, data=count)


@router.post(
    "/add-ingress-video",
    status_code=200,
    description="add an ingress video",
    response_model=ResponseSchema[IngressVideoSchema],
)
async def add_ingress_video(request: Request, ingress_video: IngressVideoCreateSchema):
    added_ingress_video = ingress_video_controller.add_ingress_video(
        request.app.ingress_video_collection, ingress_video.model_dump()
    )
    return ResponseSchema(
        success=True,
        message="Ingress video added successfully",
        data=added_ingress_video,
    )


@router.post(
    "/check-existence",
    status_code=200,
    description="Get unexisted video ids",
    response_model=ResponseSchema[IngressVideoIdsExistenceResultSchema]
)
async def check_existence(request: Request, video_ids: IngressVideoIdsSchema):
    result = ingress_video_controller.check_existence(
        request.app.ingress_video_collection, video_ids.ids
    )
    return ResponseSchema(success=True, data=result)
    


@router.put(
    "/update-ingress-video",
    status_code=200,
    description="Update an ingress video with given video id and updates",
    response_model=ResponseSchema[None],
)
async def update_ingress_video(
    request: Request, ingress_video: IngressVideoUpdateSchema
):
    ingress_video_controller.update_ingress_video(
        request.app.ingress_video_collection, ingress_video.model_dump()
    )
    return ResponseSchema(success=True, message="Ingress video updated successfully")

@router.post(
        "/retry-downloading-ingress-video",
        status_code=200,
        description="Retry downloading an ingress video with given video id",
        response_model=ResponseSchema[None],
)
async def retry_downloading_ingress_video(request: Request, data: IngressVideoIdsSchema):
    ingress_video_controller.retry_downloading_ingress_video(
        request.app.ingress_video_collection, data.ids
    )
    return ResponseSchema(success=True, message="Retry downloading ingress video successfully")

@router.delete(
    "/delete-ingress-video",
    status_code=200,
    description="Delete an ingres video with given video id",
    response_model=ResponseSchema[None],
)
async def delete_ingress_video(request: Request, video_id: str = Query()):
    ingress_video_controller.delete_ingress_video(
        request.app.ingress_video_collection, video_id
    )
    return ResponseSchema(success=True, message="Ingress video deleted successfully")
