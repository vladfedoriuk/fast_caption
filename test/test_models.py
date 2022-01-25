import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from state.models import Caption

pytestmark = pytest.mark.anyio


async def test_create_caption(db_session: AsyncSession) -> None:
    caption_obj = Caption(image_url="test_url.jpeg")
    db_session.add(caption_obj)
    await db_session.commit()
    await db_session.refresh(caption_obj)
    assert caption_obj.pk is not None
    assert caption_obj.image_url == "test_url.jpeg"
    assert caption_obj.fetch_status == status.HTTP_202_ACCEPTED
