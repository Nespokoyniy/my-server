from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.templating import Jinja2Templates


from .routers import profile, recurring_tasks, tasks, auth, frontend

app = FastAPI(docs_url=None , redoc_url=None)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static") #временно для разработки
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/")
async def root():
    return RedirectResponse(url="/register")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("frontend/static/icons/favicon.ico")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Глобальный обработчик исключений для перехвата 401.
    """
    if exc.status_code == 401 and request.headers.get("HX-Request"):
        # Если это HTMX-запрос и код ошибки 401, возвращаем частичный шаблон.
        return templates.TemplateResponse("errors/401.html", {"request": request}, status_code=401)
    
    # Для всех остальных случаев используем стандартный обработчик.
    return HTMLResponse(content=f"Error: {exc.status_code} - {exc.detail}", status_code=exc.status_code)


app.include_router(profile.router)
app.include_router(auth.router)
app.include_router(recurring_tasks.router)
app.include_router(tasks.router)
app.include_router(frontend.router)