from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def main():
    
    html = Jinja2Templates("templates")
    return html.TemplateResponse(name="index.html")