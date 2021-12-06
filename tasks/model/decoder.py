# decoder
from keras import Model
from keras.layers import Embedding, Dense, GRU, Dropout, Concatenate
import tensorflow as tf

from tasks.model.config import get_model_configuration

model_config = get_model_configuration()


class Decoder(Model):
    def __init__(self, attention: Model):
        super(Decoder, self).__init__()
        self.embedding = Embedding(
            input_dim=model_config.MAX_FEATURES + 1,
            output_dim=model_config.EMBEDDING_DIM,
        )
        self.gru = GRU(
            units=model_config.HIDDEN_DIM,
            return_sequences=True,
            return_state=True,
            recurrent_initializer="glorot_uniform",
        )
        self.fc = Dense(
            units=model_config.MAX_FEATURES,
            activation="softmax",
        )
        self.dropout = Dropout(model_config.DROPOUT_RATE)
        self.attention = attention

    def call(self, input, image_features, hidden_state, training=False):
        if training:
            hidden_state = self.dropout(hidden_state)
        context_vector, context_weights = self.attention(
            image_features, hidden_state, training=training
        )
        if training:
            context_vector = self.dropout(context_vector)

        embedding = self.embedding(input)
        if training:
            embedding = self.dropout(embedding)

        concat = Concatenate()([tf.expand_dims(context_vector, axis=1), embedding])
        if training:
            concat = self.dropout(concat)

        output, state = self.gru(concat, initial_state=hidden_state)
        if training:
            state = self.dropout(state)

        output = tf.reshape(output, (-1, output.shape[2]))
        if training:
            output = self.dropout(output)
        output = self.fc(output)

        return output, state, context_weights

    def reset_state(self, batch_size=model_config.BATCH_SIZE):
        return tf.zeros((batch_size, model_config.HIDDEN_DIM))
