import uuid
from typing import Awaitable, Callable, Optional, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from state import AsyncSessionContext
from state.models import Caption


async def get_caption_object_or_none(session: AsyncSession, caption_uuid: uuid.UUID) -> Optional[Caption]:
    caption_query = await session.execute(select(Caption).where(Caption.pk == caption_uuid))
    return caption_query.scalars().first()


T = TypeVar("T")


def with_session(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    async def inner(*args, **kwargs) -> T:
        async with AsyncSessionContext() as session:
            async with session.begin():
                result: T = await func(session, *args, **kwargs)
                await session.commit()
                return result

    return inner
