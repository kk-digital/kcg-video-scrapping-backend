import yt_dlp
from yt_dlp.utils import DownloadError
import random

import sys

sys.path.insert(0, "./")

from config import COOKIES_PATH
from utils.logger import scrapping_logger

class VideoScrapper:
    _proxies = None

    @property
    def proxies(self):
        raise ValueError("Proxies is write-only")

    @proxies.setter
    def proxies(self, new_value):
        self._proxies = new_value

    @classmethod
    def scrapping_video_urls_with_search_query(
        cls,
        search_query: str,
    ):
        ydl_opts = {
            "quiet": True,  # Suppress output
            "extract_flat": True,  # Extract metadata only, do not download videos
            "proxy": random.choice(cls._proxies) if cls._proxies else None,
        }

        video_urls = None
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url=search_query, download=False)
                video_urls = cls.extract_all_video_urls(info)
            except Exception as e:
                scrapping_logger.error("Error in scrapping_video_urls_with_search_quer %s. Error: %s", search_query, e)
                return None

        return video_urls

    @classmethod
    def extract_all_video_urls(cls, data):
        all_video_urls = []
        if data.get("_type", None) == "url":
            video_url = cls.get_video_url(data)
            if video_url:
                all_video_urls.append(video_url)
        elif data.get("_type", None) == "playlist":
            entries = data.get("entries", [])
            for entry in entries:
                video_urls = cls.extract_all_video_urls(entry)
                all_video_urls.extend(video_urls)
        else:
            print("Not support format: {}".format(data.get("_type", None)))

        return all_video_urls

    @classmethod
    def get_video_url(cls, data: dict):
        url = data.get("url", None)
        # If the url is for youtube short video, it will return None
        if "short" in url:
            url = None
        return url

    @classmethod
    def get_video_metadata(cls, video_url):
        ydl_opts = {
            "cookiefile": COOKIES_PATH, # Download with cookie
            "quiet": True,  # Suppress output
            "proxy": random.choice(cls._proxies) if cls._proxies else None, # Rotate proxy
            "extract_flat": True,  # Extract metadata only, do not download videos
            "format": "bv[height=720][fps=60]/bv[height=720][fps=30]",
        }

        video_metadata = None
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url=video_url, download=False)
                video_metadata = cls.extract_video_metadata(info)
            except Exception as e:
                scrapping_logger.error("Error in get_video_metadata: %s", e)
                if "Sign in to confirm you’re not a bot" in str(e):
                    # if scrapper faced the error - "Sign in to confirm you’re not a bot", will raise the exception
                    # it means that the ip is blocked by youtube, cookie is expired or etc
                    raise Exception("Sign in to confirm you’re not a bot")

        return video_metadata

    @classmethod
    def extract_video_metadata(cls, data):
        # return necessary value from video object
        return {
            "channel_id": data.get("channel_id", ""),
            "channel_url": data.get("channel_url", ""),
            "video_id": data.get("id", ""),
            "file_hash": "",
            "file_path": "",
            "video_url": f"https://www.youtube.com/watch?v={data.get('id', '')}",
            "video_title": data.get("title", ""),
            "video_description": data.get("description", ""),
            "video_resolution": "{}p".format(data.get("height", "")), # ex. 720p
            "video_extension": data.get("ext", ""),
            "video_length": data.get("duration", 0),
            "video_filesize": (
                data.get("filesize")
                if data.get("filesize") is not None
                else data.get("filesize_approx", 0)
            ),
            "video_frame_rate": data.get("fps", 0),
            "video_language": data.get("language", ""),
        }
