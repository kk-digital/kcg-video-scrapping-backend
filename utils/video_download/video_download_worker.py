import asyncio
from utils.http.requests import http_get_pending_ingress_videos, http_get_downloadding_ingress_videos
from utils.video_download.video_download_manager import VideoDownloadManager
from utils.logger import download_logger
from multiprocessing import Process
from utils.disk_utils import get_disk_space


class VideoDownloadWorker:
    def __init__(self, fetch_interval: int = 30):
        self.fetch_interrval = fetch_interval
        self.download_manager = VideoDownloadManager()
        self.is_running = False
        self.max_downloads = 1 # Max number of videos that can be downloaded at the same time

    async def process_pending_downloads(self):
        videos_to_process = http_get_downloadding_ingress_videos() or http_get_pending_ingress_videos() or []
        added_downloads = 0 # Number of videos added to download
        if videos_to_process is None:
            return
        for video in videos_to_process:
            video_id = video["video_id"]
            game_id = video["game_id"]
            video_url = video["video_url"]
            format = "bv[height=720][fps=60]/bv[height=720][fps=30]"

            # Check if video is already being downloading and it is able to download with max_downloads
            # and if not, add it to the download queue
            if not (self.download_manager.get_downloading_status(video_id)
                and self.download_manager.get_active_downloads_count() < self.max_downloads):
                await self.download_manager.start_download(
                    game_id, video_id, video_url, format
                )
                added_downloads += 1
        
        return added_downloads

    async def run(self):
        self.is_running = True
        while self.is_running:
            disk_space = await get_disk_space()
            if disk_space["percent"] > 90:
                download_logger.warning("Disk space is low, will idle for %s", self.fetch_interrval * 10)
                await asyncio.sleep(self.fetch_interrval * 10)
                continue
            try:
                active_downloads_count = (
                    self.download_manager.get_active_downloads_count()
                )
                if self.max_downloads > active_downloads_count:
                    # add download to the queue
                    added_downloads = await self.process_pending_downloads()
                    # If no new downloads were added, idle for a while
                    if added_downloads == 0 and active_downloads_count == 0:
                        download_logger.info("There is a no pending video to download, will idle for %s", self.fetch_interrval)
                    
                    await asyncio.sleep(self.fetch_interrval)
                elif self.max_downloads < active_downloads_count:
                    download_logger.info(f"Max downloads({self.max_downloads}) reached, will idle for %s", self.fetch_interrval)
                
                # Idle for a while
                await asyncio.sleep(3)
            except Exception as e:
                self.is_running = False
                download_logger.error("Error in VideoDownloadWorker: %s", e)
                await asyncio.sleep(self.fetch_interrval)

    async def stop(self):
        self.is_running = False
        # TODO: Add cleanup logic to stop all active downloads
        download_logger.info("Video download worker stopped")


def run_worker():
    worker = VideoDownloadWorker(fetch_interval=10)
    asyncio.run(worker.run())


def start_worker_process():
    worker_process = Process(target=run_worker)
    worker_process.start()
    return worker_process
