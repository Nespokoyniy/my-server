from fastapi import FastAPI
from .routers import auth, pages, recurring_tasks, tasks

app = FastAPI()

app.include_router(auth.router)
app.include_router(pages.router)
app.include_router(recurring_tasks.router)
app.include_router(tasks.router)