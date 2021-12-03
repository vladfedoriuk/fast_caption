import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from state.models import Caption


async def get_caption_object_or_none(
    session: AsyncSession, caption_uuid: uuid.UUID
) -> Optional[Caption]:
    caption_query = await session.execute(
        select(Caption).where(Caption.pk == caption_uuid)
    )
    return caption_query.scalars().first()
