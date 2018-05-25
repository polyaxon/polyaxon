import json
import logging
import uuid

from kubernetes.client.rest import ApiException
from rest_framework import fields

from django.conf import settings

from api.experiments.serializers import ExperimentJobDetailSerializer
from constants.experiments import ExperimentLifeCycle
from db.models.experiments import ExperimentJob
from db.models.jobs import JobResources
from docker_images.image_info import get_experiment_image_info
from polyaxon.utils import config
from polyaxon_schemas.polyaxonfile.specification.frameworks import (
    HorovodSpecification,
    MXNetSpecification,
    PytorchSpecification,
    TensorflowSpecification
)
from polyaxon_schemas.utils import Frameworks, TaskType
from scheduler.spawners.experiment_spawner import ExperimentSpawner
from scheduler.spawners.horovod_spawner import HorovodSpawner
from scheduler.spawners.mxnet_spawner import MXNetSpawner
from scheduler.spawners.pytorch_spawner import PytorchSpawner
from scheduler.spawners.tensorflow_spawner import TensorflowSpawner

logger = logging.getLogger('polyaxon.scheduler.experiment')


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
        _resources = resources.memory.to_dict()
        if any(_resources.values()):
            job_resources['memory'] = _resources
    if resources.cpu:
        _resources = resources.cpu.to_dict()
        if any(_resources.values()):
            job_resources['cpu'] = _resources
    if resources.gpu:
        _resources = resources.gpu.to_dict()
        if any(_resources.values()):
            job_resources['gpu'] = _resources
    if job_resources:
        job.resources = JobResources.objects.create(**job_resources)
    job.save()


def get_job_definition(definition):
    serializer = ExperimentJobDetailSerializer(data={
        'definition': json.dumps(definition, default=fields.DateTimeField().to_representation)
    })
    serializer.is_valid()
    return json.loads(serializer.validated_data['definition'])


def get_spawner_class(framework):
    if framework == Frameworks.TENSORFLOW:
        return TensorflowSpawner
    if framework == Frameworks.HOROVOD:
        return HorovodSpawner
    if framework == Frameworks.MXNET:
        return MXNetSpawner
    if framework == Frameworks.PYTORCH:
        return PytorchSpawner

    return ExperimentSpawner


def handle_tensorflow_experiment(experiment, spawner, response):
    # Get the number of jobs this experiment started
    master = response[TaskType.MASTER]
    job_uuid = master['pod']['metadata']['labels']['job_uuid']
    job_uuid = uuid.UUID(job_uuid)

    create_job(job_uuid=job_uuid,
               experiment=experiment,
               definition=get_job_definition(master),
               resources=spawner.spec.master_resources)

    cluster, is_distributed, = spawner.spec.cluster_def
    worker_resources = TensorflowSpecification.get_worker_resources(
        environment=spawner.spec.environment,
        cluster=cluster,
        is_distributed=is_distributed
    )

    ps_resources = TensorflowSpecification.get_ps_resources(
        environment=spawner.spec.environment,
        cluster=cluster,
        is_distributed=is_distributed
    )

    for i, worker in enumerate(response[TaskType.WORKER]):
        job_uuid = worker['pod']['metadata']['labels']['job_uuid']
        job_uuid = uuid.UUID(job_uuid)
        create_job(job_uuid=job_uuid,
                   experiment=experiment,
                   definition=get_job_definition(worker),
                   role=TaskType.WORKER,
                   resources=worker_resources.get(i))

    for i, ps in enumerate(response[TaskType.PS]):
        job_uuid = ps['pod']['metadata']['labels']['job_uuid']
        job_uuid = uuid.UUID(job_uuid)
        create_job(job_uuid=job_uuid,
                   experiment=experiment,
                   definition=get_job_definition(ps),
                   role=TaskType.PS,
                   resources=ps_resources.get(i))


def handle_horovod_experiment(experiment, spawner, response):
    # Get the number of jobs this experiment started
    master = response[TaskType.MASTER]
    job_uuid = master['pod']['metadata']['labels']['job_uuid']
    job_uuid = uuid.UUID(job_uuid)

    create_job(job_uuid=job_uuid,
               experiment=experiment,
               definition=get_job_definition(master),
               resources=spawner.spec.master_resources)

    cluster, is_distributed, = spawner.spec.cluster_def
    worker_resources = HorovodSpecification.get_worker_resources(
        environment=spawner.spec.environment,
        cluster=cluster,
        is_distributed=is_distributed
    )

    for i, worker in enumerate(response[TaskType.WORKER]):
        job_uuid = worker['pod']['metadata']['labels']['job_uuid']
        job_uuid = uuid.UUID(job_uuid)
        create_job(job_uuid=job_uuid,
                   experiment=experiment,
                   definition=get_job_definition(worker),
                   role=TaskType.WORKER,
                   resources=worker_resources.get(i))


def handle_pytorch_experiment(experiment, spawner, response):
    # Get the number of jobs this experiment started
    master = response[TaskType.MASTER]
    job_uuid = master['pod']['metadata']['labels']['job_uuid']
    job_uuid = uuid.UUID(job_uuid)

    create_job(job_uuid=job_uuid,
               experiment=experiment,
               definition=get_job_definition(master),
               resources=spawner.spec.master_resources)

    cluster, is_distributed, = spawner.spec.cluster_def
    worker_resources = PytorchSpecification.get_worker_resources(
        environment=spawner.spec.environment,
        cluster=cluster,
        is_distributed=is_distributed
    )

    for i, worker in enumerate(response[TaskType.WORKER]):
        job_uuid = worker['pod']['metadata']['labels']['job_uuid']
        job_uuid = uuid.UUID(job_uuid)
        create_job(job_uuid=job_uuid,
                   experiment=experiment,
                   definition=get_job_definition(worker),
                   role=TaskType.WORKER,
                   resources=worker_resources.get(i))


def handle_mxnet_experiment(experiment, spawner, response):
    # Get the number of jobs this experiment started
    master = response[TaskType.MASTER]
    job_uuid = master['pod']['metadata']['labels']['job_uuid']
    job_uuid = uuid.UUID(job_uuid)

    create_job(job_uuid=job_uuid,
               experiment=experiment,
               definition=get_job_definition(master),
               resources=spawner.spec.master_resources)

    cluster, is_distributed, = spawner.spec.cluster_def
    worker_resources = MXNetSpecification.get_worker_resources(
        environment=spawner.spec.environment,
        cluster=cluster,
        is_distributed=is_distributed
    )

    server_resources = MXNetSpecification.get_ps_resources(
        environment=spawner.spec.environment,
        cluster=cluster,
        is_distributed=is_distributed
    )

    for i, worker in enumerate(response[TaskType.WORKER]):
        job_uuid = worker['pod']['metadata']['labels']['job_uuid']
        job_uuid = uuid.UUID(job_uuid)
        create_job(job_uuid=job_uuid,
                   experiment=experiment,
                   definition=get_job_definition(worker),
                   role=TaskType.WORKER,
                   resources=worker_resources.get(i))

    for i, server in enumerate(response[TaskType.SERVER]):
        job_uuid = server['pod']['metadata']['labels']['job_uuid']
        job_uuid = uuid.UUID(job_uuid)
        create_job(job_uuid=job_uuid,
                   experiment=experiment,
                   definition=get_job_definition(server),
                   role=TaskType.SERVER,
                   resources=server_resources.get(i))


def handle_base_experiment(experiment, spawner, response):
    # Default case only master was created by the experiment spawner
    master = response[TaskType.MASTER]
    job_uuid = master['pod']['metadata']['labels']['job_uuid']
    job_uuid = uuid.UUID(job_uuid)

    create_job(job_uuid=job_uuid,
               experiment=experiment,
               definition=get_job_definition(master),
               resources=spawner.spec.master_resources)


def handle_experiment(experiment, spawner, response):
    framework = experiment.specification.framework
    if framework == Frameworks.TENSORFLOW:
        handle_tensorflow_experiment(experiment=experiment, spawner=spawner, response=response)
        return
    if framework == Frameworks.HOROVOD:
        handle_horovod_experiment(experiment=experiment, spawner=spawner, response=response)
        return
    if framework == Frameworks.MXNET:
        handle_mxnet_experiment(experiment=experiment, spawner=spawner, response=response)
        return
    if framework == Frameworks.PYTORCH:
        handle_pytorch_experiment(experiment=experiment, spawner=spawner, response=response)
        return

    handle_base_experiment(experiment=experiment, spawner=spawner, response=response)


def start_experiment(experiment):
    # Update experiment status to show that its started
    experiment.set_status(ExperimentLifeCycle.SCHEDULED)

    project = experiment.project
    group = experiment.experiment_group

    job_docker_image = None  # This will force the spawners to use the default docker image
    if experiment.specification.run_exec:
        try:
            image_name, image_tag = get_experiment_image_info(experiment=experiment)
        except ValueError as e:
            logger.warning('Could not start the experiment, %s', e)
            experiment.set_status(ExperimentLifeCycle.FAILED,
                                  message='External git repo was note found.')
            return
        job_docker_image = '{}:{}'.format(image_name, image_tag)
        logger.info('Start experiment with built image `%s`', job_docker_image)
    else:
        logger.info('Start experiment with default image.')

    spawner_class = get_spawner_class(experiment.specification.framework)

    # Use spawners to start the experiment
    spawner = spawner_class(project_name=project.unique_name,
                            experiment_name=experiment.unique_name,
                            experiment_group_name=group.unique_name if group else None,
                            project_uuid=project.uuid.hex,
                            experiment_group_uuid=group.uuid.hex if group else None,
                            experiment_uuid=experiment.uuid.hex,
                            original_name=experiment.original_unique_name,
                            cloning_strategy=experiment.cloning_strategy,
                            spec=experiment.specification,
                            k8s_config=settings.K8S_CONFIG,
                            namespace=settings.K8S_NAMESPACE,
                            in_cluster=True,
                            job_docker_image=job_docker_image,
                            use_sidecar=True,
                            sidecar_config=config.get_requested_params(to_str=True))
    try:
        response = spawner.start_experiment(user_token=experiment.user.auth_token.key)
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

    handle_experiment(experiment=experiment, spawner=spawner, response=response)


def stop_experiment(experiment, update_status=False):
    project = experiment.project
    group = experiment.experiment_group

    spawner_class = get_spawner_class(experiment.specification.framework)

    spawner = spawner_class(project_name=project.unique_name,
                            experiment_name=experiment.unique_name,
                            experiment_group_name=group.unique_name if group else None,
                            project_uuid=project.uuid.hex,
                            experiment_group_uuid=group.uuid.hex if group else None,
                            experiment_uuid=experiment.uuid.hex,
                            spec=experiment.specification,
                            k8s_config=settings.K8S_CONFIG,
                            namespace=settings.K8S_NAMESPACE,
                            in_cluster=True,
                            use_sidecar=True,
                            sidecar_config=config.get_requested_params(to_str=True))
    spawner.stop_experiment()
    if update_status:
        # Update experiment status to show that its stopped
        experiment.set_status(ExperimentLifeCycle.STOPPED)
