from typing import Optional
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
        raise HTTPException(status_code=404, detail="Ingress video not found")

    return dict(result)


def add_ingress_video(collection: Collection, ingress_video: dict):
    if exists_ingress_video(collection, ingress_video["video_id"]):
        raise HTTPException(status_code=422, detail="Ingress video already exists")
    ingress_video = IngressVideoSchema(**ingress_video).model_dump()

    collection.insert_one(ingress_video)

    return ingress_video


def update_ingress_video(collection: Collection, ingress_video: dict):
    if not exists_ingress_video(collection, ingress_video["video_id"]):
        raise HTTPException(status_code=404, detail="Ingress video not found")

    # remove key in which value is None
    ingress_video = {k: v for k, v in ingress_video.items() if v is not None}

    return collection.update_one(
        {"video_id": ingress_video["video_id"]}, {"$set": ingress_video}
    )


def delete_ingress_video(collection: Collection, video_id: str):
    if not exists_ingress_video(collection, video_id):
        raise HTTPException(status_code=404, detail="Ingress video not found")

    return collection.delete_one({"video_id": video_id})


def exists_ingress_video(collection: Collection, video_id: str):
    return collection.find_one({"video_id": video_id}) is not None


def get_ingress_videos_count(collection: Collection, status: Optional[str] = None):
    if status is None:
        return collection.count_documents({})
    else:
        return collection.count_documents({"status": status})
