# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.python.estimator.inputs.numpy_io import numpy_input_fn

import polyaxon as plx

from tensorflow.examples.tutorials.mnist import input_data


def create_experiment_json_fn(output_dir, X_train, y_train, X_eval, y_eval):
    """Creates a variational auto encoder on MNIST handwritten digits.

    inks:
        * [MNIST Dataset] http://yann.lecun.com/exdb/mnist/
    """
    config = {
        'name': 'vae_mnsit',
        'output_dir': output_dir,
        'eval_every_n_steps': 100,
        'train_steps_per_iteration': 100,
        'train_steps': 2000,
        'run_config': {'save_checkpoints_steps': 100},
        'train_input_data_config': {
             'input_type': plx.configs.InputDataConfig.NUMPY,
             'pipeline_config': {'name': 'train', 'batch_size': 64, 'num_epochs': None,
                                 'shuffle': True},
             'x': X_train,
             'y': y_train
         },
        'eval_input_data_config': {
             'input_type': plx.configs.InputDataConfig.NUMPY,
             'pipeline_config': {'name': 'eval', 'batch_size': 32, 'num_epochs': None,
                                 'shuffle': False},
             'x': X_eval,
             'y': y_eval
         },
        'estimator_config': {'output_dir': output_dir},
        'model_config': {
            'module': 'Generator',
            'summaries': ['loss', 'image_input', 'image_result', 'image_generated'],
            'loss_config': {'module': 'sigmoid_cross_entropy'},
            'optimizer_config': {'module': 'adam', 'learning_rate': 0.0009},
            'encoder_config': {
                'definition': [
                    (plx.layers.FullyConnected, {'num_units': 256, 'activation': 'relu'}),
                ]
            },
            'decoder_config': {
                'definition': [
                    (plx.layers.FullyConnected, {'num_units': 256, 'activation': 'relu'}),
                    (plx.layers.FullyConnected, {'num_units': 28 * 28}),
                ]
            },
            'bridge_config': {'module': 'LatentBridge', 'latent_dim': 2}
        }
    }
    experiment_config = plx.configs.ExperimentConfig.read_configs(config)
    return plx.experiments.create_experiment(experiment_config)


def encode(estimator, images, labels):
    results = estimator.encode(
        numpy_input_fn({'images': images}, batch_size=10000, shuffle=False),
        predict_keys=['results'])

    x = []
    y = []
    for result in results:
        x.append(result['results'][0])
        y.append(result['results'][1])

    plt.figure(figsize=(5, 5))
    plt.scatter(x, y, c=labels)
    plt.colorbar()
    plt.show()


def generate(estimator):
    from scipy.stats import norm

    n = 15  # Figure row size
    figure = np.zeros((28 * n, 28 * n))
    # Random normal distributions to feed network with
    x_axis = norm.ppf(np.linspace(0.05, 0.95, n))
    y_axis = norm.ppf(np.linspace(0.05, 0.95, n))

    samples = []
    for i, x in enumerate(x_axis):
        for j, y in enumerate(y_axis):
            samples.append(np.array([x, y], dtype=np.float32))

    samples = np.array(samples)
    x_reconstructed = estimator.generate(
        numpy_input_fn({'samples': samples}, batch_size=n * n, shuffle=False))

    results = [x['results'] for x in x_reconstructed]
    for i, x in enumerate(x_axis):
        for j, y in enumerate(y_axis):
            digit = results[i * n + j].reshape(28, 28)
            figure[i * 28: (i + 1) * 28, j * 28: (j + 1) * 28] = digit

    plt.figure(figsize=(10, 10))
    plt.imshow(figure, cmap='Greys_r')
    plt.show()


def main(*args):
    dataset_dir = "./data/mnist-tf"
    mnist = input_data.read_data_sets(dataset_dir)

    X_train = mnist.train.images.astype('float32') / 255.
    X_eval = mnist.validation.images.astype('float32') / 255.
    X_test = mnist.test.images.astype('float32') / 255.
    X_train = X_train.reshape((len(X_train), np.prod(X_train.shape[1:])))
    X_eval = X_eval.reshape((len(X_eval), np.prod(X_eval.shape[1:])))
    X_test = X_test.reshape((len(X_test), np.prod(X_test.shape[1:])))

    xp = create_experiment_json_fn("/tmp/polyaxon_logs/vae",
                                   {'images': X_train}, mnist.train.labels,
                                   {'images': X_eval}, mnist.validation.labels)
    xp.continuous_train_and_evaluate()

    encode(xp.estimator, X_test, mnist.test.labels)
    generate(xp.estimator)


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
