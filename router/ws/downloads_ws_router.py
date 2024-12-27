from fastapi import APIRouter, WebSocket
from utils.video_download.video_download_manager import VideoDownloadManager

router = APIRouter()
download_manager = VideoDownloadManager()


@router.websocket("/ws/downloads")
async def downloads_ws(websocket: WebSocket):
    await download_manager.connect_client(websocket=websocket)
    try:
        while True:
            await websocket.receive()
    except Exception:
        await download_manager.disconnect_client(websocket)
