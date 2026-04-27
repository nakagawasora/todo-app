from pydantic import BaseModel

class TodoCreateRequest(BaseModel):
    title: str
    done: bool = False