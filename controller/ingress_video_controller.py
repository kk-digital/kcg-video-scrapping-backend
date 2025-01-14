from typing import Optional, List
from datetime import datetime
from fastapi import HTTPException
from pymongo.collection import Collection

from schema.ingress_video_schema import IngressVideoSchema


def get_list_ingress_videos(
    collection: Collection,
    offset: int,
    limit: int,
    status: Optional[str],
    title: Optional[str],
):
    query = {}
    if status:
        query = {"status": status}
    if title:
        query["video_title"] = {"$regex": f".*{title}.*", "$options": "i"}

    return list(collection.find(query, {"_id": 0}).skip(offset).limit(limit))


def get_ingress_video_by_video_id(collection: Collection, video_id: str):
    result = collection.find_one({"video_id": video_id}, {"_id": 0})

    if result is None:
        raise HTTPException(status_code=404, detail=f"Ingress video not found. video_id: {video_id}")

    return dict(result)

def check_existence(collection: Collection, video_ids: List[str]):
    result = list(collection.find({"video_id": {"$in": video_ids}}, {"_id": 0}))
    existed_video_ids = [video["video_id"] for video in result]
    unexisted_video_ids = list(set(video_ids) - set(existed_video_ids))
    return {"existed_video_ids": existed_video_ids, "unexisted_video_ids": unexisted_video_ids}


def add_ingress_video(collection: Collection, ingress_video: dict):
    if exists_ingress_video(collection, ingress_video["video_id"]):
        raise HTTPException(status_code=422, detail=f"Ingress video already exists. video_id: {ingress_video['video_id']}")
    ingress_video = IngressVideoSchema(**ingress_video).model_dump()

    collection.insert_one(ingress_video)

    return ingress_video


def update_ingress_video(collection: Collection, ingress_video: dict):
    if not exists_ingress_video(collection, ingress_video["video_id"]):
        raise HTTPException(status_code=404, detail=f"Ingress video not found. video_id: {ingress_video['video_id']}")

    # remove key in which value is None
    ingress_video = {k: v for k, v in ingress_video.items() if v is not None}
    # update dml_type nad dml_at
    if ingress_video.get("status") is not None:
        ingress_video["dml_at"] = datetime.utcnow()
        ingress_video["dml_type"] = ingress_video["status"]

        if ingress_video.get("status") == "downloading":
            ingress_video["started_at"] = datetime.utcnow()
            ingress_video["elapsed_time"] = 0
    
    return collection.update_one(
        {"video_id": ingress_video["video_id"]}, {"$set": ingress_video}
    )


def delete_ingress_video(collection: Collection, video_id: str):
    if not exists_ingress_video(collection, video_id):
        raise HTTPException(status_code=404, detail=f"Ingress video not found. video_id: {video_id}")

    return collection.delete_one({"video_id": video_id})


def exists_ingress_video(collection: Collection, video_id: str):
    return collection.find_one({"video_id": video_id}) is not None


def get_ingress_videos_count(collection: Collection, status: Optional[str] = None):
    if status is None:
        return collection.count_documents({})
    else:
        return collection.count_documents({"status": status})
       