from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
html = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def base_page(request: Request):
    return html.TemplateResponse(name="index.html", request=request)