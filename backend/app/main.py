from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import profile, recurring_tasks, tasks, auth, frontend

app = FastAPI(docs_url=None , redoc_url=None)

app.include_router(profile.router)
app.include_router(auth.router)
app.include_router(recurring_tasks.router)
app.include_router(tasks.router)
app.include_router(frontend.router)