import asyncio
from utils.http.requests import http_get_pending_ingress_videos
from utils.video_download.video_download_manager import VideoDownloadManager
from utils.logger import download_logger
from multiprocessing import Process


class VideoDownloadWorker:
    def __init__(self, fetch_interval: int = 30):
        self.fetch_interrval = fetch_interval
        self.download_manager = VideoDownloadManager()
        self.is_running = False
        self.max_downloads = 4

    async def process_pending_downloads(self):
        pending_videos = http_get_pending_ingress_videos()
        added_downloads = 0 # Number of videos added to download
        if pending_videos is None:
            return
        for video in pending_videos:
            video_id = video["video_id"]
            game_id = video["game_id"]
            video_url = video["video_url"]
            format = "bv[height=720][fps=60]/bv[height=720][fps=30]"

            # Check if video is already being downloading and it is able to download with max_downloads
            # and if not, add it to the download queue
            if not (self.download_manager.get_downloading_status(video_id)
                and self.download_manager.get_active_downloads_count() < self.max_downloads):
                download_logger.info("Starting downloading video %s", video_id)
                await self.download_manager.start_download(
                    game_id, video_id, video_url, format
                )
                added_downloads += 1
        
        return added_downloads

    async def run(self):
        self.is_running = True
        while self.is_running:
            try:
                active_downloads_count = (
                    self.download_manager.get_active_downloads_count()
                )
                if self.max_downloads > active_downloads_count:
                    # add download to the queue
                    added_downloads = await self.process_pending_downloads()
                    # If no new downloads were added, idle for a while
                    if added_downloads == 0 and active_downloads_count == 0:
                        download_logger.info("There is a pending video to download, will idle for %s", self.fetch_interrval)
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
