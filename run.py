import uvicorn
import os
import sys

def start_server():
    uvicorn.run(app="app.main:app", host="0.0.0.0", port=8000, reload=True)

def update():
    os.system("pip freeze > requirements.txt")

if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "start":
        start_server()
    if sys.argv[1] == "update":
        update()
    else:
        print(f"command {sys.argv[1]} does not exist")
