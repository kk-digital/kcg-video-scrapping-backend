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

    async def process_pending_queries(self):
        pending_queries = http_get_pending_query()
        if pending_queries and len(pending_queries) > 0:
            for pending_query in pending_queries:
                query = pending_query["query"]
                extracted_video_urls = VideoScrapper.scrapping_video_urls_with_search_query(query)

                # If the extracted_video_urls is None or empty array, it will update the status to failed
                if not extracted_video_urls:
                    pending_query["status"] = SEARCH_QUERY_STATUS.FAILED
                    http_update_query(pending_query)

                pending_query["status"] = SEARCH_QUERY_STATUS.EXTRACTING
                http_update_query(pending_query)

                for video_url in extracted_video_urls:
                    try:
                        video_metadata = VideoScrapper.get_video_metadata(video_url)
                    except Exception as e:
                        # if scrapper faced the error - "Sign in to confirm you're not a bot", will update the status to failed
                        # and will break the loop
                        pending_query["status"] = SEARCH_QUERY_STATUS.FAILED
                        break

                    if video_metadata:
                        # If extracting video metadata is not None, it will add the video metadata to the database
                        # and update the status to extracted
                        video_metadata["game_id"] = pending_query["game_id"]
                        http_add_ingress_video(video_metadata)

                    # sleep for 3 seconds to allow the scrippint to avoid blocking from youtube
                    await asyncio.sleep(3)
                
                if pending_query["status"] == SEARCH_QUERY_STATUS.EXTRACTING:
                    pending_query["status"] = SEARCH_QUERY_STATUS.EXTRACTED
                    http_update_query(pending_query)
                elif pending_query["status"] == SEARCH_QUERY_STATUS.FAILED:
                    http_update_query(pending_query)
        else:
            scrapping_logger.info(f"There is no pending query, will sleep for {self.fetch_interval} seconds...")
            await asyncio.sleep(self.fetch_interval)
    
    async def run(self):
        self.is_running = True
        while self.is_running:
            try:
                await self.process_pending_queries()
            except Exception as e:
                self.is_running = False
                scrapping_logger.error("Error in VideoScrappingWorker: %s", e)
                await asyncio.sleep(self.fetch_interval)

    async def stop(self):
        self.is_running = False
        # TODO: Add cleanup logic to stop all active queries
        scrapping_logger.info("Video scrapping worker stopped")


def run_worker():
    worker = VideoScrappingWorker(fetch_interval=10)
    asyncio.run(worker.run())


def start_worker_process():
    worker_process = Process(target=run_worker)
    worker_process.start()
    return worker_process
