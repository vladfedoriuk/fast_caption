import asyncio
from collections.abc import Callable

from pytest_mock import mocker
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
    return 'asyncio'


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
async def db_session() -> AsyncSession:
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
    async def _override_get_session():
        yield db_session

    return _override_get_session


@pytest.fixture()
def app(override_get_session: Callable, mocker) -> FastAPI:
    from state import get_session
    from main import app
    app.dependency_overrides[get_session] = override_get_session
    return app


@pytest.fixture()
async def async_client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
