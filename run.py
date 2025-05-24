import uvicorn
import sys
import os


def start_server():
    uvicorn.run(app="app.main:app", host="0.0.0.0", port=8000, reload=True)


def update():
    os.system("pip freeze > requirements.txt")


if __name__ == "__main__":
    update()
    start_server()