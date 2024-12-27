import random
import yt_dlp
import sys
import os
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, "./")

from config import VIDEO_DOWNLOAD_DIR
from utils.constants import CHANNEL_URL_TYPE, PLAYLIST_URL_TYPE, VIDEO_URL_TYPE
from utils.logger import scrap_logger


class VideoMetadataScrapper:

    _output_dir = VIDEO_DOWNLOAD_DIR
    proxies = []

    def __init__(self):
        pass

    @property
    def output_dir(cls):
        return cls._output_dir

    @output_dir.setter
    def output_dir(cls, new_value):
        cls._output_dir = new_value

    @property
    def proxies(self):
        raise AttributeError("Proxies is write-only")

    @proxies.setter
    def proxies(cls, new_value):
        # proxies vlaue should be a list of proxies
        cls._proxies = new_value

    @classmethod
    def get_channel_videos(cls, channel_url):
        ydl_opts = {
            "extract_flat": True,  # Extract metadata only, do not download videos
            "force_generic_extractor": True,
        }

        videos = []
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get the information about the channel
            info_dict = ydl.extract_info(channel_url, download=False)

            # Extract video details
            raw_videos = info_dict.get("entries", [])

            for raw_video in raw_videos:
                videos.append(cls._extract_video_metadata_from_raw_data(raw_video))

        return videos

    @classmethod
    def get_video_by_video_url(
        cls, url: str, format: str = "bv[height=720][fps=60]/bv[height=720][fps=30]/bv"
    ):
        proxy = random.choice(cls.proxies)
        ydl_opts = {
            "proxy": proxy,
            "format": format,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url=url, download=False)
            except Exception as e:
                scrap_logger.error("Error in extract_video_metadata_by_url: %s", e)
                return None

            video_metadata = cls._extract_video_metadata_from_raw_data(info)

            return video_metadata

    @classmethod
    def get_playlist_videos(cls, playlist_url):
        return cls.get_channel_videos(playlist_url)

    def _extract_video_metadata_from_raw_data(self, raw_data):
        # return necessary value from video object
        return {
            "channel_id": raw_data.get("channel_id", ""),
            "channel_url": raw_data.get("channel_url", ""),
            "video_id": raw_data.get("id", ""),
            "video_url": f"https://www.youtube.com/watch?v={raw_data.get('id', '')}",
            "video_title": raw_data.get("title", ""),
            "video_description": raw_data.get("description", ""),
            "video_extension": raw_data.get("ext", ""),
            "video_length": raw_data.get("duration", ""),
            "video_filesize": raw_data.get("filesize", ""),
            "video_frame_rate": raw_data.get("fps", ""),
            "video_language": raw_data.get("language", ""),
        }

    @staticmethod
    def get_video_url_type(url: str):
        """
        This function is used to get url type.
        """

        if "youtube.com/watch" in url:
            return VIDEO_URL_TYPE
        elif "youtube.com/playlist" in url:
            return PLAYLIST_URL_TYPE
        elif "youtube.com/channel" in url:
            return CHANNEL_URL_TYPE
        else:
            return None

    @classmethod
    def get_video_id_from_url(url: str) -> str:
        # Parse the URL using urlparse
        parsed_url = urlparse(url=url)

        # Extract the query parameters using parse_qs
        query_params = parse_qs(qs=parsed_url.query)
        # Get the value of the 'v' parameter
        video_short_hash = query_params.get("v", [""])[0]

        if not video_short_hash:
            raise ValueError("The video short hash is empty.")

        return video_short_hash
