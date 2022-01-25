import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from state.models import Caption

pytestmark = pytest.mark.anyio


@pytest.fixture()
async def caption_obj(db_session: AsyncSession) -> Caption:
    caption_obj = Caption(image_url="http://test_url.jpeg")
    db_session.add(caption_obj)
    await db_session.commit()
    await db_session.refresh(caption_obj)
    return caption_obj


async def test_enquire_caption(app_with_db, async_client, mocker):
    mocker.patch("fastapi.BackgroundTasks.add_task")
    response = await async_client.post("/caption/enquire/", json={"url": "http://test.jpg"})
    assert response.status_code == status.HTTP_202_ACCEPTED


async def test_retrieve_caption(app_with_db, async_client, caption_obj):
    response = await async_client.get("/caption/retrieve/", params={"caption_uuid": caption_obj.pk})
    assert response.status_code == status.HTTP_200_OK


async def test_retrieve_caption_wrong_caption_uuid(app_with_db, async_client):
    response = await async_client.get("/caption/retrieve/", params={"caption_uuid": uuid.uuid4()})
    assert response.status_code == status.HTTP_404_NOT_FOUND
