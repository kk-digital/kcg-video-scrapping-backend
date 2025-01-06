import logging

# export only follow loggers
__all__ = ['scrapping_logger', 'download_logger', 'request_logger']

# log file dir
BASE_LOGGING_DIR = "logging"

# ---------------------------------- Youtube Video Scrapper Logger ----------------------------------
download_logger = logging.getLogger("youtube_video_downloader")
download_logger.setLevel(logging.INFO)

# Create a file handler
download_handler = logging.FileHandler(f"{BASE_LOGGING_DIR}/download.log")
download_handler.setLevel(logging.ERROR)
# Create a logging format
download_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
download_handler.setFormatter(download_formatter)
# Add the handlers to the download_logger
download_logger.addHandler(download_handler)

# Create a stream handler for console output
downalod_console_handler = logging.StreamHandler()
downalod_console_handler.setLevel(logging.INFO)
downalod_console_handler.setFormatter(download_formatter)
download_logger.addHandler(downalod_console_handler)

# ---------------------------------- Youtube Video Downloader Logger ----------------------------------
scrapping_logger = logging.getLogger("youtube_video_scrapper")
scrapping_logger.setLevel(logging.INFO)
# Create a file handler
scrap_handler = logging.FileHandler(f"{BASE_LOGGING_DIR}/scrapping.log")
scrap_handler.setLevel(logging.ERROR)
# Create a logging format
scrap_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
scrap_handler.setFormatter(scrap_formatter)
# Add the handlers to the scrapper_logger
scrapping_logger.addHandler(scrap_handler)

# Create a stream handler for console output
scrap_console_handler = logging.StreamHandler()
scrap_console_handler.setLevel(logging.INFO)
scrap_console_handler.setFormatter(scrap_formatter)
scrapping_logger.addHandler(scrap_console_handler)

# ---------------------------------- Request Logger ----------------------------------
request_logger = logging.getLogger("reqeust_logger")
request_logger.setLevel(logging.INFO)
# Create a file handler
request_file_handler = logging.FileHandler(f"{BASE_LOGGING_DIR}/request.log")
request_file_handler.setLevel(logging.ERROR)
# Create a logging format
request_file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
request_file_handler.setFormatter(request_file_formatter)
# Add the handlers to the request_logger
request_logger.addHandler(request_file_handler)

# Create a stream handler for console output
request_console_handler = logging.StreamHandler()
request_console_handler.setLevel(logging.INFO)
request_console_handler.setFormatter(request_file_formatter)
request_logger.addHandler(request_console_handler)