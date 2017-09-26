# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx

from polyaxon_schemas.losses import MeanSquaredErrorConfig
from polyaxon_schemas.optimizers import AdadeltaConfig
from polyaxon_schemas.processing.feature_processors import FeatureProcessorsConfig
from polyaxon_schemas.processing.pipelines import TFRecordImagePipelineConfig


def encoder_fn(mode, features):
    x = plx.layers.Conv2D(filters=32, kernel_size=3, activation='relu', padding='same')(features)
    x = plx.layers.MaxPooling2D(pool_size=2, padding='same')(x)
    x = plx.layers.Conv2D(filters=32, kernel_size=3, activation='relu', padding='same')(x)
    return plx.layers.MaxPooling2D(pool_size=2, padding='same')(x)


def decoder_fn(mode, features):
    x = plx.layers.Conv2D(filters=32, kernel_size=3, activation='relu', padding='same')(features)
    x = plx.layers.UpSampling2D(size=2)(x)
    x = plx.layers.Conv2D(filters=32, kernel_size=3, activation='relu', padding='same')(x)
    x = plx.layers.UpSampling2D(size=2)(x)
    return plx.layers.Conv2D(filters=1, kernel_size=3, activation='sigmoid', padding='same')(x)


def bridge_fn(mode, features, labels, loss, encoder_fn, decoder_fn):
    return plx.bridges.NoOpBridge(mode)(features, labels, loss, encoder_fn, decoder_fn)


def model_fn(features, labels, params, mode, config):
    model = plx.models.Generator(
        mode=mode,
        encoder_fn=encoder_fn,
        decoder_fn=decoder_fn,
        bridge_fn=bridge_fn,
        loss=MeanSquaredErrorConfig(),
        optimizer=AdadeltaConfig(learning_rate=0.9),
        summaries=['loss', 'image_input', 'image_result'])
    return model(features=features, labels=labels, params=params, config=config)


def get_train_input_fn(data_files, meta_data_file):
    return plx.processing.create_input_data_fn(
        mode=plx.Modes.TRAIN,
        pipeline_config=TFRecordImagePipelineConfig(
            shuffle=True,
            dynamic_pad=False,
            batch_size=64,
            data_files=data_files,
            meta_data_file=meta_data_file,
            feature_processors=FeatureProcessorsConfig.from_dict(
                {'image': {
                    'input_layers': [['image', 0, 0]],
                    'output_layers': [['noise', 0, 0]],
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
                        {'GaussianNoise': {
                            'name': 'noise',
                            'stddev': 0.5,
                            'inbound_nodes': [['std', 0, 0]]
                        }}
                    ]
                }})
        )
    )


def get_eval_input_fn(data_files, meta_data_file):
    return plx.processing.create_input_data_fn(
        mode=plx.Modes.EVAL,
        pipeline_config=TFRecordImagePipelineConfig(
            shuffle=False,
            dynamic_pad=False,
            batch_size=32,
            data_files=data_files,
            meta_data_file=meta_data_file,
            feature_processors=FeatureProcessorsConfig.from_dict(
                {'image': {
                    'input_layers': [['image', 0, 0]],
                    'output_layers': [['std', 0, 0]],
                    'layers': [
                        {'Cast': {
                            'name': 'cast',
                            'dtype': 'float32',
                            'inbound_nodes': [['image', 0, 0]]
                        }},
                        {'Standardization': {
                            'name': 'std',
                            'inbound_nodes': [['cast', 0, 0]]
                        }}
                    ]
                }})
        )
    )


def experiment_fn(output_dir):
    """Creates an auto encoder on MNIST handwritten digits.

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
        train_input_fn=get_train_input_fn(train_data_file, meta_data_file),
        eval_input_fn=get_eval_input_fn(eval_data_file, meta_data_file),
        train_steps=1000,
        eval_steps=10)

    return experiment


def main(*args):
    plx.experiments.run_experiment(experiment_fn=experiment_fn,
                                   output_dir="/tmp/polyaxon_logs/denoising_conv_autoencoder",
                                   schedule='continuous_train_and_eval')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
