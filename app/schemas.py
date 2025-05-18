from pydantic import BaseModel

class Task(BaseModel):
    number: int
    task: str