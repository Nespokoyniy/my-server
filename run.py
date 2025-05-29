import uvicorn
import os
import sys


def start_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = True):
    uvicorn.run(app="app.main:app", host=host, port=port, reload=reload)


def requirements_update():
    os.system("pip freeze > requirements.txt")


def alembic_upgrade():
    os.system('alembic revision --autogenerate -m "new migration"')
    os.system("alembic upgrade head")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "alembic":
        alembic_upgrade()
    if len(sys.argv) > 1 and sys.argv[1] == "req":
        requirements_update()
    start_server()