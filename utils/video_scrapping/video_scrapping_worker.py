import asyncio
from data.add_data import http_add_ingress_video
from utils.http.requests import http_get_pending_query
from utils.logger import download_logger
from multiprocessing import Process

from utils.video_scrapping.video_scrapper import VideoScrapper


class VideoScrappingWorker:
    def __init__(self, fetch_interval: int = 30):
        self.fetch_interrval = fetch_interval
        self.is_running = False
        self.max_workers = 4

    async def process_pending_downloads(self):
        pending_queries = http_get_pending_query()
        print("123456789", pending_queries)
        if pending_queries:
            for query in pending_queries:
                query = query["query"]
                video_urls = VideoScrapper.scrapping_video_urls_with_search_query(query)
                for video_url in video_urls:
                    video_metadata = VideoScrapper.get_video_metadata(video_url)
                    video_metadata["game_id"] = query["game_id"]
                    http_add_ingress_video(video_metadata)
        else:
            await asyncio.sleep(self.fetch_interrval)

    async def run(self):
        self.is_running = True
        while self.is_running:
            try:
                await self.process_pending_downloads()
            except Exception as e:
                self.is_running = False
                download_logger.error("Error in VideoScrappingWorker: %s", e)
                await asyncio.sleep(self.fetch_interrval)

    async def stop(self):
        self.is_running = False
        # TODO: Add cleanup logic to stop all active downloads
        download_logger.info("Video download worker stopped")


def run_worker():
    worker = VideoScrappingWorker(fetch_interval=5)
    asyncio.run(worker.run())


def start_worker_process():
    worker_process = Process(target=run_worker)
    worker_process.start()
    return worker_process
