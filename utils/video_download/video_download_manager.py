from threading import Lock
from typing import Dict, Set
import asyncio
from concurrent.futures import ThreadPoolExecutor
import sys

from fastapi import WebSocket

sys.path.insert(0, "./")
from enums import INGRESS_VIDEO_STATUS
from utils.http.requests import http_update_ingress_video
from utils.logger import download_logger
from utils.video_download.video_downloader import VideoDownloader


class VideoDownloadManager:
    _instance = None
    _lock = Lock()
    _executor = ThreadPoolExecutor(max_workers=4)

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize()
            return cls._instance

    def _initialize(self):
        self.active_downloads: Dict[str, Dict] = {}
        self.download_tasks: Dict[str, asyncio.Task] = {}
        self.active_connections: Set[WebSocket] = set()
        self.loop = asyncio.get_event_loop()  # Store the event loop

    async def connect_client(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        download_logger.info("Client connected")

    async def disconnect_client(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        await websocket.close()
        download_logger.info("Client disconnected")

    async def broadcast_status(self, data: Dict):
        disconnected_clients = set()
        for client in self.active_connections:
            try:
                await client.send_json(data)
            except Exception as e:
                download_logger.error(f"Error broadcasting to client: {str(e)}")
                disconnected_clients.add(client)

        # Clean up disconnected clients
        for client in disconnected_clients:
            await self.disconnect_client(client)

    def _progress_hook(self, d, game_id: str, video_id: str):
        '''
        Hook to update progress of the download. It will be used in downloading using yt-dlp.
        '''
        total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
        downloaded = d.get("downloaded_bytes", 0)
        elapsed_time = d.get("elapsed", 0)
        progress = int((downloaded / total_bytes) * 100)

        if d["status"] == "downloading" and total_bytes:
            # Only update progress if it has changed significantly
            if video_id in self.active_downloads:
                current_progress = self.active_downloads[video_id]["progress"]
                print("here", current_progress, progress)
                if progress != current_progress and (progress - current_progress > 3 or progress == 100):
                    self.update_progress(INGRESS_VIDEO_STATUS.DOWNLOADING, video_id, progress, elapsed_time)
        elif d["status"] == "finished":
            self.update_progress(INGRESS_VIDEO_STATUS.DOWNLOADED, video_id, 100, elapsed_time)
        # elif d["status"] == "error":
            # self.update_progress(INGRESS_VIDEO_STATUS.FAILED, video_id, progress, elapsed_time)
            

    async def download_worker(
        self, game_id: str, video_id: str, video_url: str, format: str
    ):
        try:
            progress_hook = lambda d: self._progress_hook(d, game_id, video_id)
            await asyncio.to_thread(
                VideoDownloader.download_video,
                url=video_url,
                video_id=video_id,
                game_id=game_id,
                format=format,
                progress_hooks=[progress_hook],
            )
        except Exception as e:
            download_logger.error("Error in download_worker: %s", e)
            await self.mark_failed(video_id, str(e))

    async def start_download(
        self, game_id: str, video_id: str, video_url: str, format: str
    ) -> bool:
        download_logger.info("Starting download for video_id: %s", video_id)
        if video_id in self.active_downloads:
            download_logger.warning(
                "Download already in progress for video_id: %s", video_id
            )
            return False

        # add video into active downloads
        # it will be helpful to send downloading status into view
        # in real time by websocket 
        download_info = {
            "game_id": game_id,
            "video_id": video_id,
            "video_url": video_url,
            "progress": 0,
            "status": "downloading",
        }
        self.active_downloads[video_id] = download_info
        http_update_ingress_video(
            {"video_id": video_id, "status": INGRESS_VIDEO_STATUS.DOWNLOADING}
        )
        
        # add download_task task to download video
        # it will be helpful to manage to download video 
        # like cancel, pause and resume
        task = asyncio.create_task(
            self.download_worker(game_id, video_id, video_url, format)
        )
        self.download_tasks[video_id] = task

        return True

    async def cancel_download(self, video_id: str):
        if video_id in self.download_tasks:
            task = self.download_tasks.pop(video_id)
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

            if video_id in self.active_downloads:
                download_info = self.active_downloads.pop(video_id)
                download_info["status"] = "cancelled"
                http_update_ingress_video(
                    {"video_id": video_id, "status": INGRESS_VIDEO_STATUS.CANCELED}
                )
                return True
        return False

    def update_progress(self, status: INGRESS_VIDEO_STATUS, video_id: str, progress: int, elapsed_time: int):
        if video_id in self.active_downloads:
            self.active_downloads[video_id]["progress"] = progress

            if status == INGRESS_VIDEO_STATUS.DOWNLOADED:
                # remove download status with given video id from active_downloads
                download_info = self.active_downloads.pop(video_id)
                # remove task from download video
                task = self.download_tasks.pop(video_id)
                
                # Update the ingress video as downloaded
                http_update_ingress_video(
                    {
                        "video_id": video_id, 
                        "status": INGRESS_VIDEO_STATUS.DOWNLOADED,
                        "elapsed_time": elapsed_time,
                        "progress": 100,
                    }
                )
                download_logger.info("Download completed for video_id: %s", video_id)
                
    async def mark_failed(self, video_id: str, error_message: str):
        if video_id in self.active_downloads:
            # remove failed video from active_downloads
            download_info = self.active_downloads.pop(video_id)
            #  remove task from download tasks
            task = self.download_tasks.pop(video_id)

            # update ingress video as failed to download
            http_update_ingress_video(
                {
                    "video_id": video_id,
                    "status": INGRESS_VIDEO_STATUS.FAILED,
                    "failed_reason": error_message,
                }
            )
            download_logger.error("Download failed for video_id: %s", video_id)

    def get_all_active_downloads(self) -> Dict[str, Dict]:
        return self.active_downloads

    def get_active_downloads_count(self) -> int:
        return len(self.active_downloads.keys())
    
    def status(self) -> bool:
        if self.get_active_downloads_count() > 0:
            return

    def get_downloading_status(self, video_id: str) -> Dict:
        """
        Get download status for a specific video_id.
        If the video_id is not found in active downloads,
        it will fetch the download info from the database.
        """
        if video_id in self.active_downloads:
            return self.active_downloads[video_id]
        return None
