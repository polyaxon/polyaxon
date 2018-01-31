# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json
import logging
import uuid

from django.conf import settings
from kubernetes.client.rest import ApiException

from polyaxon_schemas.utils import TaskType
from rest_framework import fields

from jobs.models import JobResources
from polyaxon.utils import config
from experiments.serializers import ExperimentJobDetailSerializer
from repos.dockerize import get_image_info

from spawner import K8SSpawner, K8SProjectSpawner
from experiments.models import ExperimentJob
from spawner.utils.constants import ExperimentLifeCycle

logger = logging.getLogger('polyaxon.scheduler')


def create_job(job_uuid, experiment, definition, role=None, resources=None):
    job = ExperimentJob(uuid=job_uuid,
                        experiment=experiment,
                        definition=definition)
    if role:
        job.role = role

    if not resources:
        job.save()
        return

    job_resources = {}
    if resources.memory:
        job_resources['memory'] = resources.memory.to_dict()
    if resources.cpu:
        job_resources['cpu'] = resources.cpu.to_dict()
    if resources.gpu:
        job_resources['gpu'] = resources.gpu.to_dict()
    if job_resources:
        job.resources = JobResources.objects.create(**job_resources)
    job.save()


def start_experiment(experiment):
    # Update experiment status to show that its started
    experiment.set_status(ExperimentLifeCycle.SCHEDULED)

    project = experiment.project
    group = experiment.experiment_group

    job_docker_image = None  # This will force the spawner to use the default docker image
    if experiment.compiled_spec.run_exec:
        try:
            image_name, image_tag = get_image_info(experiment=experiment)
        except ValueError as e:
            logger.warning('Could not start the experiment, %s', e)
            experiment.set_status(ExperimentLifeCycle.FAILED,
                                  message='External git repo was note found.')
            return
        job_docker_image = '{}:{}'.format(image_name, image_tag)
        logger.info('Start experiment with built image `{}`'.format(job_docker_image))
    else:
        logger.info('Start experiment with default image.')

    # Use spawner to start the experiment
    spawner = K8SSpawner(project_name=project.unique_name,
                         experiment_name=experiment.unique_name,
                         experiment_group_name=group.unique_name if group else None,
                         project_uuid=project.uuid.hex,
                         experiment_group_uuid=group.uuid.hex if group else None,
                         experiment_uuid=experiment.uuid.hex,
                         spec_config=experiment.config,
                         k8s_config=settings.K8S_CONFIG,
                         namespace=settings.K8S_NAMESPACE,
                         in_cluster=True,
                         job_docker_image=job_docker_image,
                         use_sidecar=True,
                         sidecar_config=config.get_requested_params(to_str=True))
    try:
        resp = spawner.start_experiment(user_token=experiment.user.auth_token.key)
    except ApiException as e:
        logger.warning('Could not start the experiment, please check your polyaxon spec %s', e)
        experiment.set_status(
            ExperimentLifeCycle.FAILED,
            message='Could not start the experiment, encountered a Kubernetes ApiException.')
        return
    except Exception as e:
        logger.warning('Could not start the experiment, please check your polyaxon spec %s', e)
        experiment.set_status(
            ExperimentLifeCycle.FAILED,
            message='Could not start the experiment encountered an {} exception.'.format(
                e.__class__.__name__
            ))
        return

    # Get the number of jobs this experiment started
    master = resp[TaskType.MASTER]
    job_uuid = master['pod']['metadata']['labels']['job_uuid']
    job_uuid = uuid.UUID(job_uuid)

    def get_definition(definition):
        serializer = ExperimentJobDetailSerializer(data={
            'definition': json.dumps(definition, default=fields.DateTimeField().to_representation)
        })
        serializer.is_valid()
        return json.loads(serializer.validated_data['definition'])

    create_job(job_uuid=job_uuid,
               experiment=experiment,
               definition=get_definition(master),
               resources=spawner.spec.master_resources)

    for i, worker in enumerate(resp[TaskType.WORKER]):
        job_uuid = worker['pod']['metadata']['labels']['job_uuid']
        job_uuid = uuid.UUID(job_uuid)
        create_job(job_uuid=job_uuid,
                   experiment=experiment,
                   definition=get_definition(worker),
                   role=TaskType.WORKER,
                   resources=spawner.spec.worker_resources.get(i))
    for i, ps in enumerate(resp[TaskType.PS]):
        job_uuid = ps['pod']['metadata']['labels']['job_uuid']
        job_uuid = uuid.UUID(job_uuid)
        create_job(job_uuid=job_uuid,
                   experiment=experiment,
                   definition=get_definition(ps),
                   role=TaskType.PS,
                   resources=spawner.spec.ps_resources.get(i))


def stop_experiment(experiment, update_status=False):
    project = experiment.project
    group = experiment.experiment_group
    spawner = K8SSpawner(project_name=project.unique_name,
                         experiment_name=experiment.unique_name,
                         experiment_group_name=group.unique_name if group else None,
                         project_uuid=project.uuid.hex,
                         experiment_group_uuid=group.uuid.hex if group else None,
                         experiment_uuid=experiment.uuid.hex,
                         spec_config=experiment.config,
                         k8s_config=settings.K8S_CONFIG,
                         namespace=settings.K8S_NAMESPACE,
                         in_cluster=True,
                         use_sidecar=True,
                         sidecar_config=config.get_requested_params(to_str=True))
    spawner.stop_experiment()
    if update_status:
        # Update experiment status to show that its deleted
        experiment.set_status(ExperimentLifeCycle.DELETED)


def start_tensorboard(project):
    spawner = K8SProjectSpawner(project_name=project.unique_name,
                                project_uuid=project.uuid.hex,
                                k8s_config=settings.K8S_CONFIG,
                                namespace=settings.K8S_NAMESPACE,
                                in_cluster=True)

    spawner.start_tensorboard()
    project.has_tensorboard = True
    project.save()


def stop_tensorboard(project):
    spawner = K8SProjectSpawner(project_name=project.unique_name,
                                project_uuid=project.uuid.hex,
                                k8s_config=settings.K8S_CONFIG,
                                namespace=settings.K8S_NAMESPACE,
                                in_cluster=True)

    spawner.stop_tensorboard()
    project.has_tensorboard = False
    project.save()
