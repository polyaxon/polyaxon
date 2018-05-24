import json
import logging
import random

from django.conf import settings

from libs.crypto import get_hmac
from paths.projects import get_project_repos_path
from scheduler.spawners.base import get_pod_volumes
from scheduler.spawners.project_spawner import ProjectSpawner
from scheduler.spawners.templates import constants, deployments, ingresses, pods, services

logger = logging.getLogger('polyaxon.spawners.notebook')


class NotebookSpawner(ProjectSpawner):
    NOTEBOOK_JOB_NAME = 'notebook'
    PORT = 8888

    def get_notebook_url(self):
        return self._get_service_url(self.NOTEBOOK_JOB_NAME)

    def get_notebook_token(self):
        return get_hmac(settings.APP_LABELS_NOTEBOOK, self.project_uuid)

    @staticmethod
    def get_notebook_code_volume():
        volume = pods.get_volume(volume=constants.REPOS_VOLUME,
                                 claim_name=settings.REPOS_CLAIM_NAME,
                                 volume_mount=settings.REPOS_ROOT)

        volume_mount = pods.get_volume_mount(volume=constants.REPOS_VOLUME,
                                             volume_mount=settings.REPOS_ROOT)
        return volume, volume_mount

    def request_notebook_port(self):
        if not self._use_ingress():
            return self.PORT

        labels = 'app={},role={}'.format(settings.APP_LABELS_NOTEBOOK,
                                         settings.ROLE_LABELS_DASHBOARD)
        ports = [service.spec.ports[0].port for service in self.list_services(labels)]
        port = random.randint(*settings.NOTEBOOK_PORT_RANGE)
        while port in ports:
            port = random.randint(*settings.NOTEBOOK_PORT_RANGE)
        return port

    def start_notebook(self, image, resources=None, node_selectors=None):
        ports = [self.request_notebook_port()]
        target_ports = [self.PORT]
        volumes, volume_mounts = get_pod_volumes()
        code_volume, code_volume_mount = self.get_notebook_code_volume()
        volumes.append(code_volume)
        volume_mounts.append(code_volume_mount)
        deployment_name = constants.DEPLOYMENT_NAME.format(
            project_uuid=self.project_uuid, name=self.NOTEBOOK_JOB_NAME)
        notebook_token = self.get_notebook_token()
        notebook_url = self._get_proxy_url(
            namespace=self.namespace,
            job_name=self.NOTEBOOK_JOB_NAME,
            deployment_name=deployment_name,
            port=ports[0])
        notebook_dir = get_project_repos_path(self.project_name)
        notebook_dir = '{}/{}'.format(notebook_dir, notebook_dir.split('/')[-1])
        deployment = deployments.get_deployment(
            namespace=self.namespace,
            app=settings.APP_LABELS_NOTEBOOK,
            name=self.NOTEBOOK_JOB_NAME,
            project_name=self.project_name,
            project_uuid=self.project_uuid,
            volume_mounts=volume_mounts,
            volumes=volumes,
            image=image,
            command=["/bin/sh", "-c"],
            args=[
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
                    notebook_dir=notebook_dir)],
            ports=target_ports,
            container_name=settings.CONTAINER_NAME_PLUGIN_JOB,
            resources=resources,
            node_selector=node_selectors,
            role=settings.ROLE_LABELS_DASHBOARD,
            type=settings.TYPE_LABELS_EXPERIMENT)
        deployment_labels = deployments.get_labels(app=settings.APP_LABELS_NOTEBOOK,
                                                   project_name=self.project_name,
                                                   project_uuid=self.project_uuid,
                                                   role=settings.ROLE_LABELS_DASHBOARD,
                                                   type=settings.TYPE_LABELS_EXPERIMENT)

        self.create_or_update_deployment(name=deployment_name, data=deployment)
        service = services.get_service(
            namespace=self.namespace,
            name=deployment_name,
            labels=deployment_labels,
            ports=ports,
            target_ports=target_ports,
            service_type=self._get_service_type())

        self.create_or_update_service(name=deployment_name, data=service)

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

    def stop_notebook(self):
        deployment_name = constants.DEPLOYMENT_NAME.format(project_uuid=self.project_uuid,
                                                           name=self.NOTEBOOK_JOB_NAME)
        self.delete_deployment(name=deployment_name)
        self.delete_service(name=deployment_name)
        if self._use_ingress():
            self.delete_ingress(name=deployment_name)
