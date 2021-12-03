from pydantic import BaseModel, HttpUrl


class ImageData(BaseModel):
    url: HttpUrl
