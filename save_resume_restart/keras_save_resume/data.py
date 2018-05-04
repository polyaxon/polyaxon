from __future__ import print_function

import numpy as np

import keras

from keras.datasets import cifar10

from polyaxon_helper import get_data_path


def get_data(subtract_pixel_mean, num_classes):
    # Load the CIFAR10 data.
    data_path = '{}/{}'.format(get_data_path(), "imdb.npz")
    (x_train, y_train), (x_test, y_test) = cifar10.load_data(path=data_path)

    # Input image dimensions.
    input_shape = x_train.shape[1:]

    # Normalize data.
    x_train = x_train.astype('float32') / 255
    x_test = x_test.astype('float32') / 255

    # If subtract pixel mean is enabled
    if subtract_pixel_mean:
        x_train_mean = np.mean(x_train, axis=0)
        x_train -= x_train_mean
        x_test -= x_train_mean

    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')
    print('y_train shape:', y_train.shape)

    # Convert class vectors to binary class matrices.
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    return ({'x': x_train, 'y': y_train},
            {'x': x_test, 'y': y_test},
            input_shape)
