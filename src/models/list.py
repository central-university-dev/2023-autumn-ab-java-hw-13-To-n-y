from pydantic import BaseModel


class List(BaseModel):
    id: int
    name: str
    cnt: int = 0
    user_id: int
