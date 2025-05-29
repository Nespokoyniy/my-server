# import uvicorn
# import os


# def start_server():
#     uvicorn.run(app="app.main:app", host="0.0.0.0", port=8000, reload=True)


# def update():
#     os.system("pip freeze > requirements.txt")


# def alembic_check():
#     os.system('alembic revision --autogenerate -m "new migration"')
#     os.system("alembic upgrade head")


# if __name__ == "__main__":
#     alembic_check()
#     update()
#     start_server()

import uvicorn
import os
import subprocess
import sys


def start_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = True):
    """Запуск сервера с Uvicorn."""
    uvicorn.run(app="app.main:app", host=host, port=port, reload=reload)


def update_requirements():
    """Обновляет requirements.txt, только если есть изменения."""
    print("🔍 Проверка обновлений зависимостей...")
    result = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
    current = result.stdout

    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r") as f:
            existing = f.read()
        if current == existing:
            print("✅ requirements.txt уже актуален.")
            return

    with open("requirements.txt", "w") as f:
        f.write(current)
    print("📦 requirements.txt обновлен.")


def run_migrations():
    """Запуск миграций Alembic (только при явном вызове)."""
    print("🔄 Проверка миграций...")
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("✅ Миграции применены.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка миграций: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Пример раздельного управления
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "start":
            start_server()
        elif command == "migrate":
            run_migrations()
        elif command == "update":
            update_requirements()
        else:
            print("Доступные команды: start, migrate, update")
    else:
        # По умолчанию — просто запуск сервера
        start_server()