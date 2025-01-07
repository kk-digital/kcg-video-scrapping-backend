from typing import List, Optional
import uuid
from datetime import datetime
import pymongo
from pymongo.collection import Collection
from fastapi import HTTPException

from enums import SEARCH_QUERY_STATUS
from schema.search_query_schema import SearchQuerySchema


def list_search_queries(
    collection: Collection,
    offset: int,
    limit: int,
    search_query: Optional[str],
    status: Optional[SEARCH_QUERY_STATUS],
):
    query = (
        {"query": {"$regex": f".*{search_query}.*", "$options": "i"}}
        if search_query
        else {}
    )
    if status:
        query["status"] = status
    return list(
        collection.find(query, {"_id": 0})
        .sort("created_at", pymongo.DESCENDING)
        .skip(offset)
        .limit(limit)
    )


def get_search_query_by_id(collection: Collection, id: str):
    result = collection.find_one({"id": id}, {"_id": 0})

    if result is None:
        raise HTTPException(status_code=404, detail=f"Search query not found. searh_query_id: {id}")

    return dict(result)


def get_search_queries_count(collection: Collection, status: Optional[str]):
    if status is None:
        return collection.count_documents({})

    return collection.count_documents({"status": status})


def add_search_query(collection: Collection, search_query: dict):
    if exists_search_query_by_query(collection, search_query["query"]):
        raise HTTPException(status_code=422, detail=f"Search query already exists. search_query: {search_query['query']}")
    id = uuid.uuid4().hex
    search_query["id"] = id
    search_query = SearchQuerySchema(**search_query).model_dump()
    collection.insert_one(search_query)

    return search_query


def update_search_query(collection: Collection, search_query: dict):
    if not exists_search_query_by_id(collection, search_query["id"]):
        raise HTTPException(status_code=404, detail=f"Search query not found. search_query_id: {search_query['id']}")

    # remove key in which value is None
    search_query = {k: v for k, v in search_query.items() if v is not None}
    # update dml_type nad dml_at
    if search_query.get("status") is not None:
        search_query["dml_at"] = datetime.utcnow()
        search_query["dml_type"] = search_query["status"]

    return collection.update_one({"id": search_query["id"]}, {"$set": search_query})


def delete_search_query(collection: Collection, id: str):
    if not exists_search_query_by_id(collection, id):
        raise HTTPException(status_code=404, detail=f"Search query not found. search_query_id: {id}")

    result = collection.delete_one({"id": id})
    return result.deleted_count


def delete_search_queries(collection: Collection, search_ids: List[str]):
    # Check if all games exist before deleting
    for search_id in search_ids:
        if not exists_search_query_by_id(collection, search_id):
            raise HTTPException(
                status_code=404, detail=f"Video game with id {search_id} not found"
            )

    result = collection.delete_many({"id": {"$in": search_ids}})
    return result.deleted_count


def exists_search_query_by_id(collection: Collection, id: str):
    return collection.find_one({"id": id}) is not None


def exists_search_query_by_query(collection: Collection, query: str):
    return collection.find_one({"query": query}) is not None
