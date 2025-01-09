import requests
from config import BASE_ENDPOINT_URL
from enums import INGRESS_VIDEO_STATUS, SEARCH_QUERY_STATUS
from utils.logger import request_logger

def http_add_ingress_video(data):
    url = f"{BASE_ENDPOINT_URL}/api/v1/ingress-videos/add-ingress-video"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()["data"]
        request_logger.error("Error in http_add_ingress: %s", response.text)
        return None
    except Exception as e:
        request_logger.error("Error in http_add_ingress: %s", e)
        return None

def http_update_ingress_video(data):
    url = f"{BASE_ENDPOINT_URL}/api/v1/ingress-videos/update-ingress-video"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            request_logger.error("Error in http_update_ingress: %s", response.text)
            return None
    except Exception as e:
        request_logger.error("Error in http_update_ingress: %s", e)
        return None


def http_get_pending_ingress_videos(offset: int = 0, limit: int = 1):
    url = f"{BASE_ENDPOINT_URL}/api/v1/ingress-videos/list-ingress-videos?status={INGRESS_VIDEO_STATUS.PENDING}&offset={offset}&limit={limit}"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["data"]
        request_logger.error("Error in http_get_pending_ingress_videos: %s", response.text)
        return None
    except Exception as e:
        request_logger.error("Error in http_get_pending_ingress_videos: %s", e)
        return None

def http_update_query(data):
    url = f"{BASE_ENDPOINT_URL}/api/v1/search-queries/update-search-query"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["data"]
        request_logger.error("Error in http_update_query: %s", response.text)
        return None
    except Exception as e:
        request_logger.error("Error in http_update_query: %s", e)
        return None


def http_get_pending_query(offset: int = 0, limit: int = 10):
    url = f"{BASE_ENDPOINT_URL}/api/v1/search-queries/list-search-queries?status={SEARCH_QUERY_STATUS.PENDING}&offset={offset}&limit={limit}"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["data"]
        request_logger.error("Error in http_get_pending_query: %s", response.text)
        return None
    except Exception as e:
        request_logger.error("Error in http_get_pending_query: %s", e)
        return None

def http_get_extracting_query(offset: int = 0, limit: int = 10):
    url = f"{BASE_ENDPOINT_URL}/api/v1/search-queries/list-search-queries?status={SEARCH_QUERY_STATUS.EXTRACTING}&offset={offset}&limit={limit}"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["data"]
        request_logger.error("Error in http_get_pending_query: %s", response.text)
        return None
    except Exception as e:
        request_logger.error("Error in http_get_pending_query: %s", e)
        return None
    
def http_check_existence_videos(video_ids: list):
    url = f"{BASE_ENDPOINT_URL}/api/v1/ingress-videos/check-existence"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json={"ids": video_ids}, headers=headers)
        if response.status_code == 200:
            return response.json()["data"]
        request_logger.error("Error in http_check_existence_videos: %s", response.text)
        return None
    except Exception as e:
        request_logger.error("Error in http_check_existence_videos: %s", e)
        return None