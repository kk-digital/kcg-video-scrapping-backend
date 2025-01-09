from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from enums import SEARCH_QUERY_STATUS


class SearchQueryBaseSchema(BaseModel):
    query: str
    game_id: str
    status: SEARCH_QUERY_STATUS = Field(default=SEARCH_QUERY_STATUS.PENDING)
    total_video_count: int = Field(default=0) # Total count of all extracted video urls from search query
    processed_video_count: int = Field(default=0) # Count of processed video urls from search query
    new_video_count: int = Field(default=0) # Count of unexisted video urls from search query in db

class SearchQueryCreateSchema(SearchQueryBaseSchema):
    pass


class SearchQueryUpdateSchema(BaseModel):
    id: str
    game_id: Optional[str] = Field(default=None)
    query: Optional[str] = Field(default=None)
    status: Optional[SEARCH_QUERY_STATUS] = Field(default=None)
    total_video_count: int = Field(default=None) # Total count of all extracted video urls from search query
    processed_video_count: int = Field(default=None) # Count of processed video urls from search query
    new_video_count: int = Field(default=None) # Count of unexisted video urls from search query in db


class SearchQuerySchema(SearchQueryBaseSchema):
    id: str
    dml_at: datetime = Field(default_factory=datetime.utcnow)
    dml_type: SEARCH_QUERY_STATUS = Field(default=SEARCH_QUERY_STATUS.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class QueryIdsRequest(BaseModel):
    ids: List[str]
