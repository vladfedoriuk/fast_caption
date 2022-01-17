import pytest

pytestmark = pytest.mark.anyio


async def test_enquire_caption(async_client, mocker):
    mocker.patch("fastapi.BackgroundTasks.add_task")
    response = await async_client.post("/enquire-caption/", json={"url": "http://test.jpg"})
    assert response.status_code == 202


