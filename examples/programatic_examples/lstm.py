from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx


def graph_fn(mode, features):
    x = plx.layers.Embedding(mode=mode, input_dim=10000, output_dim=128)(features['source_token'])
    x = plx.layers.LSTM(mode=mode, num_units=128, dropout=0.8, dynamic=True)(x)
    x = plx.layers.FullyConnected(mode=mode, num_units=2)(x)
    return x


def model_fn(features, labels, params, mode, config):
    model = plx.models.Classifier(
        mode=mode,
        graph_fn=graph_fn,
        loss_config=plx.configs.LossConfig(module='softmax_cross_entropy'),
        optimizer_config=plx.configs.OptimizerConfig(module='adam', learning_rate=0.001),
        eval_metrics_config=[plx.configs.MetricConfig(module='streaming_accuracy')],
        summaries='all',
        one_hot_encode=True,
        n_classes=2)
    return model(features=features, labels=labels, params=params, config=config)


def experiment_fn(output_dir):
    """Creates an experiment using LSTM architecture to classify IMDB sentiment dataset."""
    dataset_dir = '../data/imdb'
    plx.datasets.imdb.prepare(dataset_dir)
    train_input_fn, eval_input_fn = plx.datasets.imdb.create_input_fn(dataset_dir)

    run_config = plx.configs.RunConfig(save_checkpoints_steps=100)
    experiment = plx.experiments.Experiment(
        estimator=plx.estimators.Estimator(model_fn=model_fn, model_dir=output_dir,
                                           config=run_config),
        train_input_fn=train_input_fn,
        eval_input_fn=eval_input_fn,
        train_steps=10000,
        eval_steps=10,
        eval_every_n_steps=5)

    return experiment


def main(*args):
    plx.experiments.run_experiment(experiment_fn=experiment_fn,
                                   output_dir="/tmp/polyaxon_logs/lenet",
                                   schedule='continuous_train_and_evaluate')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
