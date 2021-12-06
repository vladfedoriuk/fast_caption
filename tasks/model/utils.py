import pickle
from functools import lru_cache
from pathlib import Path

from PIL import Image
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing.image import img_to_array
from keras_preprocessing.text import Tokenizer
from tensorflow import Tensor

from .config import Configuration, get_model_configuration

model_conf: Configuration = get_model_configuration()
IMAGE_WIDTH, IMAGE_HEIGHT = model_conf.IMAGE_SIZE.get("vgg16")

SERIALIZED_DATA_PATH: Path = Path(__file__).parent / "pretrained"


def image_crop_center(img: Image) -> Image:
    w, h = model_conf.IMAGE_SIZE.get("vgg16")
    img_width, img_height = img.size
    if img_width < w or img_height < h:
        return img.resize(w, h)
    left, right = (img_width - w) / 2, (img_width + w) / 2
    top, bottom = (img_height - h) / 2, (img_height + h) / 2
    left, top = round(max(0, left)), round(max(0, top))
    right, bottom = round(min(img_width - 0, right)), round(min(img_height - 0, bottom))
    return img.crop((left, top, right, bottom)).resize((w, h))


def preprocess_image(image: Image) -> Tensor:
    image = image_crop_center(image)
    image = img_to_array(image)
    image = preprocess_input(image)
    return image


@lru_cache
def load_tokenizer() -> Tokenizer:
    with open(SERIALIZED_DATA_PATH / "tokenizer.pickle", "rb") as handle:
        return pickle.load(handle)
