import logging
import traceback
import uuid

from kubernetes.client.rest import ApiException

import conf

from constants.experiments import ExperimentLifeCycle
from db.models.experiment_jobs import ExperimentJob
from db.models.job_resources import JobResources
from docker_images.image_info import get_image_info
from scheduler.spawners.experiment_spawner import ExperimentSpawner
from scheduler.spawners.horovod_spawner import HorovodSpawner
from scheduler.spawners.mpi_job_spawner import MPIJobSpawner
from scheduler.spawners.mxnet_spawner import MXNetSpawner
from scheduler.spawners.pytorch_job_spawner import PytorchJobSpawner
from scheduler.spawners.pytorch_spawner import PytorchSpawner
from scheduler.spawners.tensorflow_spawner import TensorflowSpawner
from scheduler.spawners.tf_job_spawner import TFJobSpawner
from scheduler.spawners.utils import get_job_definition
from schemas.experiments import ExperimentBackend, ExperimentFramework
from schemas.specifications import (
    HorovodSpecification,
    MXNetSpecification,
    PytorchSpecification,
    TensorflowSpecification
)
from schemas.tasks import TaskType
from stores.exceptions import VolumeNotFoundError

_logger = logging.getLogger('polyaxon.scheduler.experiment')


def create_job(job_uuid,
               experiment,
               role=None,
               k8s_replica=None,
               sequence=None,
               resources=None,
               node_selector=None,
               affinity=None,
               tolerations=None):
    job = ExperimentJob(uuid=uuid.UUID(job_uuid), experiment=experiment, definition={})

    k8s_replica = k8s_replica or role
    if role:
        job.role = role
    if k8s_replica:
        job.k8s_replica = k8s_replica

    if sequence:
        job.sequence = sequence

    if node_selector:
        job.node_selector = node_selector

    if affinity:
        job.affinity = affinity

    if tolerations:
        job.tolerations = tolerations

    def set_resources():
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
        if resources.tpu:
            _resources = resources.tpu.to_dict()
            if any(_resources.values()):
                job_resources['tpu'] = _resources
        if job_resources:
            job.resources = JobResources.objects.create(**job_resources)

    if resources:
        set_resources()

    job.save()


def set_job_definition(job_uuid, definition):
    job = ExperimentJob.objects.get(uuid=job_uuid)
    job.definition = definition
    job.save(update_fields=['definition'])


def get_native_spawner_backend(framework):
    if framework == ExperimentFramework.TENSORFLOW:
        return TensorflowSpawner
    if framework == ExperimentFramework.HOROVOD:
        return HorovodSpawner
    if framework == ExperimentFramework.MXNET:
        return MXNetSpawner
    if framework == ExperimentFramework.PYTORCH:
        return PytorchSpawner

    return ExperimentSpawner


def get_kf_spawner_backend(framework):
    if framework == ExperimentFramework.TENSORFLOW:
        return TFJobSpawner
    if framework == ExperimentFramework.HOROVOD:
        return HorovodSpawner
    if framework == ExperimentFramework.MXNET:
        return MXNetSpawner
    if framework == ExperimentFramework.PYTORCH:
        return PytorchJobSpawner

    return ExperimentSpawner


def get_spawner_class(backend, framework):
    if backend == ExperimentBackend.KUBEFLOW:
        return get_kf_spawner_backend(framework=framework)
    if backend == ExperimentBackend.MPI:
        return MPIJobSpawner

    return get_native_spawner_backend(framework=framework)


def create_tensorflow_experiment_jobs(experiment, spawner):
    master_job_uuid = spawner.job_uuids[TaskType.MASTER][0]
    k8s_replica = None
    if experiment.backend == ExperimentBackend.KUBEFLOW:
        k8s_replica = TaskType.CHIEF
    create_job(job_uuid=master_job_uuid,
               experiment=experiment,
               k8s_replica=k8s_replica,
               resources=spawner.spec.master_resources,
               node_selector=spawner.spec.master_node_selector,
               affinity=spawner.spec.master_affinity,
               tolerations=spawner.spec.master_tolerations)

    cluster, is_distributed = spawner.spec.cluster_def
    environment = spawner.spec.config.tensorflow

    worker_resources = TensorflowSpecification.get_worker_resources(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    worker_node_selectors = TensorflowSpecification.get_worker_node_selectors(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    worker_affinities = TensorflowSpecification.get_worker_affinities(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    worker_tolerations = TensorflowSpecification.get_worker_tolerations(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )

    for i, worker_job_uuid in enumerate(spawner.job_uuids[TaskType.WORKER]):
        create_job(job_uuid=worker_job_uuid,
                   experiment=experiment,
                   role=TaskType.WORKER,
                   sequence=i,
                   resources=worker_resources.get(i),
                   node_selector=worker_node_selectors.get(i),
                   affinity=worker_affinities.get(i),
                   tolerations=worker_tolerations.get(i))

    ps_resources = TensorflowSpecification.get_ps_resources(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    ps_node_selectors = TensorflowSpecification.get_ps_node_selectors(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    ps_affinities = TensorflowSpecification.get_ps_affinities(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    ps_tolerations = TensorflowSpecification.get_ps_tolerations(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )

    for i, ps_job_uuid in enumerate(spawner.job_uuids[TaskType.PS]):
        create_job(job_uuid=ps_job_uuid,
                   experiment=experiment,
                   role=TaskType.PS,
                   sequence=i,
                   resources=ps_resources.get(i),
                   node_selector=ps_node_selectors.get(i),
                   affinity=ps_affinities.get(i),
                   tolerations=ps_tolerations.get(i))


def handle_tensorflow_experiment(response):
    master = response[TaskType.MASTER]
    job_uuid = master['pod']['metadata']['labels']['job_uuid']
    job_uuid = uuid.UUID(job_uuid)

    set_job_definition(job_uuid=job_uuid, definition=get_job_definition(master))

    for worker in response[TaskType.WORKER]:
        job_uuid = worker['pod']['metadata']['labels']['job_uuid']
        job_uuid = uuid.UUID(job_uuid)
        set_job_definition(job_uuid=job_uuid, definition=get_job_definition(worker))

    for ps in response[TaskType.PS]:
        job_uuid = ps['pod']['metadata']['labels']['job_uuid']
        job_uuid = uuid.UUID(job_uuid)
        set_job_definition(job_uuid=job_uuid, definition=get_job_definition(ps))


def create_horovod_experiment_jobs(experiment, spawner):
    master_job_uuid = spawner.job_uuids[TaskType.MASTER][0]
    k8s_replica = None
    create_job(job_uuid=master_job_uuid,
               experiment=experiment,
               k8s_replica=k8s_replica,
               resources=spawner.spec.master_resources,
               node_selector=spawner.spec.master_node_selector,
               affinity=spawner.spec.master_affinity,
               tolerations=spawner.spec.master_tolerations)

    cluster, is_distributed = spawner.spec.cluster_def
    environment = spawner.spec.config.horovod
    worker_resources = HorovodSpecification.get_worker_resources(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    worker_node_selectors = HorovodSpecification.get_worker_node_selectors(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    worker_affinities = HorovodSpecification.get_worker_affinities(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    worker_tolerations = HorovodSpecification.get_worker_tolerations(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )

    for i, worker_job_uuid in enumerate(spawner.job_uuids[TaskType.WORKER]):
        create_job(job_uuid=worker_job_uuid,
                   experiment=experiment,
                   role=TaskType.WORKER,
                   sequence=i,
                   resources=worker_resources.get(i),
                   node_selector=worker_node_selectors.get(i),
                   affinity=worker_affinities.get(i),
                   tolerations=worker_tolerations.get(i))


def handle_horovod_experiment(response):
    master = response[TaskType.MASTER]
    job_uuid = master['pod']['metadata']['labels']['job_uuid']
    job_uuid = uuid.UUID(job_uuid)

    set_job_definition(job_uuid=job_uuid, definition=get_job_definition(master))

    for worker in response[TaskType.WORKER]:
        job_uuid = worker['pod']['metadata']['labels']['job_uuid']
        job_uuid = uuid.UUID(job_uuid)
        set_job_definition(job_uuid=job_uuid, definition=get_job_definition(worker))


def create_mpi_experiment_jobs(experiment, spawner):
    cluster, is_distributed = spawner.spec.cluster_def
    environment = spawner.spec.config.horovod
    worker_resources = HorovodSpecification.get_worker_resources(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    worker_node_selectors = HorovodSpecification.get_worker_node_selectors(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    worker_affinities = HorovodSpecification.get_worker_affinities(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    worker_tolerations = HorovodSpecification.get_worker_tolerations(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )

    for i, worker_job_uuid in enumerate(spawner.job_uuids[TaskType.WORKER]):
        if i == 0:
            create_job(job_uuid=worker_job_uuid,
                       experiment=experiment,
                       role=TaskType.MASTER,
                       k8s_replica=TaskType.WORKER,
                       resources=spawner.spec.master_resources,
                       node_selector=spawner.spec.master_node_selector,
                       affinity=spawner.spec.master_affinity,
                       tolerations=spawner.spec.master_tolerations)
        create_job(job_uuid=worker_job_uuid,
                   experiment=experiment,
                   role=TaskType.WORKER,
                   sequence=i,
                   resources=worker_resources.get(i),
                   node_selector=worker_node_selectors.get(i),
                   affinity=worker_affinities.get(i),
                   tolerations=worker_tolerations.get(i))


def create_pytorch_experiment_jobs(experiment, spawner):
    master_job_uuid = spawner.job_uuids[TaskType.MASTER][0]
    k8s_replica = None
    create_job(job_uuid=master_job_uuid,
               experiment=experiment,
               k8s_replica=k8s_replica,
               resources=spawner.spec.master_resources,
               node_selector=spawner.spec.master_node_selector,
               affinity=spawner.spec.master_affinity,
               tolerations=spawner.spec.master_tolerations)

    cluster, is_distributed = spawner.spec.cluster_def
    environment = spawner.spec.config.pytorch

    worker_resources = PytorchSpecification.get_worker_resources(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    worker_node_selectors = PytorchSpecification.get_worker_node_selectors(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    worker_affinities = PytorchSpecification.get_worker_affinities(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    worker_tolerations = PytorchSpecification.get_worker_tolerations(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )

    for i, worker_job_uuid in enumerate(spawner.job_uuids[TaskType.WORKER]):
        create_job(job_uuid=worker_job_uuid,
                   experiment=experiment,
                   role=TaskType.WORKER,
                   sequence=i,
                   resources=worker_resources.get(i),
                   node_selector=worker_node_selectors.get(i),
                   affinity=worker_affinities.get(i),
                   tolerations=worker_tolerations.get(i))


def handle_pytorch_experiment(response):
    master = response[TaskType.MASTER]
    job_uuid = master['pod']['metadata']['labels']['job_uuid']
    job_uuid = uuid.UUID(job_uuid)

    set_job_definition(job_uuid=job_uuid, definition=get_job_definition(master))

    for worker in response[TaskType.WORKER]:
        job_uuid = worker['pod']['metadata']['labels']['job_uuid']
        job_uuid = uuid.UUID(job_uuid)
        set_job_definition(job_uuid=job_uuid, definition=get_job_definition(worker))


def create_mxnet_experiment_jobs(experiment, spawner):
    master_job_uuid = spawner.job_uuids[TaskType.MASTER][0]
    k8s_replica = None
    create_job(job_uuid=master_job_uuid,
               experiment=experiment,
               k8s_replica=k8s_replica,
               resources=spawner.spec.master_resources,
               node_selector=spawner.spec.master_node_selector,
               affinity=spawner.spec.master_affinity,
               tolerations=spawner.spec.master_tolerations)

    cluster, is_distributed = spawner.spec.cluster_def
    environment = spawner.spec.config.mxnet

    worker_resources = MXNetSpecification.get_worker_resources(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    worker_node_selectors = MXNetSpecification.get_worker_node_selectors(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    worker_affinities = MXNetSpecification.get_worker_affinities(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    worker_tolerations = MXNetSpecification.get_worker_tolerations(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )

    for i, worker_job_uuid in enumerate(spawner.job_uuids[TaskType.WORKER]):
        create_job(job_uuid=worker_job_uuid,
                   experiment=experiment,
                   role=TaskType.WORKER,
                   sequence=i,
                   resources=worker_resources.get(i),
                   node_selector=worker_node_selectors.get(i),
                   affinity=worker_affinities.get(i),
                   tolerations=worker_tolerations.get(i))

    server_resources = MXNetSpecification.get_ps_resources(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    server_node_selectors = MXNetSpecification.get_ps_node_selectors(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    server_affinities = MXNetSpecification.get_ps_affinities(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    server_tolerations = MXNetSpecification.get_ps_tolerations(
        environment=environment,
        cluster=cluster,
        is_distributed=is_distributed
    )
    for i, server_job_uuid in enumerate(spawner.job_uuids[TaskType.SERVER]):
        create_job(job_uuid=server_job_uuid,
                   experiment=experiment,
                   role=TaskType.SERVER,
                   sequence=i,
                   resources=server_resources.get(i),
                   node_selector=server_node_selectors,
                   affinity=server_affinities,
                   tolerations=server_tolerations)


def handle_mxnet_experiment(response):
    master = response[TaskType.MASTER]
    job_uuid = master['pod']['metadata']['labels']['job_uuid']
    job_uuid = uuid.UUID(job_uuid)

    set_job_definition(job_uuid=job_uuid, definition=get_job_definition(master))

    for worker in response[TaskType.WORKER]:
        job_uuid = worker['pod']['metadata']['labels']['job_uuid']
        job_uuid = uuid.UUID(job_uuid)
        set_job_definition(job_uuid=job_uuid, definition=get_job_definition(worker))

    for server in response[TaskType.SERVER]:
        job_uuid = server['pod']['metadata']['labels']['job_uuid']
        job_uuid = uuid.UUID(job_uuid)
        set_job_definition(job_uuid=job_uuid, definition=get_job_definition(server))


def create_base_experiment_job(experiment, spawner):
    master_job_uuid = spawner.job_uuids[TaskType.MASTER][0]
    create_job(job_uuid=master_job_uuid,
               experiment=experiment,
               resources=spawner.spec.master_resources,
               node_selector=spawner.spec.master_node_selector,
               affinity=spawner.spec.master_affinity,
               tolerations=spawner.spec.master_tolerations)


def handle_base_experiment(response):
    master = response[TaskType.MASTER]
    job_uuid = master['pod']['metadata']['labels']['job_uuid']
    job_uuid = uuid.UUID(job_uuid)

    set_job_definition(job_uuid=job_uuid, definition=get_job_definition(master))


def handle_experiment(experiment, response):
    # TODO: May be save the template generate to create each one of the replicas?
    if experiment.backend in {ExperimentBackend.KUBEFLOW, ExperimentBackend.MPI}:
        return

    framework = experiment.framework
    if framework == ExperimentFramework.TENSORFLOW:
        handle_tensorflow_experiment(response=response)
        return
    if framework == ExperimentFramework.HOROVOD:
        handle_horovod_experiment(response=response)
        return
    if framework == ExperimentFramework.MXNET:
        handle_mxnet_experiment(response=response)
        return
    if framework == ExperimentFramework.PYTORCH:
        handle_pytorch_experiment(response=response)
        return

    handle_base_experiment(response=response)


def create_experiment_jobs(experiment, spawner):
    cluster, is_distributed = spawner.spec.cluster_def
    framework = experiment.specification.framework
    backend = experiment.specification.backend

    if not is_distributed:
        create_base_experiment_job(experiment=experiment, spawner=spawner)
        return

    if backend == ExperimentBackend.MPI:
        create_mpi_experiment_jobs(experiment=experiment, spawner=spawner)
        return
    if framework == ExperimentFramework.TENSORFLOW:
        create_tensorflow_experiment_jobs(experiment=experiment, spawner=spawner)
        return
    if framework == ExperimentFramework.HOROVOD:
        create_horovod_experiment_jobs(experiment=experiment, spawner=spawner)
        return
    if framework == ExperimentFramework.MXNET:
        create_mxnet_experiment_jobs(experiment=experiment, spawner=spawner)
        return
    if framework == ExperimentFramework.PYTORCH:
        create_pytorch_experiment_jobs(experiment=experiment, spawner=spawner)
        return

    create_base_experiment_job(experiment=experiment, spawner=spawner)


def start_experiment(experiment):
    # Update experiment status to show that its started
    experiment.set_status(ExperimentLifeCycle.SCHEDULED)

    project = experiment.project
    group = experiment.experiment_group

    job_docker_image = None  # This will force the spawners to use the default docker image
    if experiment.specification.build:
        try:
            image_name, image_tag = get_image_info(build_job=experiment.build_job)
        except (ValueError, AttributeError):
            _logger.error('Could not start the experiment.', exc_info=True)
            experiment.set_status(ExperimentLifeCycle.FAILED,
                                  message='Image info was not found.')
            return
        job_docker_image = '{}:{}'.format(image_name, image_tag)
        _logger.info('Start experiment with built image `%s`', job_docker_image)
    else:
        _logger.info('Start experiment with default image.')

    spawner_class = get_spawner_class(backend=experiment.backend,
                                      framework=experiment.specification.framework)
    # token_scope = RedisEphemeralTokens.get_scope(experiment.user.id,
    #                                              'experiment',
    #                                              experiment.id)

    error = {}
    try:
        # Use spawners to start the experiment
        spawner = spawner_class(project_name=project.unique_name,
                                experiment_name=experiment.unique_name,
                                experiment_group_name=group.unique_name if group else None,
                                project_uuid=project.uuid.hex,
                                experiment_group_uuid=group.uuid.hex if group else None,
                                experiment_uuid=experiment.uuid.hex,
                                persistence_config=experiment.persistence_config,
                                outputs_refs_experiments=experiment.outputs_refs_experiments,
                                outputs_refs_jobs=experiment.outputs_refs_jobs,
                                original_name=experiment.original_unique_name,
                                cloning_strategy=experiment.cloning_strategy,
                                spec=experiment.specification,
                                k8s_config=conf.get('K8S_CONFIG'),
                                namespace=conf.get('K8S_NAMESPACE'),
                                in_cluster=True,
                                job_docker_image=job_docker_image,
                                use_sidecar=True)
        # Create db jobs
        create_experiment_jobs(experiment=experiment, spawner=spawner)
        # Create k8s jobs
        response = spawner.start_experiment()
        # handle response
        handle_experiment(experiment=experiment, response=response)
        experiment.set_status(ExperimentLifeCycle.STARTING)
    except ApiException as e:
        _logger.error('Could not start the experiment, please check your polyaxon spec.',
                      exc_info=True)
        error = {
            'raised': True,
            'traceback': traceback.format_exc(),
            'message': 'Could not start the experiment, encountered a Kubernetes ApiException.'
        }
    except VolumeNotFoundError as e:
        _logger.error('Could not start the experiment, please check your volume definitions.',
                      exc_info=True)
        error = {
            'raised': True,
            'traceback': traceback.format_exc(),
            'message': 'Could not start the experiment, '
                       'encountered a volume definition problem, %s.' % e
        }
    except Exception as e:
        _logger.error('Could not start the experiment, please check your polyaxon spec',
                      exc_info=True)
        error = {
            'raised': True,
            'traceback': traceback.format_exc(),
            'message': 'Could not start the experiment encountered an {} exception.'.format(
                e.__class__.__name__)
        }
    finally:
        if error.get('raised'):
            experiment.set_status(
                ExperimentLifeCycle.FAILED,
                message=error.get('message'),
                traceback=error.get('traceback'))


def stop_experiment(project_name,
                    project_uuid,
                    experiment_name,
                    experiment_uuid,
                    specification,
                    experiment_group_name=None,
                    experiment_group_uuid=None):
    spawner_class = get_spawner_class(backend=specification.backend,
                                      framework=specification.framework)

    spawner = spawner_class(project_name=project_name,
                            project_uuid=project_uuid,
                            experiment_name=experiment_name,
                            experiment_group_name=experiment_group_name,
                            experiment_group_uuid=experiment_group_uuid,
                            experiment_uuid=experiment_uuid,
                            spec=specification,
                            k8s_config=conf.get('K8S_CONFIG'),
                            namespace=conf.get('K8S_NAMESPACE'),
                            in_cluster=True)
    return spawner.stop_experiment()
