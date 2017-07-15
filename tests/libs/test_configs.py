# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict

import tensorflow as tf
import polyaxon as plx
from polyaxon.rl.utils import get_or_create_global_timestep


class TestConfigs(tf.test.TestCase):
    def test_run_config(self):
        config_dict = OrderedDict([
            ('master', None),
            ('num_cores', 0),
            ('log_device_placement', False),
            ('gpu_memory_fraction', 1),
            ('tf_random_seed', None),
            ('save_summary_steps', 100),
            ('save_checkpoints_secs', 600),
            ('save_checkpoints_steps', None),
            ('keep_checkpoint_max', 5),
            ('keep_checkpoint_every_n_hours', 10000),
            ('evaluation_master', ''),
            ('model_dir', None),
            ('cluster_config', None),
        ])
        config = plx.configs.RunConfig(**config_dict)

        assert config.to_dict() == config_dict

    def test_pipeline_config(self):
        config_dict = {'module': 'TFRecordImagePipeline',
                       'batch_size': 64,
                       'num_epochs': 10,
                       'shuffle': True, 'dynamic_pad': False,
                       'params': {
                           'data_files': 'train_data_file',
                           'meta_data_file': 'meta_data_file'
                       },
                       'definition': {
                           'image': [
                               (plx.processing.image.Standardization, {}),
                               (plx.layers.Reshape, {'new_shape': [28 * 28]}),
                           ]}
                       }

        pipeline_config = plx.configs.PipelineConfig.read_configs(config_dict)

        # Check that feature processing is done correctly
        assert pipeline_config.subgraph_configs_by_features is not None
        assert len(pipeline_config.subgraph_configs_by_features) == 1
        assert 'image' in pipeline_config.subgraph_configs_by_features
        assert isinstance(pipeline_config.subgraph_configs_by_features['image'],
                          plx.configs.SubGraphConfig)

        to_dict = pipeline_config.to_dict()
        for key in config_dict.keys():
            assert config_dict[key] == to_dict[key]

    def test_input_data_config(self):
        pipeline_input_data_config_dict = {
            'pipeline_config': {
                'module': 'TFRecordImagePipeline',
                'batch_size': 64,
                'num_epochs': 10,
                'shuffle': True, 'dynamic_pad': False,
                'params': {
                    'data_files': 'train_data_file',
                    'meta_data_file': 'meta_data_file'
                },
                'definition': {
                    'image': [
                        (plx.processing.image.Standardization, {}),
                        (plx.layers.Reshape, {'new_shape': [28 * 28]}),
                    ]}
            },
        }

        numpy_input_data_config_dict = {
            'input_type': 'NUMPY',
            'pipeline_config': {
                'name': 'train',
                'batch_size': 64,
                'num_epochs': None,
                'shuffle': False
            },
            'x': {'x': [1, 2, 3]},
            'y': [1, 2, 3]
        }

        pipeline_input_data_config = plx.configs.InputDataConfig.read_configs(
            pipeline_input_data_config_dict)

        numpy_input_data_config = plx.configs.InputDataConfig.read_configs(
            numpy_input_data_config_dict)

        assert isinstance(pipeline_input_data_config.pipeline_config, plx.configs.PipelineConfig)
        assert isinstance(numpy_input_data_config.pipeline_config, plx.configs.PipelineConfig)

        pipeline_input_data_to_dict = pipeline_input_data_config.to_dict()
        numpy_input_data_to_dict = numpy_input_data_config.to_dict()

        assert pipeline_input_data_to_dict['input_type'] is None
        assert numpy_input_data_to_dict['input_type'] == 'NUMPY'

        assert pipeline_input_data_to_dict['x'] is None
        assert numpy_input_data_to_dict['x'] == {'x': [1, 2, 3]}

        assert pipeline_input_data_to_dict['y'] is None
        assert numpy_input_data_to_dict['y'] == [1, 2, 3]

        for key in pipeline_input_data_config_dict['pipeline_config'].keys():
            assert (pipeline_input_data_to_dict['pipeline_config'][key] ==
                    pipeline_input_data_config_dict['pipeline_config'][key])

        for key in numpy_input_data_config_dict['pipeline_config'].keys():
            assert (numpy_input_data_to_dict['pipeline_config'][key] ==
                    numpy_input_data_config_dict['pipeline_config'][key])

        # create object
        input_data_pipeline_fn = plx.processing.create_input_data_fn(
            mode='train',
            pipeline_config=pipeline_input_data_config.pipeline_config)
        assert hasattr(input_data_pipeline_fn, '__call__')

        input_data_numpy_fn = plx.processing.create_input_data_fn(
            mode='train',
            pipeline_config=numpy_input_data_config.pipeline_config,
            input_type=numpy_input_data_config.input_type,
            x=numpy_input_data_config.x,
            y=numpy_input_data_config.y)
        assert hasattr(input_data_numpy_fn, '__call__')

    def test_environment_config(self):
        config_dict = {
            'module': 'GymEnvironment',
            'env_id': 'Pendulum-v0'
        }

        config = plx.configs.EnvironmentConfig.read_configs(config_dict)

        to_dict = config.to_dict()

        for key in config_dict.keys():
            assert to_dict[key] == config_dict[key]

        # create object
        env = plx.getters.get_environment(config.module, env_id=config.env_id, **config.params)
        assert isinstance(env, plx.rl.environments.GymEnvironment)

    def test_loss(self):
        config_dict = {
            'module': 'huber_loss',
            'params': {'collect': False}
        }

        config = plx.configs.LossConfig.read_configs(config_dict)

        to_dict = config.to_dict()

        for key in config_dict.keys():
            assert to_dict[key] == config_dict[key]

        # create object
        x = tf.constant(1)
        y = tf.constant(2)
        plx.getters.get_loss(config.module, y, x, **config.params)
        assert plx.utils.get_tracked(tf.GraphKeys.LOSSES) == []

        # now with Tracking, this is just to test that params are passed correctly
        config_dict = {
            'module': 'huber_loss',
            'params': {'collect': True}
        }
        config = plx.configs.LossConfig.read_configs(config_dict)
        plx.getters.get_loss(config.module, y, x, **config.params)
        assert len(plx.utils.get_tracked(tf.GraphKeys.LOSSES)) == 1

    def test_metric_config(self):
        config_dict = {'module': 'streaming_auc'}

        config = plx.configs.MetricConfig.read_configs(config_dict)

        to_dict = config.to_dict()

        for key in config_dict.keys():
            assert to_dict[key] == config_dict[key]

        # create object
        x = tf.constant(1)
        y = tf.constant(2)
        plx.getters.get_eval_metric(config.module, y, x, **config.params)

    def test_exploration_confg(self):
        config_dict = {'module': 'decay'}

        config = plx.configs.ExplorationConfig.read_configs(config_dict)

        to_dict = config.to_dict()

        for key in config_dict.keys():
            assert to_dict[key] == config_dict[key]

        # create object
        get_or_create_global_timestep()
        plx.getters.get_exploration(config.module, is_continuous=False, **config.params)
        plx.getters.get_exploration(
            config.module, is_continuous=True, num_actions=1, **config.params)

    def test_optimizer(self):
        config_dict = {
            'module': 'adam',
            'learning_rate': 0.001,
            'decay_steps': 100
        }

        config = plx.configs.OptimizerConfig.read_configs(config_dict)

        to_dict = config.to_dict()

        for key in config_dict.keys():
            assert to_dict[key] == config_dict[key]

        # create object
        plx.getters.get_optimizer(config.module, **config.params)

    def test_memory_config(self):
        config_dict = {
            'module': 'Memory',
            'params': {
                'num_states': 4,
                'num_actions': 2,
                'is_continuous': False,
                'size': 10
            }
        }
        config = plx.configs.MemoryConfig.read_configs(config_dict)

        to_dict = config.to_dict()

        for key in config_dict.keys():
            assert to_dict[key] == config_dict[key]


        # create object
        memory = plx.getters.get_memory(config.module, **config.params)
        assert memory.state.shape == (10, 4)
        assert memory.action.shape == (10, )

    def test_subgraph_config(self):
        graph_config_dict = {
            'name': 'graph',
            'definition': [
                (
                    plx.layers.Merge,
                    {
                        'merge_mode': 'prod',
                        'modules': [
                            {
                                'name': 'subgraph1',
                                'definition': [
                                    (
                                        plx.layers.FullyConnected,
                                        {'num_units': 10, 'activation': 'tanh'}
                                    ),
                                    (
                                        plx.layers.FullyConnected,
                                        {'num_units': 2, 'activation': 'tanh'}
                                    ),
                                ]
                            },
                            {
                                'name': 'subgraph2',
                                'definition': [
                                    (
                                        plx.layers.FullyConnected,
                                        {'num_units': 10, 'activation': 'relu'}
                                    ),
                                    (
                                        plx.layers.Dropout,
                                        {'keep_prob': 0.8}
                                    ),
                                    (
                                        plx.layers.FullyConnected,
                                        {'num_units': 10, 'activation': 'relu'}
                                    ),
                                ]
                            },
                        ]
                    }
                ),
            ]
        }

        graph_config = plx.configs.SubGraphConfig.read_configs(config_values=graph_config_dict)
        graph_config_dict_result = graph_config.to_dict()

        assert graph_config_dict['name'] == graph_config_dict_result['name']

        expected_definition = graph_config_dict['definition']
        result_definition = graph_config_dict_result['definition']

        assert len(expected_definition) == len(result_definition)
        assert expected_definition[0][0] == result_definition[0][0]
        assert expected_definition[0][1].keys() == result_definition[0][1].keys()

        expected_modules = expected_definition[0][1]['modules']
        result_modules = result_definition[0][1]['modules']

        for i, expected_module in enumerate(expected_modules):
            result_module = result_modules[i]
            assert expected_module['name'] == result_module['name']
            expected_module_def = expected_module['definition']
            result_module_def = result_module['definition']
            assert len(expected_module_def) == len(result_module_def)
            for j, m_def in enumerate(result_module_def):
                assert m_def[0] == expected_module_def[j][0]
                assert m_def[1].keys() == expected_module_def[j][1].keys()
                for e_val, r_val in zip(m_def[1].values(), expected_module_def[j][1].values()):
                    assert e_val == r_val

    def test_simple_subgraph_config(self):
        config_dict = {
            'definition': [
                (plx.layers.Conv2d,
                 {'num_filter': 32, 'filter_size': 3, 'strides': 1, 'activation': 'relu',
                  'regularizer': 'l2_regularizer'}),
                (plx.layers.MaxPool2d, {'kernel_size': 2}),
                (plx.layers.Conv2d, {'num_filter': 32, 'filter_size': 3, 'activation': 'relu',
                                     'regularizer': 'l2_regularizer'}),
                (plx.layers.MaxPool2d, {'kernel_size': 2}),
            ]
        }

        config = plx.configs.SubGraphConfig.read_configs(config_values=config_dict)
        config_dict_def = config_dict['definition']
        to_dict_def = config.to_dict()['definition']

        for j, m_def in enumerate(config_dict_def):
            assert m_def[0] == to_dict_def[j][0]
            assert m_def[1].keys() == to_dict_def[j][1].keys()
            for e_val, r_val in zip(m_def[1].values(), to_dict_def[j][1].values()):
                assert e_val == r_val

    def test_model_config(self):
        config_dict = {
            'module': 'Generator',
            'summaries': ['loss'],
            'optimizer_config': {'module': 'adadelta', 'learning_rate': 0.9},
            'encoder_config': {
                'definition': [
                    (plx.layers.FullyConnected, {'num_units': 128}),
                    (plx.layers.FullyConnected, {'num_units': 256}),
                ]
            },
            'decoder_config': {
                'definition': [
                    (plx.layers.FullyConnected, {'num_units': 256}),
                    (plx.layers.FullyConnected, {'num_units': 28 * 28}),
                ]
            },
            'bridge_config': {'module': 'LatentBridge'}
        }

        config = plx.configs.ModelConfig.read_configs(config_values=config_dict)
        assert config.module == 'Generator'
        assert config.summaries == ['loss']
        assert isinstance(config.optimizer_config, plx.configs.OptimizerConfig)
        assert isinstance(config.encoder_config, plx.configs.SubGraphConfig)
        assert isinstance(config.decoder_config, plx.configs.SubGraphConfig)
        assert isinstance(config.bridge_config, plx.configs.BridgeConfig)
        assert config.graph_config is None

        to_dict = config.to_dict()

        assert to_dict['module'] == config_dict['module']
        assert to_dict['summaries'] == config_dict['summaries']
        for key in config_dict['optimizer_config'].keys():
            assert to_dict['optimizer_config'][key] == config_dict['optimizer_config'][key]
        for key in config_dict['encoder_config'].keys():
            assert to_dict['encoder_config'][key] == config_dict['encoder_config'][key]
        for key in config_dict['decoder_config'].keys():
            assert to_dict['decoder_config'][key] == config_dict['decoder_config'][key]
        for key in config_dict['bridge_config'].keys():
            assert to_dict['bridge_config'][key] == config_dict['bridge_config'][key]

    def test_estimator_config(self):
        config_dict = {
            'module': 'Estimator',
            'output_dir': 'output_dir',
        }
        config = plx.configs.EstimatorConfig.read_configs(config_values=config_dict)
        to_dict = config.to_dict()

        for key in config_dict.keys():
            assert to_dict[key] == config_dict[key]

    def test_experiment_config(self):
        config_dict = {
            'name': 'vgg19',
            'output_dir': 'output_dir',
            'eval_every_n_steps': 10,
            'train_steps_per_iteration': 100,
            'run_config': {'save_checkpoints_steps': 100},
            'train_input_data_config': {
                'pipeline_config': {'module': 'TFRecordImagePipeline', 'batch_size': 64,
                                    'num_epochs': 1,
                                    'shuffle': True, 'dynamic_pad': False,
                                    'params': {'data_files': 'train_data_file',
                                               'meta_data_file': 'meta_data_file'}},
            },
            'eval_input_data_config': {
                'pipeline_config': {'module': 'TFRecordImagePipeline', 'batch_size': 32,
                                    'num_epochs': 1,
                                    'shuffle': True, 'dynamic_pad': False,
                                    'params': {'data_files': '/data_file',
                                               'meta_data_file': '/meta_data_file'}},
            },
            'estimator_config': {'output_dir': 'output_dir'},
            'model_config': {
                'module': 'Classifier',
                'summaries': ['loss'],
                'loss_config': {'module': 'softmax_cross_entropy'},
                'eval_metrics_config': [{'module': 'streaming_accuracy', 'params': {}},
                                        {'module': 'streaming_precision', 'params': {}}],
                'optimizer_config': {'module': 'adam', 'learning_rate': 0.007,
                                     'decay_type': 'exponential_decay', 'decay_rate': 0.2},
                'one_hot_encode': True,
                'n_classes': 17,
                'graph_config': {
                    'name': 'vgg',
                    'features': ['image'],
                    'definition': [
                        ('Conv2d', {'num_filter': 64, 'filter_size': 3,
                                             'activation': 'relu'}),
                        ('Conv2d', {'num_filter': 64, 'filter_size': 3,
                                             'activation': 'relu'}),
                        ('MaxPool2d', {'kernel_size': 2, 'strides': 2}),

                        ('Conv2d', {'num_filter': 128, 'filter_size': 3,
                                             'activation': 'relu'}),
                        ('Conv2d', {'num_filter': 128, 'filter_size': 3,
                                             'activation': 'relu'}),
                        ('MaxPool2d', {'kernel_size': 2, 'strides': 2}),

                        ('Conv2d', {'num_filter': 256, 'filter_size': 3,
                                             'activation': 'relu'}),
                        ('Conv2d', {'num_filter': 256, 'filter_size': 3,
                                             'activation': 'relu'}),
                        ('Conv2d', {'num_filter': 256, 'filter_size': 3,
                                             'activation': 'relu'}),
                        ('MaxPool2d', {'kernel_size': 2, 'strides': 2}),

                        ('Conv2d', {'num_filter': 512, 'filter_size': 3,
                                             'activation': 'relu'}),
                        ('Conv2d', {'num_filter': 512, 'filter_size': 3,
                                             'activation': 'relu'}),
                        ('Conv2d', {'num_filter': 512, 'filter_size': 3,
                                             'activation': 'relu'}),
                        ('MaxPool2d', {'kernel_size': 2, 'strides': 2}),

                        ('FullyConnected', {'num_units': 4096, 'activation': 'relu',
                                                     'dropout': 0.5}),
                        ('FullyConnected', {'num_units': 4096, 'activation': 'relu',
                                                     'dropout': 0.5}),
                        ('FullyConnected', {'num_units': 17}),
                    ]
                }
            }
        }

        config = plx.configs.ExperimentConfig.read_configs(config_values=config_dict)
        to_dict = config.to_dict()
        assert to_dict['name'] == config_dict['name']
        assert to_dict['output_dir'] == config_dict['output_dir']
        assert to_dict['eval_every_n_steps'] == config_dict['eval_every_n_steps']
        assert to_dict['train_steps_per_iteration'] == config_dict['train_steps_per_iteration']

        assert (to_dict['run_config']['save_checkpoints_steps'] ==
                config_dict['run_config']['save_checkpoints_steps'])

        assert (to_dict['train_input_data_config']['pipeline_config']['module'] ==
                config_dict['train_input_data_config']['pipeline_config']['module'])

        assert (to_dict['eval_input_data_config']['pipeline_config']['module'] ==
                config_dict['eval_input_data_config']['pipeline_config']['module'])

        assert (to_dict['estimator_config']['output_dir'] ==
                config_dict['estimator_config']['output_dir'])

        assert to_dict['model_config']['module'] == config_dict['model_config']['module']
        assert to_dict['model_config']['summaries'] == config_dict['model_config']['summaries']
        assert (to_dict['model_config']['one_hot_encode'] ==
                config_dict['model_config']['one_hot_encode'])
        assert (to_dict['model_config']['n_classes'] ==
                config_dict['model_config']['n_classes'])
        assert (to_dict['model_config']['eval_metrics_config'] ==
                config_dict['model_config']['eval_metrics_config'])

        for key in config_dict['model_config']['loss_config'].keys():
            assert (to_dict['model_config']['loss_config'][key] ==
                    config_dict['model_config']['loss_config'][key])

        for key in config_dict['model_config']['optimizer_config'].keys():
            assert (to_dict['model_config']['optimizer_config'][key] ==
                    config_dict['model_config']['optimizer_config'][key])

        graph_config = config_dict['model_config']['graph_config']['definition']
        to_dict_graph_config = to_dict['model_config']['graph_config']['definition']
        for j, m_def in enumerate(graph_config):
            assert m_def[0] == to_dict_graph_config[j][0]
            assert m_def[1].keys() == to_dict_graph_config[j][1].keys()
            for e_val, r_val in zip(m_def[1].values(), to_dict_graph_config[j][1].values()):
                assert e_val == r_val

        # create object
        plx.experiments.create_experiment(config)

    def test_rl_experiment_config(self):
        config_dict = {
            'name': 'dqn_cartpole',
            'output_dir': 'output_dir',
            'agent_config': {
                'output_dir': 'output_dir',
                'memory_config': {
                    'module': 'Memory',
                    'params': {
                        'num_states': 4,
                        'num_actions': 2,
                        'is_continuous': False,
                        'size': 10
                    }
                }
            },
            'environment_config': {'module': 'GymEnvironment', 'env_id': 'CartPole-v0'},
            'model_config': {
                'module': 'DQNModel',
                'summaries': 'all',
                'loss_config': {'module': 'huber_loss'},
                'optimizer_config': {'module': 'adam', 'learning_rate': 0.007,
                                     'decay_type': 'exponential_decay', 'decay_rate': 0.2},
                'exploration_config': {'module': 'decay'},
                'num_actions': 2,
                'num_states': 4,
                'graph_config': {
                    'definition': [
                        ('FullyConnected', {'num_units': 512})
                    ]
                }
            }
        }

        config = plx.configs.RLExperimentConfig.read_configs(config_values=config_dict)
        to_dict = config.to_dict()
        assert to_dict['name'] == config_dict['name']
        assert to_dict['output_dir'] == config_dict['output_dir']

        for key in config_dict['agent_config'].keys():
            assert to_dict['agent_config'][key] == config_dict['agent_config'][key]

        for key in config_dict['environment_config'].keys():
            assert to_dict['environment_config'][key] == config_dict['environment_config'][key]

        assert to_dict['model_config']['module'] == config_dict['model_config']['module']
        assert to_dict['model_config']['summaries'] == config_dict['model_config']['summaries']
        assert (to_dict['model_config']['num_actions'] ==
                config_dict['model_config']['num_actions'])
        assert (to_dict['model_config']['num_states'] ==
                config_dict['model_config']['num_states'])

        for key in config_dict['model_config']['exploration_config'].keys():
            assert (to_dict['model_config']['exploration_config'][key] ==
                    config_dict['model_config']['exploration_config'][key])

        for key in config_dict['model_config']['loss_config'].keys():
            assert (to_dict['model_config']['loss_config'][key] ==
                    config_dict['model_config']['loss_config'][key])

        for key in config_dict['model_config']['optimizer_config'].keys():
            assert (to_dict['model_config']['optimizer_config'][key] ==
                    config_dict['model_config']['optimizer_config'][key])

        graph_config = config_dict['model_config']['graph_config']['definition']
        to_dict_graph_config = to_dict['model_config']['graph_config']['definition']
        for j, m_def in enumerate(graph_config):
            assert m_def[0] == to_dict_graph_config[j][0]
            assert m_def[1].keys() == to_dict_graph_config[j][1].keys()
            for e_val, r_val in zip(m_def[1].values(), to_dict_graph_config[j][1].values()):
                assert e_val == r_val

        plx.experiments.create_rl_experiment(config)
