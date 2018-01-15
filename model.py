from __future__ import division, print_function, absolute_import

import argparse

import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data

from polyaxon_helper import get_outputs_path, send_metrics, get_log_level


def set_logging(log_level=None):
    if log_level == 'INFO':
        log_level = tf.logging.INFO
    elif log_level == 'DEBUG':
        log_level = tf.logging.DEBUG
    elif log_level == 'WARN':
        log_level = tf.logging.WARN
    else:
        log_level = 'INFO'

    tf.logging.set_verbosity(log_level)


set_logging(get_log_level())


mnist = input_data.read_data_sets("/tmp/data/", one_hot=False)


def get_model_fn(learning_rate, dropout, activation):
    """Create a `model_fn` compatible with tensorflow estimator based on hyperparams."""

    def get_network(x_dict, is_training):
        with tf.variable_scope('network'):
            x = x_dict['images']
            x = tf.reshape(x, shape=[-1, 28, 28, 1])
            conv1 = tf.layers.conv2d(x, 32, 5, activation=activation)
            conv1 = tf.layers.max_pooling2d(conv1, 2, 2)
            conv2 = tf.layers.conv2d(conv1, 64, 3, activation=activation)
            conv2 = tf.layers.max_pooling2d(conv2, 2, 2)
            fc1 = tf.contrib.layers.flatten(conv2)
            fc1 = tf.layers.dense(fc1, 1024)
            fc1 = tf.layers.dropout(fc1, rate=dropout, training=is_training)
            out = tf.layers.dense(fc1, 10)
        return out

    def model_fn(features, labels, mode):
        is_training = mode == tf.estimator.ModeKeys.TRAIN

        results = get_network(features, is_training=is_training)

        pred_classes = tf.argmax(results, axis=1)

        # Return prediction
        if mode == tf.estimator.ModeKeys.PREDICT:
            return tf.estimator.EstimatorSpec(mode, predictions=pred_classes)

        # Define loss
        loss_op = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(
            logits=results, labels=tf.cast(labels, dtype=tf.int32)))
        optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
        train_op = optimizer.minimize(loss_op, global_step=tf.train.get_global_step())

        # Evaluation metrics
        accuracy = tf.metrics.accuracy(labels=labels, predictions=pred_classes)
        precision = tf.metrics.precision(labels=labels, predictions=pred_classes)

        return tf.estimator.EstimatorSpec(
            mode=mode,
            predictions=pred_classes,
            loss=loss_op,
            train_op=train_op,
            eval_metric_ops={'accuracy': accuracy, 'precision': precision})

    return model_fn


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--batch_size',
        default=128,
        type=int
    )
    parser.add_argument(
        '--num_steps',
        default=200,
        type=int
    )
    parser.add_argument(
        '--learning_rate',
        default=0.001,
        type=int
    )
    parser.add_argument(
        '--dropout',
        default=0.25,
        type=int
    )
    parser.add_argument(
        '--num_epochs',
        default=1,
        type=int
    )
    parser.add_argument(
        '--activation',
        default='relu',
        type=str
    )

    args = parser.parse_args()
    arguments = args.__dict__

    batch_size = arguments.pop('batch_size')
    num_steps = arguments.pop('num_steps')
    learning_rate = arguments.pop('learning_rate')
    dropout = arguments.pop('dropout')
    num_epochs = arguments.pop('num_epochs')
    activation = arguments.pop('activation')
    if activation == 'relu':
        activation = tf.nn.relu
    elif activation == 'sigmoid':
        activation = tf.nn.sigmoid
    elif activation == 'linear':
        activation = None

    estimator = tf.estimator.Estimator(
        get_model_fn(learning_rate=learning_rate, dropout=dropout, activation=activation),
        model_dir=get_outputs_path())

    # Train the Model
    input_fn = tf.estimator.inputs.numpy_input_fn(
        x={'images': mnist.train.images},
        y=mnist.train.labels,
        batch_size=batch_size,
        num_epochs=num_epochs,
        shuffle=True)
    estimator.train(input_fn, steps=num_steps)

    # Evaluate the Model
    input_fn = tf.estimator.inputs.numpy_input_fn(
        x={'images': mnist.test.images},
        y=mnist.test.labels,
        batch_size=batch_size,
        shuffle=False)

    metrics = estimator.evaluate(input_fn)

    print("Testing mterics: {}", metrics)
    send_metrics(loss=metrics['loss'], accuracy=metrics['accuracy'], precision=metrics['precision'])
