from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx

from polyaxon_schemas.losses import SoftmaxCrossEntropyConfig
from polyaxon_schemas.metrics import AccuracyConfig
from polyaxon_schemas.optimizers import AdamConfig


def graph_fn(mode, features):
    x = plx.layers.Embedding(input_dim=10000, output_dim=128)(features['source_token'])
    x = plx.layers.LSTM(units=128, dropout=0.2, recurrent_dropout=0.2)(x)
    x = plx.layers.Dense(units=2)(x)
    return x


def model_fn(features, labels, params, mode, config):
    model = plx.models.Classifier(
        mode=mode,
        graph_fn=graph_fn,
        loss=SoftmaxCrossEntropyConfig(),
        optimizer=AdamConfig(learning_rate=0.001),
        metrics=[AccuracyConfig()],
        summaries='all',
        one_hot_encode=True,
        n_classes=2)
    return model(features=features, labels=labels, params=params, config=config)


def experiment_fn(output_dir):
    """Creates an experiment using LSTM architecture to classify IMDB sentiment dataset."""
    dataset_dir = '../data/imdb'
    plx.datasets.imdb.prepare(dataset_dir)
    train_input_fn, eval_input_fn = plx.datasets.imdb.create_input_fn(dataset_dir)

    experiment = plx.experiments.Experiment(
        estimator=plx.estimators.Estimator(model_fn=model_fn, model_dir=output_dir),
        train_input_fn=train_input_fn,
        eval_input_fn=eval_input_fn,
        train_steps=10000,
        eval_steps=10)

    return experiment


def main(*args):
    plx.experiments.run_experiment(experiment_fn=experiment_fn,
                                   output_dir="/tmp/polyaxon_logs/imdb_lsmt",
                                   schedule='continuous_train_and_eval')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
