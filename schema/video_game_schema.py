from typing import Optional
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
    pass
