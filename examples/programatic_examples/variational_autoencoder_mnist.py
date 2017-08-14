# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import numpy as np
import tensorflow as tf
import polyaxon as plx

from tensorflow.examples.tutorials.mnist import input_data

from polyaxon.libs.utils import total_tensor_depth


def encoder_fn(mode, features):
    return plx.encoders.Encoder(
        mode=mode,
        modules=[
            plx.layers.FullyConnected(mode=mode, num_units=256, activation='relu')
        ]
    )(features)


def decoder_fn(mode, features):
    return plx.decoders.Decoder(
        mode=mode,
        modules=[
            plx.layers.FullyConnected(mode=mode, num_units=256, activation='relu'),
            plx.layers.FullyConnected(mode=mode, num_units=28 * 28)
        ]
    )(features)


def bridge_fn(mode, features, labels, loss_config, encoder_fn, decoder_fn):
    return plx.bridges.LatentBridge(mode, latent_dim=2)(features, labels, loss_config,
                                                        encoder_fn, decoder_fn)


def model_fn(features, labels, params, mode, config):
    model = plx.models.Generator(
        mode=mode,
        encoder_fn=encoder_fn,
        decoder_fn=decoder_fn,
        bridge_fn=bridge_fn,
        loss_config=plx.configs.LossConfig(module='sigmoid_cross_entropy'),
        optimizer_config=plx.configs.OptimizerConfig(module='adam', learning_rate=0.00009),
        summaries=['loss'])
    return model(features=features, labels=labels, params=params, config=config)


def experiment_fn(output_dir, x_train, y_train, x_eval, y_eval):
    """Creates a variational auto encoder on MNIST handwritten digits.

    inks:
        * [MNIST Dataset] http://yann.lecun.com/exdb/mnist/
    """
    run_config = plx.configs.RunConfig(save_checkpoints_steps=100)
    return plx.experiments.Experiment(
        estimator=plx.estimators.Estimator(
            model_fn=model_fn, model_dir=output_dir, config=run_config),
        train_input_fn=plx.processing.numpy_input_fn(
            x=x_train, y=y_train, batch_size=64, num_epochs=None, shuffle=False),
        eval_input_fn=plx.processing.numpy_input_fn(
            x=x_eval, y=y_eval, batch_size=32, num_epochs=None, shuffle=False),
        train_steps=5000,
        eval_steps=100,
        eval_every_n_steps=5)


def encode(estimator, images, labels):
    results = estimator.encode(
        plx.processing.numpy_input_fn({'images': images}, batch_size=10000, shuffle=False),
        predict_keys=['results'])

    x = []
    y = []
    for result in results:
        x.append(result['results'][0])
        y.append(result['results'][1])

    try:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(5, 5))
        plt.scatter(x, y, c=labels)
        plt.colorbar()
        plt.show()
    except ImportError:
        pass


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
        plx.processing.numpy_input_fn({'samples': samples}, batch_size=n * n, shuffle=False))

    results = [x['results'] for x in x_reconstructed]
    for i, x in enumerate(x_axis):
        for j, y in enumerate(y_axis):
            digit = results[i * n + j].reshape(28, 28)
            figure[i * 28: (i + 1) * 28, j * 28: (j + 1) * 28] = digit

    try:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(10, 10))
        plt.imshow(figure, cmap='Greys_r')
        plt.show()
    except ImportError:
        pass


def main(*args):
    dataset_dir = "../data/mnist-tf"
    mnist = input_data.read_data_sets(dataset_dir)

    x_train = mnist.train.images.astype('float32') / 255.
    x_eval = mnist.validation.images.astype('float32') / 255.
    x_test = mnist.test.images.astype('float32') / 255.
    x_train = x_train.reshape((len(x_train), total_tensor_depth(x_train)))
    x_eval = x_eval.reshape((len(x_eval), total_tensor_depth(x_eval)))
    x_test = x_test.reshape((len(x_test), total_tensor_depth(x_test)))

    xp = experiment_fn("/tmp/polyaxon_logs/vae",
                       {'images': x_train}, mnist.train.labels,
                       {'images': x_eval}, mnist.validation.labels)
    xp.continuous_train_and_evaluate()

    encode(xp.estimator, x_test, mnist.test.labels)
    generate(xp.estimator)


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
