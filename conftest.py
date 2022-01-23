import asyncio
from collections.abc import Callable

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from typing import AsyncGenerator, Generator

import pytest
from fastapi import FastAPI

from config import get_settings
from httpx import AsyncClient


@pytest.fixture()
def anyio_backend():
    """Use asyncio as a default backend"""
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def get_model(mocker) -> Generator:
    """Mock the model loading and the returned models"""
    mocked_get_model = mocker.patch(
        "tasks.model.pretrained.get_model", mocker.MagicMock
    )
    feature_extractor_mock = mocker.MagicMock()
    attention_mock = mocker.MagicMock()
    encoder_mock = mocker.MagicMock()
    decoder_mock = mocker.MagicMock()
    mocked_get_model.returned_value = (
        feature_extractor_mock,
        attention_mock,
        encoder_mock,
        decoder_mock,
    )
    yield mocked_get_model


@pytest.fixture()
async def db_session() -> AsyncSession:
    """Mock the database session"""
    settings = get_settings()
    engine = create_async_engine(settings.postgres_url, echo=True, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
        async_session = sessionmaker(conn, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture()
def override_get_session(db_session: AsyncSession) -> Callable:
    """The session dependency override"""

    async def _override_get_session():
        yield db_session

    return _override_get_session


@pytest.fixture()
def app() -> FastAPI:
    """Creates an app without loading the model on setup and without database connection"""
    from main import router

    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture()
def app_with_db(override_get_session: Callable, app) -> FastAPI:
    """Creates an app without loading the model on setup and with database connection"""
    from state import get_session

    app.dependency_overrides[get_session] = override_get_session
    return app


@pytest.fixture()
async def async_client(app: FastAPI) -> AsyncGenerator:
    """Async HTTP client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
