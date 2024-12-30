import requests
from config import BASE_ENDPOINT_URL
from enums import INGRESS_VIDEO_STATUS, SEARCH_QUERY_STATUS
from utils.logger import download_logger, scrapping_logger


def http_update_ingress_video(data):
    url = f"{BASE_ENDPOINT_URL}/api/v1/ingress-videos/update-ingress-video"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error in http_update_ingress", response.text)
            return None
    except Exception as e:
        download_logger("Error in http_update_ingress: %s", e)
        return None


def http_get_pending_ingress_videos(offset: int = 0, limit: int = 1):
    url = f"{BASE_ENDPOINT_URL}/api/v1/ingress-videos/list-ingress-videos?status={INGRESS_VIDEO_STATUS.PENDING}&offset={offset}&limit={limit}"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["data"]
        download_logger("Error in http_get_pending_ingress_videos: %s", response.text)
        return None
    except Exception as e:
        download_logger("Error in http_get_pending_ingress_videos: %s", e)
        return None


def http_get_pending_query(offset: int = 0, limit: int = 1):
    url = f"{BASE_ENDPOINT_URL}/api/v1/search-queries/list-search-queries?status={SEARCH_QUERY_STATUS.PENDING}&offset={offset}&limit={limit}"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["data"]
        scrapping_logger("Error in http_get_pending_query: %s", response.text)
        return None
    except Exception as e:
        scrapping_logger("Error in http_get_pending_query: %s", e)
        return None
