import yt_dlp
import random

import sys

sys.path.insert(0, "./")

from config import PROXIES
from utils.logger import download_logger


class VideoDownloader:
    _output_dir = "output"
    _proxies = PROXIES

    @property
    def output_dir(self):
        return self._output_dir

    @output_dir.setter
    def output_dir(self, new_value):
        self._output_dir = new_value

    @property
    def proxies(self):
        raise ValueError("Proxies is write-only")

    @proxies.setter
    def proxies(self, new_value):
        self._proxies = new_value

    @classmethod
    def download_video(
        cls,
        video_id,
        url,
        game_id,
        format: str = "bv[height=720][fps=60]/bv[height=720][fps=30]",
        progress_hooks=[],
    ):
        ydl_opts = {
            "quiet": True,
            "format": format,
            "progress_hooks": progress_hooks,
            "outtmpl": f"{cls._output_dir}/S_{game_id}/{video_id}.%(ext)s",
            "proxy": random.choice(cls._proxies),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url=url, download=True)
        
        download_logger.info(f"Downloaded video {video_id} successfully")
