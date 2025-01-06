from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from enums import SEARCH_QUERY_STATUS


class SearchQueryBaseSchema(BaseModel):
    query: str
    game_id: str
    status: SEARCH_QUERY_STATUS = Field(default=SEARCH_QUERY_STATUS.PENDING)


class SearchQueryCreateSchema(SearchQueryBaseSchema):
    pass


class SearchQuerySchema(SearchQueryBaseSchema):
    id: str
    dml_at: datetime = Field(default_factory=datetime.utcnow)
    dml_type: SEARCH_QUERY_STATUS = Field(default=SEARCH_QUERY_STATUS.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SearchQueryUpdateSchema(SearchQueryBaseSchema):
    id: str
    game_id: Optional[str] = Field(default=None)
    query: Optional[str] = Field(default=None)
    status: Optional[SEARCH_QUERY_STATUS] = Field(default=None)


class QueryIdsRequest(BaseModel):
    ids: List[str]
