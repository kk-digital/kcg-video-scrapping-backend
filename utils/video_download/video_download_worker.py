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

    async def process_pending_downloads(self):
        pending_videos = http_get_pending_ingress_videos()
        if pending_videos is None:
            return
        for video in pending_videos:
            video_id = video["video_id"]
            game_id = video["game_id"]
            video_url = video["video_url"]
            format = "bv[height=720][fps=60]/bv[height=720][fps=30]"

            # Check if video is already being downloading
            if not self.download_manager.get_downloading_status(video_id):
                download_logger.info("Starting downloading video %s", video_id)
                self.download_manager.start_download(
                    game_id, video_id, video_url, format
                )

    async def run(self):
        self.is_running = True
        while self.is_running:
            try:
                if not self.download_manager.get_all_active_downloads():
                    await self.process_pending_downloads()

                print(f"No active downloads, will idle for {self.fetch_interrval}")
                await asyncio.sleep(self.fetch_interrval)
            except Exception as e:
                self.is_running = False
                download_logger.error("Error in VideoDownloadWorker: %s", e)
                await asyncio.sleep(self.fetch_interrval)

    async def stop(self):
        self.is_running = False
        # TODO: Add cleanup logic to stop all active downloads
        download_logger.info("Video download worker stopped")


def run_worker():
    worker = VideoDownloadWorker(fetch_interval=3)
    asyncio.run(worker.run())


def start_worker_process():
    worker_process = Process(target=run_worker)
    worker_process.start()
    return worker_process
