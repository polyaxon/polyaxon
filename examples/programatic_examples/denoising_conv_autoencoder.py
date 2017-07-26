# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
import polyaxon as plx


def encoder_fn(mode, features):
    return plx.encoders.Encoder(
        mode=mode,
        modules=[
            plx.layers.Conv2d(mode=mode, num_filter=32, filter_size=3, strides=1, activation='relu',
                              regularizer='l2_regularizer'),
            plx.layers.MaxPool2d(mode=mode, kernel_size=2),
            plx.layers.Conv2d(mode=mode, num_filter=32, filter_size=3, activation='relu',
                              regularizer='l2_regularizer'),
            plx.layers.MaxPool2d(mode=mode,kernel_size=2)
        ]
    )(features)


def decoder_fn(mode, features):
    return plx.decoders.Decoder(
        mode=mode,
        modules=[
            plx.layers.Conv2d(mode=mode, num_filter=32, filter_size=3, strides=1, activation='relu',
                              regularizer='l2_regularizer'),
            plx.layers.Upsample2d(mode=mode, kernel_size=2),
            plx.layers.Conv2d(mode=mode, num_filter=32, filter_size=3, activation='relu',
                              regularizer='l2_regularizer'),
            plx.layers.Upsample2d(mode=mode, kernel_size=2),
            plx.layers.Conv2d(mode=mode, num_filter=1, filter_size=3, activation='relu',
                              regularizer='l2_regularizer')
        ]
    )(features)


def bridge_fn(mode, features, labels, loss_config, encoder_fn, decoder_fn):
    return plx.bridges.NoOpBridge(mode)(features, labels, loss_config, encoder_fn, decoder_fn)


def model_fn(features, labels, params, mode, config):
    model = plx.models.Generator(
        mode=mode,
        encoder_fn=encoder_fn,
        decoder_fn=decoder_fn,
        bridge_fn=bridge_fn,
        loss_config=plx.configs.LossConfig(module='mean_squared_error'),
        optimizer_config=plx.configs.OptimizerConfig(module='adadelta', learning_rate=0.9),
        summaries=['loss', 'image_input', 'image_result'])
    return model(features=features, labels=labels, params=params, config=config)


def get_train_input_fn(data_files, meta_data_file):
    config = plx.configs.InputDataConfig.read_configs(
        {
            "pipeline_config": {
                "module": "TFRecordImagePipeline",
                "batch_size": 64,
                "num_epochs": 1,
                "shuffle": True,
                "dynamic_pad": False,
                "params": {
                    "data_files": data_files,
                    "meta_data_file": meta_data_file
                },
                "definition": {
                    "image": [
                        ["Standardization", {}],
                        ["GaussianNoise", {'scale': 0.5}]
                    ]
                }
            }
        }
    )

    return plx.processing.create_input_data_fn(mode=plx.Modes.TRAIN,
                                               pipeline_config=config.pipeline_config)


def get_eval_input_fn(data_files, meta_data_file):
    config = plx.configs.InputDataConfig.read_configs(
        {
            "pipeline_config": {
                "module": "TFRecordImagePipeline",
                "batch_size": 32,
                "num_epochs": 1,
                "shuffle": True,
                "dynamic_pad": False,
                "params": {
                    "data_files": data_files,
                    "meta_data_file": meta_data_file
                },
                "definition": {
                    "image": [
                        ["Standardization", {}]
                    ]
                }
            }
        }
    )

    return plx.processing.create_input_data_fn(mode=plx.Modes.EVAL,
                                               pipeline_config=config.pipeline_config)


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

    run_config = plx.configs.RunConfig(save_checkpoints_steps=100)
    experiment = plx.experiments.Experiment(
        estimator=plx.estimators.Estimator(model_fn=model_fn, model_dir=output_dir,
                                           config=run_config),
        train_input_fn=get_train_input_fn(train_data_file, meta_data_file),
        eval_input_fn=get_eval_input_fn(eval_data_file, meta_data_file),
        train_steps=1000,
        eval_steps=10,
        eval_every_n_steps=5)

    return experiment


def main(*args):
    plx.experiments.run_experiment(experiment_fn=experiment_fn,
                                   output_dir="/tmp/polyaxon_logs/denoising_conv_autoencoder",
                                   schedule='continuous_train_and_evaluate')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
