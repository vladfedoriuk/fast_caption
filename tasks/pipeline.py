import uuid

import requests
from requests import Response, RequestException
from PIL import Image
from io import BytesIO
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import select

from state import engine, AsyncSessionContext
from state.models import Caption


def generate_caption(image: np.array) -> str:
    return "Mock caption"


async def fetch_image(image_url: str, caption_uuid: uuid.UUID):
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    try:
        response: Response = requests.get(url=image_url)
        response.raise_for_status()
        with Image.open(BytesIO(response.content)) as img:
            caption = generate_caption(np.asarray(img))
            async with AsyncSessionContext() as session:
                caption_query = await session.execute(
                    select(Caption).where(Caption.pk == caption_uuid)
                )
                caption_obj: Caption = caption_query.scalars().first()
                if caption_obj:
                    caption_obj.caption = caption
                    caption_obj.fetch_status = response.status_code
                    session.add(caption_obj)
                await session.commit()
    except RequestException:
        pass
        # TODO: add handling the invalid image url / download errors
