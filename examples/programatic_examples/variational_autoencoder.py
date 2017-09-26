# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx

from polyaxon_schemas.losses import MeanSquaredErrorConfig
from polyaxon_schemas.optimizers import AdamConfig
from polyaxon_schemas.processing.feature_processors import FeatureProcessorsConfig
from polyaxon_schemas.processing.pipelines import TFRecordImagePipelineConfig


def encoder_fn(mode, features):
    x = plx.layers.Dense(units=128)(features)
    return plx.layers.Dense(units=256)(x)


def decoder_fn(mode, features):
    x = plx.layers.Dense(units=256)(features)
    return plx.layers.Dense(units=28 * 28)(x)


def bridge_fn(mode, features, labels, loss, encoder_fn, decoder_fn):
    return plx.bridges.LatentBridge(mode)(features, labels, loss, encoder_fn, decoder_fn)


def model_fn(features, labels, params, mode, config):
    model = plx.models.Generator(
        mode=mode,
        encoder_fn=encoder_fn,
        decoder_fn=decoder_fn,
        bridge_fn=bridge_fn,
        loss=MeanSquaredErrorConfig(),
        optimizer=AdamConfig(learning_rate=0.00009),
        summaries=['loss'])
    return model(features=features, labels=labels, params=params, config=config)


def get_input_fn(mode, data_files, meta_data_file):
    return plx.processing.create_input_data_fn(
        mode=mode,
        pipeline_config=TFRecordImagePipelineConfig(
            shuffle=plx.Modes.is_train(mode),
            dynamic_pad=False,
            batch_size=64 if plx.Modes.is_train(mode) else 32,
            data_files=data_files,
            meta_data_file=meta_data_file,
            feature_processors=FeatureProcessorsConfig.from_dict(
                {'image': {
                    'input_layers': [['image', 0, 0]],
                    'output_layers': [['reshape', 0, 0]],
                    'layers': [
                        {'Cast': {
                            'name': 'cast',
                            'dtype': 'float32',
                            'inbound_nodes': [['image', 0, 0]]
                        }},
                        {'Standardization': {
                            'name': 'std',
                            'inbound_nodes': [['cast', 0, 0]]
                        }},
                        {'Flatten': {
                            'name': 'flatten',
                            'inbound_nodes': [['std', 0, 0]]
                        }},
                        {'Reshape': {
                            'name': 'reshape',
                            'target_shape': [784],
                            'inbound_nodes': [['flatten', 0, 0]]
                        }}
                    ]
                }})
        )
    )


def experiment_fn(output_dir):
    """Creates a variational auto encoder on MNIST handwritten digits.

    inks:
        * [MNIST Dataset] http://yann.lecun.com/exdb/mnist/
    """
    dataset_dir = '../data/mnist'
    plx.datasets.mnist.prepare(dataset_dir)
    train_data_file = plx.datasets.mnist.RECORD_FILE_NAME_FORMAT.format(dataset_dir,
                                                                        plx.Modes.TRAIN)
    eval_data_file = plx.datasets.mnist.RECORD_FILE_NAME_FORMAT.format(dataset_dir, plx.Modes.EVAL)
    meta_data_file = plx.datasets.mnist.META_DATA_FILENAME_FORMAT.format(dataset_dir)

    experiment = plx.experiments.Experiment(
        estimator=plx.estimators.Estimator(model_fn=model_fn, model_dir=output_dir),
        train_input_fn=get_input_fn(plx.Modes.TRAIN, train_data_file, meta_data_file),
        eval_input_fn=get_input_fn(plx.Modes.EVAL, eval_data_file, meta_data_file),
        train_steps=1000,
        eval_steps=10)

    return experiment


def main(*args):
    plx.experiments.run_experiment(experiment_fn=experiment_fn,
                                   output_dir="/tmp/polyaxon_logs/vae",
                                   schedule='continuous_train_and_eval')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
