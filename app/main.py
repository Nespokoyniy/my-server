from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
html = Jinja2Templates(directory="templates")

@app.get("/start", response_class=HTMLResponse)
def start_page(request: Request):
    return html.TemplateResponse(name="index.html", request=request)

@app.get("/login")
def login_page(request: Request):
    return html.TemplateResponse(name="", request=request)