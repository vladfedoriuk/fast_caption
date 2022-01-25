import uuid

from sqlmodel import Field, SQLModel
from starlette import status


class CaptionBase(SQLModel):
    pk: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False)

    class Config:
        orm_mode = True


class Caption(CaptionBase, table=True):
    image_url: str = Field(
        default="",
        nullable=False,
        max_length=255,
        description="The url from which the image should be downloaded",
    )
    caption: str = Field(
        default="",
        nullable=False,
        max_length=255,
        description="A caption generated by a model",
    )
    fetch_status: int = Field(
        default=status.HTTP_202_ACCEPTED,
        description="The http status received when fetching the image.",
    )
    fetch_error: str = Field(
        default="",
        nullable=False,
        max_length=255,
        description="The http error occurred while fetching the image.",
    )

    class Config:
        orm_mode = True
