import yt_dlp
import sys

sys.path.insert(0, "./")

ydl_opts = {
    "format": "bv[height=720][fps=60]/bv[height=720][fps=30]", # specific file format
    "cookiefile": "cookies.txt", # cookie file path
    "http_headers": {  
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    },
    "outtmpl": "%(title)s.%(ext)s", # download file name format
}

url = "https://www.youtube.com/watch?v=spQ4O-JrO9Q"

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        # First, list available formats
        info_dict = ydl.extract_info(url=url, download=False)
        print(info_dict)  # Print available formats to debug

        # Now, attempt to download
        ydl.extract_info(url=url, download=True)
    except Exception as e:
        print(f"Error in downloading {url}: {e}")

# Note: if this script is not working well, you have to change cookie
# or user agent. And you have to check yt-dlp library documentation to ensure
# that you are using the correct options if policy of youtube changed.
# https://github.com/yt-dlp/yt-dlp
# https://github.com/coletdjnz/yt-dlp-youtube-oauth2
# https://github.com/yt-dlp/yt-dlp/wiki/Extractors#logging-in-with-oauth