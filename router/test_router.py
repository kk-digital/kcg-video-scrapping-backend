from fastapi import APIRouter, Query, Request
from enums import INGRESS_VIDEO_STATUS

router = APIRouter(prefix="/test", tags=["test"])

@router.post("/remove-all-ingress-video")
def remove_all_ingress_video(request: Request):
    request.app.ingress_video_collection.delete_many({})

@router.post("/update-all-ingress-video")
def update_all_ingress_video(request: Request, status: INGRESS_VIDEO_STATUS):
    request.app.ingress_video_collection.update_many({}, {"$set": {"status": status}})
