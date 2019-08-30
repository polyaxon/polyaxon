# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import os
import shutil
import sys
import tempfile
import time

from hestia.user_path import polyaxon_user_path
from polyaxon_deploy.operators.docker import DockerOperator
from polyaxon_dockerizer import build as dockerizer_build
from polyaxon_dockerizer import constants as dockerizer_constants
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
POLYAXON_DATA_PATH = '/tmp/data'


def _get_env_vars(project, experiment_id, params, data_paths=None):
    env_vars = [
        ('POLYAXON_IS_MANAGED', 'true'),
        ('POLYAXON_IS_LOCAL', 'true'),
        ('POLYAXON_EXPERIMENT_INFO', json.dumps({
            'project_name': project,
            'experiment_name': '{}.{}'.format(project, experiment_id)})),
    ]
    if POLYAXON_NO_OP_KEY in os.environ:
        env_vars += [(POLYAXON_NO_OP_KEY, 'true')]
    if 'POLYAXON_IS_OFFLINE' in os.environ:
        env_vars += [('POLYAXON_IS_OFFLINE', 'true')]

    paths = {'local': '/tmp'}

    if data_paths:
        paths.update(data_paths)

    env_vars += [('POLYAXON_PARAMS', json.dumps(params))]
    env_vars += [('POLYAXON_RUN_DATA_PATHS', json.dumps(paths))]
    env_vars += [('POLYAXON_RUN_OUTPUTS_PATH', '/tmp/outputs')]

    return env_vars


def _get_config_volume():
    return ['-v', '{}:{}'.format(polyaxon_user_path(), TMP_POLYAXON_PATH)]


def _get_data_bind_mounts(mount_refs=None):
    data_paths = {}
    bind_mounts = {}

    if not mount_refs:
        return data_paths, bind_mounts

    for dpath in mount_refs:
        parts = dpath.split(':')
        if len(parts) >= 2:
            ref = parts[1]
            data_ref_path = os.path.join(POLYAXON_DATA_PATH, ref)
            host_path = os.path.abspath(os.path.expanduser(parts[0]))
            data_paths[ref] = data_ref_path
            bind_mounts[host_path] = data_ref_path
        else:
            # we have just data ref name
            ref = parts[0]
            data_ref_path = os.path.join(POLYAXON_DATA_PATH, ref)
            data_paths[ref] = data_ref_path
    return data_paths, bind_mounts


def _get_data_volumes(bind_mounts):
    result = []
    for host_path, mount_path in bind_mounts.items():
        result += ['-v', '{}:{}'.format(host_path, mount_path)]
    return result


def _create_docker_build(build_job, build_config, project):
    directory = tempfile.mkdtemp()
    build_context = build_config.context or '.'
    try:
        dst_path = os.path.join(directory, dockerizer_constants.REPO_PATH)
        shutil.copytree(src=build_context, dst=dst_path)
        dockerfile_path = POLYAXON_DOCKERFILE_NAME
        dockerfile_generate = True
        if build_config.dockerfile:
            dockerfile_path = os.path.join(directory, dockerfile_path)
            shutil.copy(build_config.dockerfile, dockerfile_path)
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
        if 'POLYAXON_IS_OFFLINE' not in os.environ:
            job_name = build_job.job['unique_name']
        else:
            job_name = "{project}-builds-local-{timestamp}".format(
                project=project, timestamp=int(time.time()))

        image_name = job_name.replace('.', '-')

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
    image = _create_docker_build(build_job, build_config, project)

    experiment = Experiment(project=project, track_logs=False)
    experiment.create(name=name,
                      tags=tags,
                      description=description,
                      build_id=build_job.job_id,
                      content=specification.raw_data)

    cmd_args = ['run', '--rm']
    data_paths, bind_mounts = _get_data_bind_mounts(specification.data_refs)
    for key, value in _get_env_vars(
            project=project,
            experiment_id=experiment.experiment_id,
            params=specification.params,
            data_paths=data_paths):
        cmd_args += ['-e', '{key}={value}'.format(key=key, value=value)]
    cmd_args += _get_config_volume()
    cmd_args += _get_data_volumes(bind_mounts)
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
