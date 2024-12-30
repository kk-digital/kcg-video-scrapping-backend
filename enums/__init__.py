from enum import Enum


class INGRESS_VIDEO_STATUS(str, Enum):
    PENDING = "pending"
    DOWNLOADINDG = "downloading"
    DOWNLOADED = "downloaded"
    FAILED = "failed"
    CANCELED = "canceled"


class SEARCH_QUERY_STATUS(str, Enum):
    PENDING = "pending"
    EXTRACTING = "extracting"
    EXTRACTED = "extracted"
    FAILED = "failed"
    CANCELED = "canceled"
