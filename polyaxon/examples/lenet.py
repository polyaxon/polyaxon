import tensorflow as tf
import polyaxon as plx

from polyaxon.examples.mnist_data import load_mnist


def create_experiment_json_fn(output_dir):
    X_train, Y_train, X_test, Y_test = load_mnist()

    config = {
        'name': 'real_mnsit',
        'output_dir': output_dir,
        'eval_every_n_steps': 5,
        'run_config': {'save_checkpoints_steps': 100},
        'train_input_data_config': {
            'input_type': plx.configs.InputDataConfig.NUMPY,
            'pipeline_config': {'name': 'train', 'batch_size': 64, 'num_epochs': None,
                                'shuffle': True},
            'x': X_train,
            'y': Y_train
        },
        'eval_input_data_config': {
            'input_type': plx.configs.InputDataConfig.NUMPY,
            'pipeline_config': {'name': 'eval', 'batch_size': 32, 'num_epochs': None,
                                'shuffle': False},
            'x': X_test,
            'y': Y_test
        },
        'estimator_config': {'output_dir': output_dir},
        'model_config': {
            'model_type': 'classifier',
            'loss_config': {'name': 'softmax_cross_entropy'},
            'eval_metrics_config': [{'name': 'streaming_accuracy'},
                                    {'name': 'streaming_precision'}],
            'optimizer_config': {'name': 'Adam', 'learning_rate': 0.008},
            'graph_config': {
                'name': 'mnist',
                'definition': [
                    (plx.layers.Conv2d, {'num_filter': 32, 'filter_size': 5, 'strides': 1}),
                    (plx.layers.MaxPool2d, {'kernel_size': 2}),
                    (plx.layers.Conv2d, {'num_filter': 64, 'filter_size': 5}),
                    (plx.layers.MaxPool2d, {'kernel_size': 2}),
                    (plx.layers.FullyConnected, {'n_units': 1024, 'activation': 'tanh'}),
                    (plx.layers.FullyConnected, {'n_units': 10}),
                ]
            }
        }
    }
    experiement_config = plx.configs.ExperimentConfig.read_configs(config)
    return plx.experiments.create_experiment(experiement_config)


def main(*args):
    plx.experiments.run_experiment(experiment_fn=create_experiment_json_fn,
                                   output_dir="/tmp/polyaxon_logs/lenet",
                                   schedule='continuous_train_and_eval')


if __name__ == "__main__":
    tf.logging.set_verbosity(tf.logging.INFO)
    tf.app.run()
