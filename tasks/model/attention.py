import tensorflow as tf
from keras import Model
from keras.layers import Dense, Dropout

from tasks.model.config import get_model_configuration

model_config = get_model_configuration()


class Attention(Model):
    def __init__(self, hidden_dim):
        super(Attention, self).__init__()
        self.hidden_dim = hidden_dim
        self.U = Dense(
            units=hidden_dim,
        )
        self.W = Dense(
            units=hidden_dim,
        )
        self.V = Dense(
            units=1,
        )
        self.dropout = Dropout(model_config.DROPOUT_RATE)

    def call(self, image_features, hidden_state, training=False):
        if training:
            hidden_state = self.dropout(hidden_state)
            image_features = self.dropout(image_features)

        hidden_state = tf.expand_dims(hidden_state, axis=1)
        attention_hidden = tf.nn.tanh(self.U(image_features) + self.W(hidden_state))

        if training:
            attention_hidden = self.dropout(attention_hidden)

        score = self.V(attention_hidden)
        attention_weights = tf.nn.softmax(score, axis=1)
        context_vector = attention_weights * image_features

        if training:
            context_vector = self.dropout(context_vector)

        context_vector = tf.reduce_sum(context_vector, axis=1)
        return context_vector, attention_weights
