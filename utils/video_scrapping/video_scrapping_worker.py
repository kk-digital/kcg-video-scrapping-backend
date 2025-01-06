import asyncio
from multiprocessing import Process

from utils.http.requests import http_get_pending_query, http_update_query, http_add_ingress_video
from utils.video_scrapping.video_scrapper import VideoScrapper
from utils.logger import scrapping_logger

from config import PROXIES
from enums import SEARCH_QUERY_STATUS

class VideoScrappingWorker:
    def __init__(self, fetch_interval: int = 30):
        self.fetch_interval = fetch_interval
        self.is_running = False
        self.max_workers = 4
        VideoScrapper.proxies = PROXIES

    async def process_pending_downloads(self):
        pending_queries = http_get_pending_query()

        if pending_queries and len(pending_queries) > 0:
            for pending_query in pending_queries:
                query = pending_query["query"]
                extracted_video_urls = VideoScrapper.scrapping_video_urls_with_search_query(query)

                for video_url in extracted_video_urls:
                    video_metadata = VideoScrapper.get_video_metadata(video_url)

                    if video_metadata:
                        video_metadata["game_id"] = pending_query["game_id"]
                        http_add_ingress_video(video_metadata)
                        pending_query["status"] = SEARCH_QUERY_STATUS.EXTRACTED
                    else:
                        pending_query["status"] = SEARCH_QUERY_STATUS.FAILED

                    # update search query as extracted
                    http_update_query(pending_query)
                    
                    # sleep for 3 seconds to allow the scrippint to avoid blocking from youtube
                    await asyncio.sleep(3)
        else:
            scrapping_logger.info(f"There is no pending query, will sleep for {self.fetch_interval} seconds...")
            await asyncio.sleep(self.fetch_interval)
    async def run(self):
        self.is_running = True
        while self.is_running:
            try:
                await self.process_pending_downloads()
            except Exception as e:
                self.is_running = False
                scrapping_logger.error("Error in VideoScrappingWorker: %s", e)
                await asyncio.sleep(self.fetch_interval)

    async def stop(self):
        self.is_running = False
        # TODO: Add cleanup logic to stop all active downloads
        scrapping_logger.info("Video download worker stopped")


def run_worker():
    worker = VideoScrappingWorker(fetch_interval=10)
    asyncio.run(worker.run())


def start_worker_process():
    worker_process = Process(target=run_worker)
    worker_process.start()
    return worker_process
