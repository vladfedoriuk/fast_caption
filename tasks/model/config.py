from functools import lru_cache


class Configuration:
    DATASET_SIZE = 32000
    BATCH_SIZE = 32
    EPOCHS = 30
    MAX_FEATURES = 1000
    EMBEDDING_DIM = 512
    HIDDEN_DIM = 256
    MAX_SEQ_LEN = 20
    TEST_SIZE = 0.05
    VAL_SIZE = 0.05
    IMAGE_SIZE = {"vgg16": (224, 224)}
    CNN_OUTPUT = {"vgg16": (7, 7, 512)}
    DROPOUT_RATE = 0.1


@lru_cache
def get_model_configuration() -> Configuration:
    return Configuration()
