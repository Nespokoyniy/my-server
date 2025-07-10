from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import pytest
from sqlalchemy import delete
from fastapi.testclient import TestClient
from backend.app.database import models
from backend.app.database.database import get_db
from backend.app.main import app
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from backend.app.config import settings as ss
from backend.app.services.auth import login, register
from backend.app.services.tasks import create_task
from backend.app.services.users import delete_user
from backend.app.utils.dependencies import get_current_user
from backend.app.utils.hash import hash_pwd
from backend.app.validation import schemas


@pytest.fixture
def test_db():
    engine = create_engine(ss.DB_URL)
    SessionLocal = sessionmaker(autoflush=False, bind=engine)
    test_db = SessionLocal()
    try:
        print("XXXXXXXXXXXXXXXXXXXXXXXXx")
        yield test_db
    finally:
        test_db.execute(delete(models.Task))
        test_db.execute(delete(models.User))
        test_db.execute(delete(models.RecurringTask))
        test_db.commit()
        test_db.close()
        engine.dispose()


@pytest.fixture
def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def register(test_db: Session):
    test_db.execute(delete(models.User).where(models.User.name == "example"))
    test_db.commit()

    user = models.User(
        name="example",
        email="example@gmail.com",
        password=hash_pwd("example123"),
    )
    test_db.add(user)
    test_db.commit()


@pytest.fixture
def token(register, test_db: Session):
    token = login(
        OAuth2PasswordRequestForm(username="example", password="example123"), test_db
    )
    return {"Authorization": f"Bearer {token['access_token']}"}


@pytest.fixture
def create_tasks(token, test_db):
    user_id = get_current_user(token["Authorization"].split()[1], test_db)
    for num in range(1, 4):
        create_task(
            schemas.TaskWithOwner(
                name=f"task {num}",
                description=f"desc {num}",
                priority=num,
                owner=user_id,
            ),
            test_db,
        )
    test_db.commit()
    yield
