import json
import random

import conf

from constants.k8s_jobs import JOB_NAME_FORMAT, TENSORBOARD_JOB_NAME
from constants.stores import GCS, S3
from libs.unique_urls import get_tensorboard_health_url
from polyaxon_k8s.exceptions import PolyaxonK8SError
from scheduler.spawners.project_job_spawner import ProjectJobSpawner
from scheduler.spawners.templates import ingresses, services
from scheduler.spawners.templates.stores import get_stores_secrets
from scheduler.spawners.templates.tensorboards import manager
from scheduler.spawners.templates.volumes import (
    get_pod_outputs_volume,
    get_pod_refs_outputs_volumes,
    get_volume_from_secret
)


class TensorboardValidation(Exception):
    pass


class TensorboardSpawner(ProjectJobSpawner):
    PORT = 6006
    STORE_SECRET_VOLUME_NAME = 'plx-{}-secret'  # noqa
    STORE_SECRET_MOUNT_PATH = '/tmp'  # noqa
    STORE_SECRET_KEY_MOUNT_PATH = STORE_SECRET_MOUNT_PATH + '/.' + STORE_SECRET_VOLUME_NAME

    def __init__(self,
                 project_name,
                 project_uuid,
                 job_name,
                 job_uuid,
                 spec=None,
                 k8s_config=None,
                 namespace='default',
                 in_cluster=False,
                 job_container_name=None,
                 job_docker_image=None,
                 sidecar_container_name=None,
                 sidecar_docker_image=None,
                 role_label=None,
                 type_label=None,
                 use_sidecar=False,
                 sidecar_config=None):
        self.spec = spec
        self.resource_manager = manager.ResourceManager(
            namespace=namespace,
            name=TENSORBOARD_JOB_NAME,
            project_name=project_name,
            project_uuid=project_uuid,
            job_name=job_name,
            job_uuid=job_uuid,
            job_docker_image=job_docker_image,
            job_container_name=job_container_name,
            sidecar_container_name=sidecar_container_name,
            sidecar_docker_image=sidecar_docker_image,
            role_label=role_label,
            type_label=type_label,
            use_sidecar=use_sidecar,
            sidecar_config=sidecar_config,
            health_check_url=get_tensorboard_health_url(job_name),
            log_level=self.spec.log_level if self.spec else None)
        super().__init__(project_name=project_name,
                         project_uuid=project_uuid,
                         job_name=job_name,
                         job_uuid=job_uuid,
                         k8s_config=k8s_config,
                         namespace=namespace,
                         in_cluster=in_cluster)

    def get_tensorboard_url(self):
        return self._get_service_url(TENSORBOARD_JOB_NAME)

    def request_tensorboard_port(self):
        if not self._use_ingress():
            return self.PORT

        labels = 'app={},role={}'.format(conf.get('APP_LABELS_TENSORBOARD'),
                                         conf.get('ROLE_LABELS_DASHBOARD'))
        ports = [service.spec.ports[0].port for service in self.list_services(labels)]
        port = random.randint(*conf.get('TENSORBOARD_PORT_RANGE'))
        while port in ports:
            port = random.randint(*conf.get('TENSORBOARD_PORT_RANGE'))
        return port

    @staticmethod
    def validate_stores_secrets_keys(stores_secrets):
        """Validates that we can only authenticate to one S3 and one GCS."""
        stores = set([])
        for store_secret in stores_secrets:
            if store_secret['store'] in stores:
                raise TensorboardValidation('Received an invalid store configuration.')
            elif store_secret['store'] not in {GCS, S3}:
                raise TensorboardValidation('Received an unsupported store configuration.')
            stores.add(store_secret['store'])

    @classmethod
    def get_stores_secrets_volumes(cls, stores_secrets):
        """Handles the case of GCS and S3 and create a volume with secret file."""
        volumes = []
        volume_mounts = []
        for store_secret in stores_secrets:
            store = store_secret['store']
            if store in {GCS, S3}:
                secrets_volumes, secrets_volume_mounts = get_volume_from_secret(
                    volume_name=cls.STORE_SECRET_VOLUME_NAME.format(store),
                    mount_path=cls.STORE_SECRET_KEY_MOUNT_PATH.format(store),
                    secret_name=store_secret['persistence_secret'],
                )
                volumes += secrets_volumes
                volume_mounts += secrets_volume_mounts

        return volumes, volume_mounts

    @classmethod
    def get_stores_secrets_command_args(cls, stores_secrets):
        """Create an auth command for S3 and GCS."""
        commands = []
        for store_secret in stores_secrets:
            store = store_secret['store']
            if store == GCS:
                commands.append('export GOOGLE_APPLICATION_CREDENTIALS={}'.format(
                    cls.STORE_SECRET_KEY_MOUNT_PATH.format(store) + '/' +
                    store_secret['persistence_secret_key']
                ))
            elif store == S3:
                commands.append(
                    "import json; data = json.loads(open('{}').read()); content = []; [content.append('export {}={}'.format(k, data[k])) for k in data]; output = open('{}', 'w'); output.write('\n'.join(content)); output.close()".format(  # noqa
                        cls.STORE_SECRET_KEY_MOUNT_PATH.format(store) + '/' +
                        store_secret['persistence_secret_key'],
                        cls.STORE_SECRET_KEY_MOUNT_PATH.format('envs3'),
                    ))
                commands.append("source {}".format(
                    cls.STORE_SECRET_KEY_MOUNT_PATH.format('envs3')))

        return commands

    def start_tensorboard(self,
                          outputs_path,
                          persistence_outputs,
                          outputs_specs=None,
                          outputs_refs_jobs=None,
                          outputs_refs_experiments=None,
                          resources=None,
                          node_selector=None,
                          affinity=None,
                          tolerations=None):
        ports = [self.request_tensorboard_port()]
        target_ports = [self.PORT]
        volumes, volume_mounts = get_pod_outputs_volume(persistence_outputs)
        refs_volumes, refs_volume_mounts = get_pod_refs_outputs_volumes(
            outputs_refs=outputs_refs_jobs,
            persistence_outputs=persistence_outputs)
        volumes += refs_volumes
        volume_mounts += refs_volume_mounts
        refs_volumes, refs_volume_mounts = get_pod_refs_outputs_volumes(
            outputs_refs=outputs_specs,
            persistence_outputs=persistence_outputs)
        volumes += refs_volumes
        volume_mounts += refs_volume_mounts
        refs_volumes, refs_volume_mounts = get_pod_refs_outputs_volumes(
            outputs_refs=outputs_refs_experiments,
            persistence_outputs=persistence_outputs)
        volumes += refs_volumes
        volume_mounts += refs_volume_mounts

        # Add volumes for persistence outputs secrets
        stores_secrets = get_stores_secrets(specs=outputs_specs)
        self.validate_stores_secrets_keys(stores_secrets=stores_secrets)
        secrets_volumes, secrets_volume_mounts = self.get_stores_secrets_volumes(
            stores_secrets=stores_secrets)
        volumes += secrets_volumes
        volume_mounts += secrets_volume_mounts

        resource_name = self.resource_manager.get_resource_name()
        # Get persistence outputs secrets auth commands
        command_args = self.get_stores_secrets_command_args(stores_secrets=stores_secrets)
        command_args.append("tensorboard --logdir={} --port={}".format(outputs_path, self.PORT))
        args = [' && '.join(command_args)]
        command = ["/bin/sh", "-c"]

        deployment = self.resource_manager.get_deployment(
            resource_name=resource_name,
            volume_mounts=volume_mounts,
            volumes=volumes,
            labels=self.resource_manager.labels,
            env_vars=None,
            command=command,
            args=args,
            persistence_outputs=persistence_outputs,
            outputs_refs_jobs=outputs_refs_jobs,
            outputs_refs_experiments=outputs_refs_experiments,
            resources=resources,
            ephemeral_token=None,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
            ports=target_ports,
            restart_policy=None)

        dep_resp, _ = self.create_or_update_deployment(name=resource_name, data=deployment)
        service = services.get_service(
            namespace=self.namespace,
            name=resource_name,
            labels=self.resource_manager.get_labels(),
            ports=ports,
            target_ports=target_ports,
            service_type=self._get_service_type())
        service_resp, _ = self.create_or_update_service(name=resource_name, data=service)
        results = {'deployment': dep_resp.to_dict(), 'service': service_resp.to_dict()}

        if self._use_ingress():
            annotations = json.loads(conf.get('K8S_INGRESS_ANNOTATIONS'))
            paths = [{
                'path': '/tensorboards/{}'.format(self.project_name.replace('.', '/')),
                'backend': {
                    'serviceName': resource_name,
                    'servicePort': ports[0]
                }
            }]
            ingress = ingresses.get_ingress(namespace=self.namespace,
                                            name=resource_name,
                                            labels=self.resource_manager.get_labels(),
                                            annotations=annotations,
                                            paths=paths)
            self.create_or_update_ingress(name=resource_name, data=ingress)

        return results

    def stop_tensorboard(self):
        deployment_name = JOB_NAME_FORMAT.format(name=TENSORBOARD_JOB_NAME, job_uuid=self.job_uuid)
        try:
            self.delete_deployment(name=deployment_name)
            self.delete_service(name=deployment_name)
            if self._use_ingress():
                self.delete_ingress(name=deployment_name)
            return True
        except PolyaxonK8SError:
            return False
