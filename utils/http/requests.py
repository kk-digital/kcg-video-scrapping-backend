import requests
from config import BASE_ENDPOINT_URL
from enums import INGRESS_VIDEO_STATUS


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
        print("Error in http_update_ingress", e)
        return None


def http_get_pending_ingress_videos():
    url = f"{BASE_ENDPOINT_URL}/api/v1/ingress-videos/list-ingress-videos?status={INGRESS_VIDEO_STATUS.PENDING}"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["data"]
        print("Error in http_get_pending_ingress_videos", response.text)
        return None
    except Exception as e:
        print("Error in http_get_pending_ingress_videos", e)
        return None
