from typing import List, Optional
from fastapi import APIRouter, Query, Request
from controller import search_query_controller
from schema.deleted_count_schema import DeletedCountSchema
from schema.response_schema import ResponseSchema
from schema.search_query_schema import (
    SearchQueryCreateSchema,
    SearchQuerySchema,
    SearchQueryUpdateSchema,
)

router = APIRouter(prefix="/search-queries", tags=["search-queries"])


@router.get(
    "/list-search-queries",
    status_code=200,
    description="Get the list of search queries",
    response_model=ResponseSchema[List[SearchQuerySchema]],
)
async def list_search_queries(
    request: Request,
    offset: int = Query(default=0),
    limit: int = Query(default=20),
):
    search_queries = search_query_controller.list_search_queries(
        request.app.search_query_collection, offset, limit
    )

    return ResponseSchema(success=True, data=search_queries)


@router.get(
    "/get-search-query-by-id",
    status_code=200,
    description="Get an search query by given id",
    response_model=ResponseSchema[SearchQuerySchema],
)
async def get_search_query_by_id(request: Request, id: str = Query()):
    result = search_query_controller.get_search_query_by_id(
        request.app.search_query_collection, id
    )
    return ResponseSchema(success=True, data=result)


@router.get(
    "/get-search-queries-count",
    status_code=200,
    description="Get the count of search queries",
    response_model=ResponseSchema[int],
)
async def get_search_queries_count(
    request: Request,
    status: Optional[str] = Query(default=None),
):
    count = search_query_controller.get_search_queries_count(
        request.app.search_query_collection, status
    )
    return ResponseSchema(success=True, data=count)


@router.post(
    "/add-search-query",
    status_code=200,
    description="Add a search query",
    response_model=ResponseSchema[SearchQuerySchema],
)
async def add_search_query(
    request: Request,
    search_query: SearchQueryCreateSchema,
):
    added_search_query = search_query_controller.add_search_query(
        request.app.search_query_collection, search_query.model_dump()
    )

    return ResponseSchema(success=True, data=added_search_query)


@router.put(
    "/update-search-query",
    status_code=200,
    description="Update a search query with given search id",
    response_model=ResponseSchema[None],
)
async def update_search_query(request: Request, search_query: SearchQueryUpdateSchema):
    search_query_controller.update_search_query(
        request.app.search_query_collection, search_query.model_dump()
    )
    return ResponseSchema(success=True, message="Search query updated successfully")


@router.delete(
    "/delete-search-query",
    status_code=200,
    description="Delete an search query with given search query",
    response_model=ResponseSchema[DeletedCountSchema],
)
def delete_search_query(request: Request, search_query_id: str = Query()):
    deleted_count = search_query_controller.delete_search_query(
        request.app.search_query_collection, id=search_query_id
    )

    return ResponseSchema(
        success=True,
        message="Search query deleted successfully",
        data={"deleted_count": deleted_count},
    )