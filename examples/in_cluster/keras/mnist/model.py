import argparse

import tensorflow as tf

# Polyaxon
from polyaxon import tracking
from polyaxon.tracking.contrib.keras import PolyaxonCallback

OPTIMIZERS = {
    'adam': tf.keras.optimizers.Adam,
    'rmsprop': tf.keras.optimizers.RMSprop,
    'sgd': tf.keras.optimizers.SGD,
}


def transform_data(x_train, y_train, x_test, y_test):
    x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
    x_train = x_train.astype('float32') / 255

    x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)
    x_test = x_test.astype('float32') / 255

    y_train = tf.keras.utils.to_categorical(y_train, num_classes=10)
    y_test = tf.keras.utils.to_categorical(y_test, num_classes=10)

    return x_train, y_train, x_test, y_test


def train(conv1_size, conv2_size, dropout, hidden1_size, optimizer, log_learning_rate, epochs):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(filters=conv1_size,
                                     kernel_size=(3, 3),
                                     activation='relu',
                                     input_shape=x_train.shape[1:]))
    model.add(tf.keras.layers.Conv2D(filters=conv2_size,
                                     kernel_size=(3, 3),
                                     activation='relu'))
    model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(tf.keras.layers.Dropout(dropout))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(hidden1_size, activation='relu'))
    model.add(tf.keras.layers.Dense(10, activation='softmax'))

    optimizer = OPTIMIZERS[optimizer](lr=10 ** log_learning_rate)
    model.compile(
        optimizer=optimizer,
        loss='categorical_crossentropy',
        metrics=['accuracy'],
    )

    model.fit(
        x_train,
        y_train,
        epochs=epochs,
        batch_size=100,
        callbacks=[PolyaxonCallback()],  # Polyaxon
    )
    return model.evaluate(x_test, y_test)[1]


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
        default=0.8
    )
    parser.add_argument(
        '--hidden1_size',
        type=int,
        default=500
    )
    parser.add_argument(
        '--optimizer',
        type=str,
        default='adam'
    )
    parser.add_argument(
        '--log_learning_rate',
        type=int,
        default=-3
    )
    parser.add_argument(
        '--epochs',
        type=int,
        default=1
    )
    args = parser.parse_args()

    # Polyaxon
    tracking.init()

    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

    # Polyaxon
    tracking.log_data_ref(content=x_train, name='x_train')
    tracking.log_data_ref(content=y_train, name='y_train')
    tracking.log_data_ref(content=x_test, name='x_test')
    tracking.log_data_ref(content=y_test, name='y_test')

    x_train, y_train, x_test, y_test = transform_data(x_train, y_train, x_test, y_test)
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(256, activation=tf.keras.activations.relu),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(10, activation=tf.keras.activations.softmax)
    ])

    accuracy = train(conv1_size=args.conv1_size,
                     conv2_size=args.conv2_size,
                     dropout=args.dropout,
                     hidden1_size=args.hidden1_size,
                     optimizer=args.optimizer,
                     log_learning_rate=args.log_learning_rate,
                     epochs=args.epochs)

    # Polyaxon
    tracking.log_metrics(eval_accuracy=accuracy)
