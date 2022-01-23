import uuid
from typing import Optional, Awaitable, TypeVar, Callable
from typing_extensions import ParamSpec, Concatenate

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from state import AsyncSessionContext
from state.models import Caption


async def get_caption_object_or_none(
    session: AsyncSession, caption_uuid: uuid.UUID
) -> Optional[Caption]:
    caption_query = await session.execute(
        select(Caption).where(Caption.pk == caption_uuid)
    )
    return caption_query.scalars().first()


P = ParamSpec("P")
T = TypeVar("T")


def with_session(
    func: Callable[[Concatenate[AsyncSession, P]], Awaitable[T]]
) -> Callable[[Concatenate[AsyncSession, P]], Awaitable[T]]:
    async def inner(*args: P.args, **kwargs: P.kwargs) -> T:
        async with AsyncSessionContext() as session:
            async with session.begin():
                result: T = await func(session, *args, **kwargs)
                await session.commit()
                return result

    return inner
