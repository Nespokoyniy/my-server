from fastapi import FastAPI

from .routers import pages, recurring_tasks, tasks, users, auth

app = FastAPI(docs_url=False, redoc_url=False)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(pages.router)
app.include_router(recurring_tasks.router)
app.include_router(tasks.router)