from tensorflow import keras
from tensorflow.keras import layers


def vgg(input_tensor):
    """
    The original feature extraction structure from CRNN paper.
    Related paper: http://arxiv.org/abs/1507.05717
    """
    x = layers.Conv2D(
        filters=64, 
        kernel_size=3, 
        padding='same',
        activation='relu')(input_tensor)
    x = layers.MaxPool2D(pool_size=2, padding='same')(x)

    x = layers.Conv2D(
        filters=128, 
        kernel_size=3, 
        padding='same',
        activation='relu')(x)
    x = layers.MaxPool2D(pool_size=2, padding='same')(x)

    for i in range(2):
        x = layers.Conv2D(filters=256, kernel_size=3, padding='same',
                          activation='relu')(x)
    x = layers.MaxPool2D(pool_size=(2, 2), strides=(2, 1), padding='same')(x)

    for i in range(2):
        x = layers.Conv2D(filters=512, kernel_size=3, padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
    x = layers.MaxPool2D(pool_size=(2, 2), strides=(2, 1), padding='same')(x)

    x = layers.Conv2D(filters=512, kernel_size=2, activation='relu')(x)
    return x


def crnn(num_classes):
    img_input = keras.Input(shape=(32, None, 1))

    x = vgg(img_input)
    x = layers.Reshape((-1, 512))(x)

    x = layers.Bidirectional(layers.LSTM(units=256, return_sequences=True))(x)
    x = layers.Bidirectional(layers.LSTM(units=256, return_sequences=True))(x)
    x = layers.Dense(units=num_classes)(x)
    return keras.Model(inputs=img_input, outputs=x, name='CRNN')


if __name__ == "__main__":
    model = crnn(10)
    model.summary()