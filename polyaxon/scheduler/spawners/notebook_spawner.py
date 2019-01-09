import json
import random

from hestia.crypto import get_hmac

from django.conf import settings

import conf
import stores

from constants.k8s_jobs import JOB_NAME_FORMAT, NOTEBOOK_JOB_NAME
from libs.paths.projects import get_project_repos_path
from polyaxon_k8s.exceptions import PolyaxonK8SError
from scheduler.spawners.project_job_spawner import ProjectJobSpawner
from scheduler.spawners.templates import constants, ingresses, services
from scheduler.spawners.templates.env_vars import (
    get_job_env_vars,
    get_pod_env_from,
    validate_configmap_refs,
    validate_secret_refs
)
from scheduler.spawners.templates.pod_environment import (
    get_affinity,
    get_node_selector,
    get_tolerations
)
from scheduler.spawners.templates.project_jobs import deployments
from scheduler.spawners.templates.volumes import (
    get_pod_refs_outputs_volumes,
    get_pod_volumes,
    get_shm_volumes,
    get_volume,
    get_volume_mount
)


class NotebookSpawner(ProjectJobSpawner):
    PORT = 8888

    def get_notebook_url(self):
        return self._get_service_url(NOTEBOOK_JOB_NAME)

    def get_notebook_token(self):
        return get_hmac(conf.get('APP_LABELS_NOTEBOOK'), self.project_uuid)

    @staticmethod
    def get_notebook_code_volume():
        volume = get_volume(volume=conf.get('REPOS_VOLUME'),
                            claim_name=conf.get('REPOS_CLAIM_NAME'),
                            host_path=conf.get('REPOS_HOST_PATH'))

        volume_mount = get_volume_mount(volume=conf.get('REPOS_VOLUME'),
                                        volume_mount=conf.get('REPOS_MOUNT_PATH'))
        return volume, volume_mount

    def request_notebook_port(self):
        if not self._use_ingress():
            return self.PORT

        labels = 'app={},role={}'.format(conf.get('APP_LABELS_NOTEBOOK'),
                                         conf.get('ROLE_LABELS_DASHBOARD'))
        ports = [service.spec.ports[0].port for service in self.list_services(labels)]
        port = random.randint(*settings.NOTEBOOK_PORT_RANGE)
        while port in ports:
            port = random.randint(*settings.NOTEBOOK_PORT_RANGE)
        return port

    def get_notebook_args(self, deployment_name, ports, allow_commits=False):
        notebook_token = self.get_notebook_token()
        notebook_url = self._get_proxy_url(
            namespace=self.namespace,
            job_name=NOTEBOOK_JOB_NAME,
            deployment_name=deployment_name,
            port=ports[0])

        if allow_commits:
            notebook_dir = get_project_repos_path(self.project_name)
            notebook_dir = '{}/{}'.format(notebook_dir, notebook_dir.split('/')[-1])
        else:
            notebook_dir = '.'

        return [
            "jupyter notebook "
            "--no-browser "
            "--port={port} "
            "--ip=0.0.0.0 "
            "--allow-root "
            "--NotebookApp.token={token} "
            "--NotebookApp.trust_xheaders=True "
            "--NotebookApp.base_url={base_url} "
            "--NotebookApp.notebook_dir={notebook_dir} ".format(
                port=self.PORT,
                token=notebook_token,
                base_url=notebook_url,
                notebook_dir=notebook_dir)]

    def start_notebook(self,
                       image,
                       persistence_outputs=None,
                       persistence_data=None,
                       outputs_refs_jobs=None,
                       outputs_refs_experiments=None,
                       resources=None,
                       secret_refs=None,
                       configmap_refs=None,
                       node_selector=None,
                       affinity=None,
                       tolerations=None,
                       allow_commits=False):
        ports = [self.request_notebook_port()]
        target_ports = [self.PORT]
        volumes, volume_mounts = get_pod_volumes(persistence_outputs=persistence_outputs,
                                                 persistence_data=persistence_data)
        refs_volumes, refs_volume_mounts = get_pod_refs_outputs_volumes(
            outputs_refs=outputs_refs_jobs,
            persistence_outputs=persistence_outputs)
        volumes += refs_volumes
        volume_mounts += refs_volume_mounts
        refs_volumes, refs_volume_mounts = get_pod_refs_outputs_volumes(
            outputs_refs=outputs_refs_experiments,
            persistence_outputs=persistence_outputs)
        volumes += refs_volumes
        volume_mounts += refs_volume_mounts
        shm_volumes, shm_volume_mounts = get_shm_volumes()
        volumes += shm_volumes
        volume_mounts += shm_volume_mounts
        env_vars = get_job_env_vars(
            persistence_outputs=persistence_outputs,
            outputs_path=stores.get_notebook_job_outputs_path(
                persistence=persistence_outputs,
                notebook_job=self.job_name),
            persistence_data=persistence_data,
            outputs_refs_jobs=outputs_refs_jobs,
            outputs_refs_experiments=outputs_refs_experiments
        )
        secret_refs = validate_secret_refs(secret_refs)
        configmap_refs = validate_configmap_refs(configmap_refs)
        env_from = get_pod_env_from(secret_refs=secret_refs, configmap_refs=configmap_refs)
        code_volume, code_volume_mount = self.get_notebook_code_volume()
        volumes.append(code_volume)
        volume_mounts.append(code_volume_mount)
        deployment_name = JOB_NAME_FORMAT.format(name=NOTEBOOK_JOB_NAME, job_uuid=self.job_uuid)

        node_selector = get_node_selector(
            node_selector=node_selector,
            default_node_selector=settings.NODE_SELECTOR_EXPERIMENTS)
        affinity = get_affinity(
            affinity=affinity,
            default_affinity=settings.AFFINITY_EXPERIMENTS)
        tolerations = get_tolerations(
            tolerations=tolerations,
            default_tolerations=settings.TOLERATIONS_EXPERIMENTS)
        deployment = deployments.get_deployment(
            namespace=self.namespace,
            app=conf.get('APP_LABELS_NOTEBOOK'),
            name=NOTEBOOK_JOB_NAME,
            project_name=self.project_name,
            project_uuid=self.project_uuid,
            job_name=self.job_name,
            job_uuid=self.job_uuid,
            volume_mounts=volume_mounts,
            volumes=volumes,
            image=image,
            command=["/bin/sh", "-c"],
            args=self.get_notebook_args(deployment_name=deployment_name,
                                        ports=ports,
                                        allow_commits=allow_commits),
            ports=target_ports,
            container_name=settings.CONTAINER_NAME_PLUGIN_JOB,
            env_vars=env_vars,
            env_from=env_from,
            resources=resources,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
            role=conf.get('ROLE_LABELS_DASHBOARD'),
            type=conf.get('TYPE_LABELS_RUNNER'),
            service_account_name=conf.get('K8S_SERVICE_ACCOUNT_EXPERIMENTS'))
        deployment_labels = deployments.get_labels(app=conf.get('APP_LABELS_NOTEBOOK'),
                                                   project_name=self.project_name,
                                                   project_uuid=self.project_uuid,
                                                   job_name=self.job_name,
                                                   job_uuid=self.job_uuid,
                                                   role=conf.get('ROLE_LABELS_DASHBOARD'),
                                                   type=conf.get('TYPE_LABELS_RUNNER'))
        dep_resp, _ = self.create_or_update_deployment(name=deployment_name, data=deployment)
        service = services.get_service(
            namespace=self.namespace,
            name=deployment_name,
            labels=deployment_labels,
            ports=ports,
            target_ports=target_ports,
            service_type=self._get_service_type())

        service_resp, _ = self.create_or_update_service(name=deployment_name, data=service)
        results = {'deployment': dep_resp.to_dict(), 'service': service_resp.to_dict()}

        if self._use_ingress():
            annotations = json.loads(settings.K8S_INGRESS_ANNOTATIONS)
            paths = [{
                'path': '/notebook/{}'.format(self.project_name.replace('.', '/')),
                'backend': {
                    'serviceName': deployment_name,
                    'servicePort': ports[0]
                }
            }]
            ingress = ingresses.get_ingress(namespace=self.namespace,
                                            name=deployment_name,
                                            labels=deployment_labels,
                                            annotations=annotations,
                                            paths=paths)
            self.create_or_update_ingress(name=deployment_name, data=ingress)
        return results

    def stop_notebook(self):
        deployment_name = JOB_NAME_FORMAT.format(name=NOTEBOOK_JOB_NAME, job_uuid=self.job_uuid)
        try:
            self.delete_deployment(name=deployment_name, reraise=True)
            self.delete_service(name=deployment_name)
            if self._use_ingress():
                self.delete_ingress(name=deployment_name)
            return True
        except PolyaxonK8SError:
            return False
