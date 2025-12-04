from functools import lru_cache
from typing import Generator, List, Dict, Callable

import pytest
from fakeredis import FakeRedis, FakeServer
from fastapi.testclient import TestClient

from ..app.core.shortener import Shortener
from ..app.api.dependencies import get_db
from ..app.main import app


@pytest.fixture(scope="session")
def shortener_info() -> Dict:
    shortener = {"mapping": "flksdjlfsjwqoiqepi31209831098dalnlj",
                 "key_length": 8,
                 "key_prefix": "shortener:",
                 "retries": 10}
    return shortener


@pytest.fixture(scope="function")
def db() -> Generator:
    db = FakeRedis(decode_responses=True)
    yield db
    db.close()
    
    
@pytest.fixture(scope="function")
def create_items_from_urls(urls: List[str], db: FakeRedis) -> None:
    shortener = Shortener(db)
    for url in urls:
        shortener.long_to_short(url)
        
        
@pytest.fixture(scope="function")
def fake_db() -> Callable[[None], FakeRedis]:
    """
    Создает и кэширует экземпляр FakeRedis для использования таким же образом, 
    как и внедрение зависимостей в fastapi.
    """
    @lru_cache
    def wrapper() -> FakeRedis:
        db = FakeRedis(decode_responses = True)
        return db
    
    return wrapper


@pytest.fixture(scope="function")
def client(fake_db) -> Generator:
    app.dependency_overrides[get_db] = fake_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides = {}
    
    
@pytest.fixture(scope="function")
def client_db_disconnected() -> Generator:
    server = FakeServer()
    server.connected = False
    db = FakeRedis(server=server)
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides = {}
    