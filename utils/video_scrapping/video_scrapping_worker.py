import asyncio
from multiprocessing import Process
from typing import List

from utils.http.requests import (
    http_get_pending_query, 
    http_update_query, 
    http_add_ingress_video,
    http_get_extracting_query,
    http_check_existence_videos
)
from utils.video_scrapping.video_scrapper import VideoScrapper
from utils.logger import scrapping_logger
from utils.video_processing_utils import get_youtube_video_id, get_youtube_video_url

from config import PROXIES
from enums import SEARCH_QUERY_STATUS

class VideoScrappingWorker:
    def __init__(self, fetch_interval: int = 30):
        self.fetch_interval = fetch_interval
        self.is_running = False
        self.max_workers = 4
        VideoScrapper.proxies = PROXIES

    async def process_pending_queries(self):
        extracting_queries = http_get_extracting_query()
        pending_queries = http_get_pending_query() if not extracting_queries else extracting_queries
        if pending_queries and len(pending_queries) > 0:
            for pending_query in pending_queries:
                query = pending_query["query"]
                extracted_video_urls = VideoScrapper.scrapping_video_urls_with_search_query(query)
                total_count_video_urls = len(extracted_video_urls)

                # If the extracted_video_urls is None or empty array, it will update the status to failed
                if not extracted_video_urls:
                    pending_query["status"] = SEARCH_QUERY_STATUS.FAILED
                    http_update_query(pending_query)
                    continue

                # If the extracted_video_urls is not None or empty array, it will update the status to extracting
                pending_query["status"] = SEARCH_QUERY_STATUS.EXTRACTING
                pending_query["total_video_count"] = total_count_video_urls
                http_update_query(pending_query)

                # extract metadata from video urls by batch of batch_size
                batch_size = 10
                # if query is already extracting, will start at the last point
                for index in range(pending_query["processed_video_count"], total_count_video_urls, batch_size):
                    batch_video_urls = extracted_video_urls[index:index+batch_size]
                    unexisted_video_ids = self.get_unexisted_video_urls(batch_video_urls)
                    new_video_count = 0
                    for video_url in unexisted_video_ids:
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
                            if http_add_ingress_video(video_metadata):                        
                                new_video_count += 1

                        # sleep for 3 seconds to allow the scrippint to avoid blocking from youtube
                        await asyncio.sleep(3)
                    
                    # update the status of search query processing
                    pending_query["processed_video_count"] = index + len(batch_video_urls)
                    pending_query["new_video_count"] += new_video_count
                    http_update_query(pending_query)
                
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

    def get_unexisted_video_urls(self, video_urls: List[str]):
        video_ids = [get_youtube_video_id(video_url) for video_url in video_urls]
        unexisted_video_ids = http_check_existence_videos(video_ids)["unexisted_video_ids"]
        
        return [get_youtube_video_url(video_id) for video_id in unexisted_video_ids]


def run_worker():
    worker = VideoScrappingWorker(fetch_interval=10)
    asyncio.run(worker.run())


def start_worker_process():
    worker_process = Process(target=run_worker)
    worker_process.start()
    return worker_process
