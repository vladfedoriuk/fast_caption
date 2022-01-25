from functools import lru_cache
from typing import Tuple

import numpy as np
import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from tensorflow.keras import Model
from tensorflow.keras.applications import VGG16

from tasks.model.attention import Attention
from tasks.model.config import get_model_configuration
from tasks.model.decoder import Decoder
from tasks.model.encoder import Encoder
from tasks.model.utils import SERIALIZED_DATA_PATH, load_tokenizer

model_config = get_model_configuration()


__all__ = ("get_model",)


@lru_cache
def get_model() -> Tuple[Model, Attention, Encoder, Decoder]:
    cnn = VGG16(include_top=False, weights="imagenet")
    last_layer = cnn.layers[-1]
    feature_extractor = Model(inputs=cnn.input, outputs=last_layer.output)

    attention_model = Attention(model_config.HIDDEN_DIM)
    encoder_model = Encoder()
    decoder_model = Decoder(attention_model)

    def init():
        tokenizer: Tokenizer = load_tokenizer()
        word_idx = tokenizer.word_index
        input_image_features = np.zeros(model_config.CNN_OUTPUT.get("vgg16"))
        _, _, c = input_image_features.shape
        input_image_features = np.reshape(input_image_features, (-1, c))
        image_features = encoder_model(np.expand_dims(input_image_features, axis=0), training=False)
        decoder_input = tf.expand_dims(np.array([word_idx["<start>"]]), axis=1)
        hidden = tf.zeros((1, model_config.HIDDEN_DIM))
        decoder_model(decoder_input, image_features, hidden, training=False)

    init()

    encoder_model.load_weights(SERIALIZED_DATA_PATH / "encoder.h5")
    decoder_model.load_weights(SERIALIZED_DATA_PATH / "decoder.h5")
    attention_model.load_weights(SERIALIZED_DATA_PATH / "attention.h5")

    return feature_extractor, attention_model, encoder_model, decoder_model
