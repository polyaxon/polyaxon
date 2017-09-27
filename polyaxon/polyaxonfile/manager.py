# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.eval import EvalConfig
from polyaxon_schemas.polyaxonfile.polyaxonfile import PolyaxonFile
from polyaxon_schemas.train import TrainConfig

from experiments import Experiment
from polyaxon import Modes, getters
from polyaxon.estimators.run_config import RunConfig
from polyaxon.processing.input_data import create_input_data_fn


def _get_train(config):
    assert isinstance(config, TrainConfig), '`config` must be a an instance of `TrainConfig`'

    input_fn = create_input_data_fn(
        mode=Modes.TRAIN,
        pipeline_config=config.data_pipeline
    )
    return input_fn, config.steps, config.hooks


def _get_eval(config):
    assert isinstance(config, EvalConfig), '`config` must be a an instance of `EvalConfig`'

    input_fn = create_input_data_fn(
        mode=Modes.EVAL,
        pipeline_config=config.data_pipeline
    )
    return (input_fn,
            config.steps,
            config.hooks,
            config.delay_secs,
            config.continuous_eval_throttle_secs)


def _get_local_cluster(num_workers, num_ps):
    host = '127.0.0.1'
    master_port = 10000
    worker_port = 11000
    ps_port = 12000

    def get_address(port):
        return '{}:{}'.format(host, port)

    cluster_config = {
        'master': [get_address(master_port)]
    }

    workers = []
    for i in range(num_workers):
        workers.append(get_address(worker_port))
        worker_port += 1

    if workers:
        cluster_config['worker'] = workers

    ps = []
    for i in range(num_ps):
        ps.append(get_address(ps_port))
        ps_port += 1

    if ps:
        cluster_config['ps'] = ps

    return cluster_config


def _get_run_configs(environement):
    def get_master_config(config):
        return RunConfig.from_config(config)

    config = environement.run_config or RunConfig.CONFIG()

    num_workers = environement.n_workers or 0
    num_ps = environement.n_ps or 0

    if not num_workers and not num_ps:
        return {'master': get_master_config(config)}, False

    cluster_config = _get_local_cluster(num_workers, num_ps)
    config.cluster = cluster_config

    configs = {'master': get_master_config(config)}

    if num_workers > 0:
        configs['workers'] = []

    if num_ps > 0:
        configs['ps'] = []

    worker_session_configs = {}
    for session_config in environement.worker_configs or []:
        worker_session_configs[session_config.index] = session_config

    ps_session_configs = {}
    for session_config in environement.ps_configs or []:
        ps_session_configs[session_config.index] = session_config

    default_worker_config = environement.default_worker_config
    for i in range(num_workers):
        config = get_master_config(config)
        session_config = worker_session_configs.get(i, default_worker_config)
        if session_config:
            session_config = RunConfig.get_session_config(session_config)
            config = config.replace(session_config=session_config)

        configs['workers'].append(config)

    default_ps_config = environement.default_ps_config
    for i in range(num_ps):
        config = get_master_config(config)
        session_config = ps_session_configs.get(i, default_ps_config)
        if session_config:
            session_config = RunConfig.get_session_config(session_config)
            config = config.replace(session_config=session_config)

        configs['ps'].append(config)

    return configs, True


def prepare_experiments(polyaxonfil):
    plx_file = PolyaxonFile(polyaxonfil)
    is_distributed = False

    if not plx_file.settings.environement:
        configs = {'master': [RunConfig()]}
        delay_workers_by_global_step = False
    else:
        configs, is_distributed = _get_run_configs(plx_file.settings.environement)
        delay_workers_by_global_step = plx_file.settings.environement.delay_workers_by_global_step

    train_input_fn, train_steps, train_hooks = _get_train(plx_file.train)
    (eval_input_fn, eval_steps, eval_hooks, eval_delay_secs,
     continuous_eval_throttle_secs) = _get_eval(plx_file.eval)

    def get_experiment(config):
        estimator = getters.get_estimator(plx_file.model,
                                          config,
                                          output_dir=plx_file.project_path)

        return Experiment(
            estimator=estimator,
            train_input_fn=train_input_fn,
            eval_input_fn=eval_input_fn,
            train_steps=train_steps,
            eval_steps=eval_steps,
            train_hooks=train_hooks,
            eval_hooks=eval_hooks,
            eval_delay_secs=eval_delay_secs,
            continuous_eval_throttle_secs=continuous_eval_throttle_secs,
            delay_workers_by_global_step=delay_workers_by_global_step,
            export_strategies=plx_file.settings.export_strategies)

    master_xp = get_experiment(configs['master'][0])
    if not is_distributed:
        return get_experiment(configs['master'][0])

    xps = [master_xp]

    for i_config in configs.get('workers', []):
        xps.append(get_experiment(i_config))

    for i_config in configs.get('ps', []):
        xps.append(get_experiment(i_config))

    return xps
