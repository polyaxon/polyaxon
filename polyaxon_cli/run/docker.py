# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os
import shutil
import sys
import tempfile

from hestia.user_path import polyaxon_user_path
from polyaxon_deploy.operators.docker import DockerOperator
from polyaxon_dockerizer import build as dockerizer_build
from polyaxon_dockerizer import generate as dockerizer_generate

from polyaxon_cli.client.exceptions import (
    PolyaxonClientException,
    PolyaxonHTTPError,
    PolyaxonShouldExitError
)
from polyaxon_cli.client.tracking import (
    POLYAXON_NO_OP_KEY,
    TMP_POLYAXON_PATH,
    BuildJob,
    Experiment,
    hash_value
)
from polyaxon_cli.exceptions import PolyaxonConfigurationError
from polyaxon_cli.schemas import BuildSpecification
from polyaxon_cli.utils.formatting import Printer

POLYAXON_DOCKERFILE_NAME = 'Dockerfile'
POLYAXON_DATA_PATH = os.path.join(TMP_POLYAXON_PATH, 'data')


def _get_env_vars(project, experiment_id):
    env_vars = [
        ('POLYAXON_IS_MANAGED', 'true'),
        ('POLYAXON_IS_LOCAL', 'true'),
        ('POLYAXON_EXPERIMENT_INFO', json.dumps({
            'project_name': project,
            'experiment_name': '{}.{}'.format(project, experiment_id)})),
    ]
    if POLYAXON_NO_OP_KEY in os.environ:
        env_vars += [('POLYAXON_NO_OP', 'true')]

    # TODO: use user's (data/outputs) paths
    env_vars += [('POLYAXON_RUN_DATA_PATHS', json.dumps({'local': '/tmp'}))]
    env_vars += [('POLYAXON_RUN_OUTPUTS_PATH', '/tmp')]

    return env_vars


def _get_config_volume():
    return ['-v', '{}:{}'.format(polyaxon_user_path(), TMP_POLYAXON_PATH)]


def _get_data_volumes(data_path):
    return ['-v', '{}:{}'.format(data_path, POLYAXON_DATA_PATH)]


def _create_docker_build(build_job, build_config):
    directory = tempfile.mkdtemp()
    build_context = build_config.context or '.'
    try:
        dst_path = os.path.join(directory, "code")
        shutil.copytree(src=build_context, dst=dst_path)
        dockerfile_path = POLYAXON_DOCKERFILE_NAME
        dockerfile_generate = True
        if build_config.dockerfile:
            shutil.copy(build_config.dockerfile, os.path.join(directory, dockerfile_path))
            dockerfile_generate = False
        if dockerfile_generate:
            rendered_dockerfile = dockerizer_generate(
                repo_path=dst_path,
                from_image=build_config.image,
                build_steps=build_config.build_steps,
                env_vars=build_config.env_vars,
                lang_env=build_config.lang_env,
            )
        else:
            with open(dockerfile_path) as dockerfile:
                rendered_dockerfile = dockerfile

        if rendered_dockerfile:
            build_job.log_dockerfile(dockerfile=rendered_dockerfile)
        else:
            message = 'Failed to generate the dockerfile.'
            Printer.print_error(message)
            build_job.failed(message=message)
            raise PolyaxonShouldExitError('')

        image_tag = hash_value(rendered_dockerfile)
        image_name = build_job.job['unique_name'].replace('.', '-')

        dockerizer_build(build_context=directory,
                         image_tag=image_tag,
                         image_name=image_name,
                         nocache=build_config.nocache)
        build_job.succeeded()
    finally:
        shutil.rmtree(directory)
    return '{}:{}'.format(image_name, image_tag)


def _run(ctx, name, user, project_name, description, tags, specification, log):
    docker = DockerOperator()
    if not docker.check():
        raise PolyaxonConfigurationError('Docker is required to run this command.')

    # Create Build
    project = '{}.{}'.format(user, project_name)
    build_job = BuildJob(project=project, track_logs=False)

    build_spec = BuildSpecification.create_specification(specification.build, to_dict=False)
    build_spec.apply_context()
    build_config = build_spec.config
    build_job.create(name=name,
                     description=description,
                     tags=tags,
                     content=build_spec.raw_data)
    image = _create_docker_build(build_job, build_config)

    experiment = Experiment(project=project, track_logs=False)
    experiment.create(name=name,
                      tags=tags,
                      description=description,
                      build_id=build_job.job_id,
                      content=specification.raw_data)

    cmd_args = ['run', '--rm']
    for key, value in _get_env_vars(project=project, experiment_id=experiment.experiment_id):
        cmd_args += ['-e', '{key}={value}'.format(key=key, value=value)]
    cmd_args += _get_config_volume()
    cmd_args += [image]

    # Add cmd.run
    for arg in specification.run.get_container_cmd():
        cmd_args += arg
    try:
        print(cmd_args)
        docker.execute(cmd_args, stream=True)
    except Exception as e:
        Printer.print_error('Could start local run.')
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)


def run(ctx, name, user, project_name, description, tags, specification, log):
    try:
        _run(ctx, name, user, project_name, description, tags, specification, log)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could start local run.')
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)
    except Exception as e:
        Printer.print_error('Could start local run.')
        Printer.print_error('Unexpected Error: `{}`.'.format(e))
        sys.exit(1)
