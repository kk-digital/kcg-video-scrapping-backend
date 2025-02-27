from dotenv import load_dotenv
import json
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
VIDEO_DOWNLOAD_DIR = os.getenv("VIDEO_DOWNLOAD_DIR")
BASE_ENDPOINT_URL = os.getenv("BASE_ENDPOINT_URL")
COOKIES_PATH = os.getenv("COOKIES_PATH")

PROXIES = []
with open("proxies.json", "r") as f:
    PROXIES = json.load(f) 