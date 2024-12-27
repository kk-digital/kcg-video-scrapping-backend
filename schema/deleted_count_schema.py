from pydantic import BaseModel


class DeletedCountSchema(BaseModel):
    deleted_count: int
