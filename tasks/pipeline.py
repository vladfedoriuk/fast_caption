import uuid

import requests
from requests import Response, RequestException
from PIL import Image
from io import BytesIO
import numpy as np

from state import AsyncSessionContext
from state.models import Caption
from tasks.utils import get_caption_object_or_none


def generate_caption(image: np.array) -> str:
    return "Mock caption"


async def process_image(image_url: str, caption_uuid: uuid.UUID):
    try:
        response: Response = requests.get(url=image_url)
        response.raise_for_status()
        with Image.open(BytesIO(response.content)) as img:
            caption = generate_caption(np.asarray(img))
            async with AsyncSessionContext() as session:
                async with session.begin():
                    caption_obj: Caption = await get_caption_object_or_none(
                        session, caption_uuid
                    )
                    if caption_obj:
                        caption_obj.caption = caption
                        caption_obj.fetch_status = response.status_code
                        session.add(caption_obj)
                        await session.commit()
    except RequestException as e:
        async with AsyncSessionContext() as session:
            async with session.begin():
                caption_obj: Caption = await get_caption_object_or_none(
                    session, caption_uuid
                )
                if caption_obj:
                    caption_obj.fetch_status = e.response.status_code
                    caption_obj.fetch_error = str(e)
                    session.add(caption_obj)
                    await session.commit()
