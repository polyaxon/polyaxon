#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

import keras
import tensorflow as tf

from keras.datasets import fashion_mnist
from tensorflow.keras.layers import Dense, Flatten, Conv2D, Dense, Dropout, Activation, MaxPooling2D
from tensorflow.keras.models import Sequential
from tensorflow.keras import optimizers

from polyaxon import tracking
from polyaxon.tracking.contrib.keras import PolyaxonKerasCallback, PolyaxonKerasModelCheckpoint


OPTIMIZERS = {
    'adam': optimizers.Adam,
    'rmsprop': optimizers.RMSprop,
    'sgd': optimizers.SGD,
}


def create_model(
    conv1_size,
    conv2_size,
    dropout,
    hidden1_size,
    conv_activation,
    dense_activation,
    optimizer,
    learning_rate,
    loss,
    num_classes,
):
    model = Sequential()
    model.add(Conv2D(conv1_size, (5, 5), activation=conv_activation,
                     input_shape=(img_width, img_height, 1)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(conv2_size, (5, 5), activation=conv_activation))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(dropout))
    model.add(Flatten())
    model.add(Dense(hidden1_size, activation=dense_activation))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(
        optimizer=OPTIMIZERS[optimizer](lr=learning_rate),
        loss=loss,
        metrics=['accuracy'],
    )

    return model


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--conv1_size',
        type=int,
        default=32)
    parser.add_argument(
        '--conv2_size',
        type=int,
        default=64
    )
    parser.add_argument(
        '--dropout',
        type=float,
        default=0.2
    )
    parser.add_argument(
        '--hidden1_size',
        type=int,
        default=500
    )
    parser.add_argument(
        '--conv_activation',
        type=str,
        default="relu"
    )
    parser.add_argument(
        '--dense_activation',
        type=str,
        default="relu"
    )
    parser.add_argument(
        '--optimizer',
        type=str,
        default='adam'
    )
    parser.add_argument(
        '--learning_rate',
        type=float,
        default=0.001
    )
    parser.add_argument(
        '--epochs',
        type=int,
        default=10
    )
    parser.add_argument(
        '--loss',
        type=str,
        default="categorical_crossentropy"
    )

    args = parser.parse_args()

    img_width, img_height = 28, 28

    # Data
    (X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()
    labels = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
              "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]

    X_train = X_train.astype('float32')
    X_train /= 255.
    X_test = X_test.astype('float32')
    X_test /= 255.

    # reshape input data
    X_train = X_train.reshape(X_train.shape[0], img_width, img_height, 1)
    X_test = X_test.reshape(X_test.shape[0], img_width, img_height, 1)

    # one hot encode outputs
    y_train = keras.utils.to_categorical(y_train)
    y_test = keras.utils.to_categorical(y_test)
    num_classes = y_test.shape[1]

    # Polyaxon
    tracking.init()
    plx_callback = PolyaxonKerasCallback()
    plx_model_callback = PolyaxonKerasModelCheckpoint()
    log_dir = tracking.get_tensorboard_path()

    print("log_dir", log_dir)
    print("model_dir", plx_model_callback.filepath)
    # TF Model
    model = create_model(
        conv1_size=args.conv1_size,
        conv2_size=args.conv2_size,
        dropout=args.dropout,
        hidden1_size=args.hidden1_size,
        conv_activation=args.conv_activation,
        dense_activation=args.dense_activation,
        optimizer=args.optimizer,
        learning_rate=args.learning_rate,
        loss=args.loss,
        num_classes=y_test.shape[1]
    )

    tensorboard_callback = tf.keras.callbacks.TensorBoard(
        log_dir=log_dir,
        histogram_freq=1,
        update_freq=100
    )

    model.fit(x=X_train,
              y=y_train,
              epochs=args.epochs,
              validation_data=(X_test, y_test),
              callbacks=[tensorboard_callback, plx_callback, plx_model_callback])
