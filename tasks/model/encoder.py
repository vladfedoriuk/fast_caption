from keras import Model
from keras.layers import BatchNormalization, Dense, Dropout

from tasks.model.config import get_model_configuration

model_config = get_model_configuration()


class Encoder(Model):
    def __init__(self):
        super(Encoder, self).__init__()
        self.D = Dense(
            units=model_config.EMBEDDING_DIM,
            activation="relu",
        )
        self.dropout = Dropout(model_config.DROPOUT_RATE)
        self.bna = BatchNormalization()

    def call(self, image_features, training=False):
        output = self.D(image_features)
        output = self.bna(output, training=training)
        if training:
            output = self.dropout(output)
        return output
