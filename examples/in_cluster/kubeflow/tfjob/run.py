"""An example of multi-worker training with Keras model using Strategy API."""

from __future__ import absolute_import, division, print_function

import argparse
import json
import os

import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras import layers, models
from tensorflow.keras import optimizers

from polyaxon import tracking
from polyaxon.tracking.contrib.keras import PolyaxonKerasCallback, PolyaxonKerasModelCheckpoint


OPTIMIZERS = {
    'adam': optimizers.Adam,
    'rmsprop': optimizers.RMSprop,
    'sgd': optimizers.SGD,
}


def make_datasets_unbatched():
    BUFFER_SIZE = 10000

    # Scaling MNIST data from (0, 255] to (0., 1.]
    def scale(image, label):
        image = tf.cast(image, tf.float32)
        image /= 255
        return image, label

    datasets, info = tfds.load(name='mnist', with_info=True, as_supervised=True)

    return datasets['train'].map(scale).cache().shuffle(BUFFER_SIZE)


def get_model(args):
    model = models.Sequential()
    model.add(
        layers.Conv2D(args.conv1_size, (3, 3), activation=args.conv_activation, input_shape=(28, 28, 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(args.conv2_size, (3, 3), activation=args.conv_activation))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation=args.conv_activation))
    model.add(layers.Dropout(args.dropout))
    model.add(layers.Flatten())
    model.add(layers.Dense(args.hidden1_size, activation=args.dense_activation))
    model.add(layers.Dense(10, activation='softmax'))

    model.summary()

    model.compile(optimizer=OPTIMIZERS[args.optimizer](learning_rate=args.learning_rate),
                  loss=args.loss,
                  metrics=['accuracy'])

    return model


def decay(epoch):
    if epoch < 3:
        return 1e-3
    elif epoch >= 3 and epoch < 7:
        return 1e-4
    else:
        return 1e-5


def main(args):
    # MultiWorkerMirroredStrategy creates copies of all variables in the model's
    # layers on each device across all workers
    # if your GPUs don't support NCCL, replace "communication" with another
    strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy(
        communication=tf.distribute.experimental.CollectiveCommunication.NCCL)

    BATCH_SIZE_PER_REPLICA = 64
    BATCH_SIZE = BATCH_SIZE_PER_REPLICA * strategy.num_replicas_in_sync

    with strategy.scope():
        ds_train = make_datasets_unbatched().batch(BATCH_SIZE).repeat()
        options = tf.data.Options()
        options.experimental_distribute.auto_shard_policy = \
            tf.data.experimental.AutoShardPolicy.DATA
        ds_train = ds_train.with_options(options)
        # Model building/compiling need to be within `strategy.scope()`.
        multi_worker_model = get_model(args)

    # Function for decaying the learning rate.
    # You can define any decay function you need.
    # Callback for printing the LR at the end of each epoch.
    class PrintLR(tf.keras.callbacks.Callback):

        def on_epoch_end(self, epoch, logs=None):
            print('\nLearning rate for epoch {} is {}'.format(
                epoch + 1, multi_worker_model.optimizer.lr.numpy()))
    callbacks = [
        PrintLR(),
        tf.keras.callbacks.LearningRateScheduler(decay),
    ]

    # Polyaxon
    if TASK_INDEX == 0:
        plx_callback = PolyaxonKerasCallback()
        plx_model_callback = PolyaxonKerasModelCheckpoint(save_weights_only=True)
        log_dir = tracking.get_tensorboard_path()
        callbacks = [
            tf.keras.callbacks.TensorBoard(log_dir=log_dir),
            plx_model_callback,
            plx_callback,
        ]

    # Keras' `model.fit()` trains the model with specified number of epochs and
    # number of steps per epoch. Note that the numbers here are for demonstration
    # purposes only and may not sufficiently produce a model with good quality.
    multi_worker_model.fit(ds_train,
                           epochs=args.epochs,
                           steps_per_epoch=70,
                           callbacks=callbacks)

    multi_worker_model.save("/tmp/model")

    if TASK_INDEX == 0:
        tracking.log_model(path="/tmp/model", framework="tensorflow")


if __name__ == '__main__':
    os.environ['NCCL_DEBUG'] = 'INFO'

    tfds.disable_progress_bar()

    # to decide if a worker is chief, get TASK_INDEX in Cluster info
    tf_config = json.loads(os.environ.get('TF_CONFIG') or '{}')
    TASK_INDEX = tf_config['task']['index']

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
        default=64
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
        default="sparse_categorical_crossentropy"
    )

    args = parser.parse_args()

    # Polyaxon
    if TASK_INDEX == 0:
        tracking.init()

    main(args)
