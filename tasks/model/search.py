import heapq
from contextlib import suppress
from dataclasses import dataclass
from functools import total_ordering
from operator import attrgetter, itemgetter
from typing import List

import numpy as np
import tensorflow as tf
from keras import Model
from keras_preprocessing.text import Tokenizer

from tasks.model.config import get_model_configuration
from tasks.model.utils import load_tokenizer

model_config = get_model_configuration()


@total_ordering
@dataclass(order=False)
class Caption:
    prob: float
    tokens: List[str]
    hidden_state: tf.Tensor

    def __eq__(self, other):
        return self.prob == other.prob

    def __lt__(self, other):
        return self.prob < other.prob


def beam_search(encoder: Model, decoder: Model, image: np.ndarray, beam_size: int = 3) -> str:  # type: ignore
    tokenizer: Tokenizer = load_tokenizer()

    word_idx = tokenizer.word_index
    idx_word = tokenizer.index_word

    hidden = tf.zeros((1, model_config.HIDDEN_DIM))
    print(np.expand_dims(image, axis=0).shape)
    image_features = encoder(np.expand_dims(image, axis=0), training=False)
    decoder_input = tf.expand_dims(np.array([word_idx["<start>"]]), axis=1)

    captions: List[Caption] = []
    predictions, hidden, _ = decoder(decoder_input, image_features, hidden, training=False)
    predicted_ids = np.argsort(predictions[0])[-beam_size:]
    for idx in reversed(predicted_ids):
        heapq.heappush(
            captions,
            Caption(predictions[0][idx].numpy(), [idx_word[idx]], tf.identity(hidden)),
        )
    for _ in range(model_config.MAX_SEQ_LEN - 1):
        new_captions = []
        for caption in captions:
            decoder_input = tf.expand_dims(np.array([word_idx[caption.tokens[-1]]]), axis=1)
            hidden = caption.hidden_state
            predictions, hidden, _ = decoder(decoder_input, image_features, hidden, training=False)
            predicted_ids = np.argsort(predictions[0])[-beam_size:]
            for idx in reversed(predicted_ids):
                new_captions.append(
                    Caption(
                        caption.prob + predictions[0][idx].numpy(),
                        caption.tokens + [idx_word[idx]],
                        tf.identity(hidden),
                    )
                )
        captions.extend(new_captions)
        heapq.heapify(captions)
        captions = heapq.nlargest(beam_size, captions, key=attrgetter("prob"))

    for caption in captions:
        with suppress(ValueError):
            idx = caption.tokens.index("<end>")
            caption.tokens = caption.tokens[:idx]

    finals = [(caption.prob / (len(caption.tokens) ** 0.75), " ".join(caption.tokens)) for caption in captions]
    return min(finals, key=itemgetter(0))[1]
