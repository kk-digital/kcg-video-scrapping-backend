from typing import List
from pydantic import BaseModel, Field
from datetime import datetime

from enums import SEARCH_QUERY_STATUS


class SearchQueryBaseSchema(BaseModel):
    query: str
    game_id: str
    status: SEARCH_QUERY_STATUS = Field(default=SEARCH_QUERY_STATUS.PENDING)
    dmlAt: datetime = Field(default_factory=datetime.utcnow)
    dmlType: SEARCH_QUERY_STATUS = Field(default=SEARCH_QUERY_STATUS.PENDING)


class SearchQueryCreateSchema(SearchQueryBaseSchema):
    pass


class SearchQuerySchema(SearchQueryBaseSchema):
    id: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)


class SearchQueryUpdateSchema(SearchQueryBaseSchema):
    id: str
    game_id: str = Field(default=None)
    query: str = Field(default=None)
    status: SEARCH_QUERY_STATUS = Field(default=SEARCH_QUERY_STATUS.PENDING)
    dmlAt: datetime = Field(default=None)
    dmlType: SEARCH_QUERY_STATUS = Field(default=None)


class QueryIdsRequest(BaseModel):
    ids: List[str]
