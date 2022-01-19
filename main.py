import uuid

import sqlalchemy.exc
from fastapi import FastAPI, BackgroundTasks, status, Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from models import ImageData
from state import get_session
from state.models import Caption, CaptionBase
from tasks.model import get_model
from tasks.pipeline import process_image

router = APIRouter(
    prefix="/caption",
    tags=["caption"],
)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    get_model()


@router.post(
    "/enquire/",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=CaptionBase,
)
async def enquire_caption(
    image_data: ImageData,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    caption_obj = Caption(image_url=image_data.url)
    session.add(caption_obj)
    await session.commit()
    await session.refresh(caption_obj)
    background_tasks.add_task(process_image, image_data.url, caption_obj.pk)
    return JSONResponse(
        jsonable_encoder(caption_obj), status_code=status.HTTP_202_ACCEPTED
    )


@router.get("/retrieve/", status_code=status.HTTP_200_OK, response_model=Caption)
async def retrieve_caption(
    caption_uuid: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    try:
        caption_obj = await session.execute(
            select(Caption).where(Caption.pk == caption_uuid)
        )
        caption_obj = caption_obj.scalars().one()
    except (sqlalchemy.exc.MultipleResultsFound, sqlalchemy.exc.NoResultFound) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return JSONResponse(jsonable_encoder(caption_obj), status_code=status.HTTP_200_OK)


app.include_router(router)
