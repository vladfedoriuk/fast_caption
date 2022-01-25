import asyncio
import uuid
from functools import partial
from io import BytesIO
from typing import Optional

import httpx
import numpy as np
from httpx import HTTPStatusError, Response
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from state.models import Caption
from tasks.model import get_model
from tasks.model.search import beam_search
from tasks.model.utils import preprocess_image
from tasks.utils import get_caption_object_or_none, with_session


@with_session
async def update_caption(
    session: AsyncSession,
    caption_uuid: uuid.UUID,
    fetch_status: int = status.HTTP_202_ACCEPTED,
    fetch_error: str = "",
    caption: str = "",
) -> None:
    caption_obj: Optional[Caption] = await get_caption_object_or_none(session, caption_uuid)
    if caption_obj is not None:
        caption_obj.fetch_status = fetch_status
        caption_obj.fetch_error = fetch_error
        caption_obj.caption = caption
        session.add(caption_obj)


def generate_caption(image: Image) -> str:
    feature_extractor, attention_model, encoder_model, decoder_model = get_model()
    image = preprocess_image(image)
    image = feature_extractor(np.array([image]))[0]
    _, _, c = image.shape
    image = np.reshape(image, (-1, c))
    return beam_search(encoder_model, decoder_model, image)


async def process_image(image_url: str, caption_uuid: uuid.UUID):
    try:
        async with httpx.AsyncClient() as client:
            response: Response = await client.get(url=image_url)
            response.raise_for_status()
            with Image.open(BytesIO(response.content)) as image:
                loop = asyncio.get_running_loop()
                caption = await loop.run_in_executor(None, partial(generate_caption, image))
                await update_caption(caption_uuid, fetch_status=response.status_code, caption=caption)
    except HTTPStatusError as e:
        await update_caption(caption_uuid, fetch_status=e.response.status_code, fetch_error=str(e))
