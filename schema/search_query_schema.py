from pydantic import BaseModel, Field
from datetime import datetime

from enums import SEARCH_QUERY_STATUS


class SearchQueryBaseSchema(BaseModel):
    query: str
    game_id: str
    createdAt: datetime = Field(default_factory=datetime.now)
    dmlAt: datetime = Field(default_factory=datetime.now)
    dmlType: SEARCH_QUERY_STATUS = Field(default=SEARCH_QUERY_STATUS.PENDING)


class SearchQueryCreateSchema(SearchQueryBaseSchema):
    pass


class SearchQuerySchema(SearchQueryBaseSchema):
    id: str


class SearchQueryUpdateSchema(SearchQueryBaseSchema):
    id: str
    game_id: str = Field(default=None)
    query: str = Field(default=None)
    createdAt: datetime = Field(default=None)
    dmlAt: datetime = Field(default=None)
    dmlType: SEARCH_QUERY_STATUS = Field(default=None)
