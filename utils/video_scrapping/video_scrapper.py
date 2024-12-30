import yt_dlp
import random

import sys

sys.path.insert(0, "./")

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

        video_urls = []
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url=search_query, download=False)
                video_urls = cls.extract_all_video_urls(info)
            except Exception as e:
                print(e)

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
    def get_video_url(data: dict):
        url = data.get("url", None)
        if "short" in url:
            url = None
        return url

    @classmethod
    def get_video_metadata(cls, video_url):
        ydl_opts = {
            "quiet": True,  # Suppress output
            "proxy": random.choice(cls._proxies) if cls._proxies else None,
            "extract_flat": True,  # Extract metadata only, do not download videos
            "format": "bv[height=720][fps=60]/bv[height=720][fps=30]",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url=video_url, download=False)
                video_metadata = cls.extract_video_metadata(info)
            except Exception as e:
                scrapping_logger.error("Error in get_video_metadata: %s", e)
                video_metadata = None

    @classmethod
    def extract_video_metadata(data):
        # return necessary value from video object
        return {
            "channel_id": data.get("channel_id", ""),
            "channel_url": data.get("channel_url", ""),
            "video_id": data.get("id", ""),
            "video_url": f"https://www.youtube.com/watch?v={data.get('id', '')}",
            "video_title": data.get("title", ""),
            "video_description": data.get("description", ""),
            "video_extension": data.get("ext", ""),
            "video_length": data.get("duration", ""),
            "video_filesize": (
                data.get("filesize")
                if data.get("filesize") is not None
                else data.get("filesize_approx", 0)
            ),
            "video_frame_rate": data.get("fps", ""),
            "video_language": data.get("language", ""),
        }
