import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pymongo

from config import MONGODB_URI
from enums import INGRESS_VIDEO_STATUS

from router.ingress_video_router import router as ingress_video_router
from router.video_game_router import router as video_game_router
from router.search_query_router import router as search_query_router
from router.ws.downloads_ws_router import router as downloads_ws_router
from router.test_router import router as test_router
from utils.video_download.video_download_worker import VideoDownloadWorker
from utils.video_scrapping.video_scrapping_worker import start_worker_process as start_scrapping_worker_process
from utils.video_download.video_download_worker import start_worker_process as start_download_worker_process

app = FastAPI(title="KCG Ingress Video Scrapping")
# worker = VideoDownloadWorker(fetch_interval=3)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingress_video_router, prefix="/api/v1")
app.include_router(video_game_router, prefix="/api/v1")
app.include_router(search_query_router, prefix="/api/v1")
app.include_router(test_router)
app.include_router(downloads_ws_router)


def create_index_if_not_exists(collection, index_key, index_name):
    existing_indexes = collection.index_information()
    
    if index_name not in existing_indexes:
        collection.create_index(index_key, name=index_name)
        print(f"Index '{index_name}' created on collection '{collection.name}'.")
    else:
        print(f"Index '{index_name}' already exists on collection '{collection.name}'.")


def startup_db_client():
    app.mongodb_client = pymongo.MongoClient(MONGODB_URI, uuidRepresentation="standard")
    app.mongodb_db = app.mongodb_client["ingress-video-scrapping"]
    app.ingress_video_collection = app.mongodb_db["ingress-video"]
    app.video_game_collection = app.mongodb_db["video-game"]
    app.search_query_collection = app.mongodb_db["search-query"]

    ingress_video_title=[
        ('video_title', pymongo.ASCENDING)
    ]
    create_index_if_not_exists(app.ingress_video_collection ,ingress_video_title, 'ingress_video_title')
    
    ingress_video_resolution=[
        ('video_title', pymongo.ASCENDING),
        ('video_resolution', pymongo.ASCENDING)
    ]
    create_index_if_not_exists(app.ingress_video_collection ,ingress_video_resolution, 'ingress_video_resolution')
    
    ingress_video_length=[
        ('video_title', pymongo.ASCENDING),
        ('video_length', pymongo.ASCENDING)
    ]
    create_index_if_not_exists(app.ingress_video_collection ,ingress_video_length, 'ingress_video_length')
    
    ingress_video_filesize=[
        ('video_title', pymongo.ASCENDING),
        ('video_filesize', pymongo.ASCENDING)
    ]
    create_index_if_not_exists(app.ingress_video_collection ,ingress_video_filesize, 'ingress_video_filesize')
    
    ingress_video_frame_rate=[
        ('video_title', pymongo.ASCENDING),
        ('video_frame_rate', pymongo.ASCENDING)
    ]
    create_index_if_not_exists(app.ingress_video_collection ,ingress_video_frame_rate, 'ingress_video_frame_rate')


async def startup():
    startup_db_client()
    # app.download_worker_process = start_download_worker_process()
    # app.scrapping_worker_process = start_scrapping_worker_process()


async def shutdown_db_client() -> None:
    app.mongodb_client.close()


async def shutdown():
    await shutdown_db_client()
    if hasattr(app, "download_worker_process"):
        app.download_worker_process.terminate()
        app.download_worker_process.join()
    if hasattr(app, "scrapping_worker_process"):
        app.scrapping_worker_process.terminate()
        app.scrapping_worker_process.join()


def add_ingress_videos():
    ingress_videos = []

    import json
    from tqdm import tqdm

    with open("data/all_ingress_videos.json", "r") as f:
        ingress_videos = json.load(f)

    for ingress_video in tqdm(ingress_videos):
        ingress_video["status"] = INGRESS_VIDEO_STATUS.DOWNLOADED
        ingress_video["processed"] = True
        app.ingress_video_collection.insert_one(ingress_video)


def add_video_games():

    video_games = []
    import json
    from tqdm import tqdm

    with open("data/all_video_games.json", "r") as f:
        video_games = json.load(f)
    for video_game in tqdm(video_games):
        app.video_game_collection.insert_one(video_game)


app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)


if __name__ == "__main__":
    config = uvicorn.Config(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=4,
        log_level="info",
        access_log=True,
        use_colors=True,
    )

    server = uvicorn.Server(config)
    server.run()
