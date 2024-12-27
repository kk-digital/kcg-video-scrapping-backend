from typing import Optional
import uuid
from datetime import datetime
from pymongo.collection import Collection
from fastapi import HTTPException


def list_search_queries(collection: Collection, offset: int, limit: int):
    return list(collection.find({}, {"_id": 0}).skip(offset).limit(limit))


def get_search_query_by_id(collection: Collection, id: str):
    result = collection.find_one({"id": id}, {"_id": 0})

    if result is None:
        raise HTTPException(status_code=404, detail="Search query not found")

    return dict(result)


def get_search_queries_count(collection: Collection, status: Optional[str]):
    if status is None:
        return collection.count_documents({})

    return collection.count_documents({"status": status})


def add_search_query(collection: Collection, search_query: dict):
    if exists_search_query_by_query(collection, search_query["query"]):
        raise HTTPException(status_code=422, detail="Search query already exists")
    id = uuid.uuid4().hex
    search_query["id"] = id
    collection.insert_one(search_query)

    return search_query


def update_search_query(collection: Collection, search_query: dict):
    if not exists_search_query_by_id(collection, search_query["id"]):
        raise HTTPException(status_code=404, detail="Search query not found")

    # remove key in which value is None
    search_query = {k: v for k, v in search_query.items() if v is not None}

    return collection.update_one({"id": search_query["id"]}, {"$set": search_query})


def delete_search_query(collection: Collection, id: str):
    if not exists_search_query_by_id(collection, id):
        raise HTTPException(status_code=404, detail="Search query not found")

    result = collection.delete_one({"id": id})
    return result.deleted_count


def exists_search_query_by_id(collection: Collection, id: str):
    return collection.find_one({"id": id}) is not None


def exists_search_query_by_query(collection: Collection, query: str):
    return collection.find_one({"query": query}) is not None
