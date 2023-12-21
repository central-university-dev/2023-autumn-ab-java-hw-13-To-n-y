from pydantic import BaseModel


class Task(BaseModel):
    id: int
    list_id: int
    name: str
    description: str
