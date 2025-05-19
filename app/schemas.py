from pydantic import BaseModel

class Task(BaseModel):
    name: str
    description: str = ""
    priority: int = 0
    

class RecurTask(Task):
    days: list