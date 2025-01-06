from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enums import INGRESS_VIDEO_STATUS


class IngressVideoBaseSchema(BaseModel):
    video_id: str
    channel_id: Optional[str] = Field(default=None)
    channel_url: Optional[str] = Field(default=None)
    file_hash: str
    file_path: str
    video_url: str
    video_title: str
    video_description: str
    video_resolution: str
    video_extension: str
    video_length: int
    video_filesize: int
    video_frame_rate: int
    video_language: Optional[str]
    game_id: str
    transferred: bool = Field(default=False)
    status: INGRESS_VIDEO_STATUS = Field(default=INGRESS_VIDEO_STATUS.PENDING)
    

class IngressVideoUpdateSchema(IngressVideoBaseSchema):
    video_id: str
    channel_id: Optional[str] = Field(default=None)
    channel_url: Optional[str] = Field(default=None)
    file_hash: Optional[str] = Field(default=None)
    file_path: Optional[str] = Field(default=None)
    video_url: Optional[str] = Field(default=None)
    video_title: Optional[str] = Field(default=None)
    video_description: Optional[str] = Field(default=None)
    video_resolution: Optional[str] = Field(default=None)
    video_extension: Optional[str] = Field(default=None)
    video_length: Optional[int] = Field(default=None)
    video_filesize: Optional[int] = Field(default=None)
    video_frame_rate: Optional[int] = Field(default=None)
    video_language: Optional[str] = Field(default=None)
    transferred: Optional[bool] = Field(default=None)
    status: INGRESS_VIDEO_STATUS = Field(default=None)
    game_id: Optional[str] = Field(default=None)


class IngressVideoCreateSchema(IngressVideoBaseSchema):
    pass


class IngressVideoSchema(IngressVideoBaseSchema):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    dml_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    dml_type: Optional[INGRESS_VIDEO_STATUS] = Field(default=INGRESS_VIDEO_STATUS.PENDING)
