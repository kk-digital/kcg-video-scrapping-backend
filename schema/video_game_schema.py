from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class VideoGameBaseSchema(BaseModel):
    game_id: str
    title: str
    description: str


class VideoGameCreateSchema(VideoGameBaseSchema):
    pass


class VideoGameUpdateSchema(BaseModel):
    game_id: str
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)


class VideoGameSchema(VideoGameBaseSchema):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    pass


class VideoGameIdsRequest(BaseModel):
    ids: List[str]
