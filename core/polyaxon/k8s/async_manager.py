#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.=

from kubernetes_asyncio import client, config
from kubernetes_asyncio.client.rest import ApiException

from polyaxon.exceptions import PolyaxonK8SError
from polyaxon.k8s.monitor import is_pod_running
from polyaxon.logger import logger


class AsyncK8SManager:
    def __init__(self, namespace="default", in_cluster=False):
        self.namespace = namespace
        self.in_cluster = in_cluster

        self.api_client = None
        self.k8s_api = None
        self.k8s_batch_api = None
        self.k8s_beta_api = None
        self.k8s_custom_object_api = None
        self.k8s_version_api = None

    async def setup(self, k8s_config=None):
        if not k8s_config:
            if self.in_cluster:
                config.load_incluster_config()
            else:
                await config.load_kube_config()
            self.api_client = client.api_client.ApiClient()
        else:
            self.api_client = client.api_client.ApiClient(configuration=k8s_config)

        self.k8s_api = client.CoreV1Api(self.api_client)
        self.k8s_batch_api = client.BatchV1Api(self.api_client)
        self.k8s_beta_api = client.ExtensionsV1beta1Api(self.api_client)
        self.k8s_custom_object_api = client.CustomObjectsApi(self.api_client)
        self.k8s_version_api = client.VersionApi(self.api_client)

    async def close(self):
        if self.api_client:
            await self.api_client.close()

    async def set_namespace(self, namespace):
        self.namespace = namespace

    async def get_pod(self, name, reraise=False):
        try:
            return await self.k8s_api.read_namespaced_pod(
                name=name, namespace=self.namespace
            )
        except ApiException as e:
            if reraise:
                raise PolyaxonK8SError("Connection error: %s" % e) from e
            return None

    async def is_pod_running(self, pod_id: str, container_id: str):
        event = await self.k8s_api.read_namespaced_pod_status(pod_id, self.namespace)
        return is_pod_running(event, container_id)

    async def _list_namespace_resource(self, resource_api, reraise=False, **kwargs):
        try:
            res = await resource_api(namespace=self.namespace, **kwargs)
            return [p for p in res.items]
        except ApiException as e:
            logger.error("K8S error: {}".format(e))
            if reraise:
                raise PolyaxonK8SError("Connection error: %s" % e) from e
            return []

    async def list_pods(self, reraise=False, **kwargs):
        return await self._list_namespace_resource(
            resource_api=self.k8s_api.list_namespaced_pod,
            reraise=reraise,
            **kwargs,
        )

    async def list_jobs(self, reraise=False, **kwargs):
        return await self._list_namespace_resource(
            resource_api=self.k8s_batch_api.list_namespaced_job,
            reraise=reraise,
            **kwargs,
        )

    async def list_custom_objects(
        self, group, version, plural, reraise=False, **kwargs
    ):
        return await self._list_namespace_resource(
            resource_api=self.k8s_custom_object_api.list_namespaced_custom_object,
            reraise=reraise,
            group=group,
            version=version,
            plural=plural,
            **kwargs,
        )

    async def list_services(self, reraise=False, **kwargs):
        return await self._list_namespace_resource(
            resource_api=self.k8s_api.list_namespaced_service,
            reraise=reraise,
            **kwargs,
        )

    async def list_deployments(self, reraise=False, **kwargs):
        return await self._list_namespace_resource(
            resource_api=self.k8s_beta_api.list_namespaced_deployment,
            reraise=reraise,
            **kwargs,
        )

    async def create_custom_object(self, name, group, version, plural, body):
        resp = await self.k8s_custom_object_api.create_namespaced_custom_object(
            group=group,
            version=version,
            plural=plural,
            namespace=self.namespace,
            body=body,
        )
        logger.debug("Custom object `{}` was created".format(name))
        return resp

    async def update_custom_object(self, name, group, version, plural, body):
        resp = await self.k8s_custom_object_api.patch_namespaced_custom_object(
            name=name,
            group=group,
            version=version,
            plural=plural,
            namespace=self.namespace,
            body=body,
        )
        logger.debug("Custom object `{}` was patched".format(name))
        return resp

    async def create_or_update_custom_object(
        self, name, group, version, plural, body, reraise=False
    ):
        try:
            create = await self.create_custom_object(
                name=name, group=group, version=version, plural=plural, body=body
            )
            return create, True

        except ApiException as e_create:
            try:
                update = await self.update_custom_object(
                    name=name, group=group, version=version, plural=plural, body=body
                )
                return update, False
            except ApiException as e:
                if reraise:
                    raise PolyaxonK8SError(
                        "Connection error: creation %s - update %s" % (e_create, e)
                    ) from e
                else:
                    logger.error("K8S error: {}".format(e))

    async def get_custom_object(self, name, group, version, plural, reraise=False):
        try:
            return await self.k8s_custom_object_api.get_namespaced_custom_object(
                name=name,
                group=group,
                version=version,
                plural=plural,
                namespace=self.namespace,
            )
        except ApiException as e:
            if reraise:
                raise PolyaxonK8SError("Connection error: %s" % e) from e
            return None

    async def delete_custom_object(self, name, group, version, plural, reraise=False):
        try:
            await self.k8s_custom_object_api.delete_namespaced_custom_object(
                name=name,
                group=group,
                version=version,
                plural=plural,
                namespace=self.namespace,
                body=client.V1DeleteOptions(),
            )
            logger.debug("Custom object `{}` deleted".format(name))
        except ApiException as e:
            if reraise:
                raise PolyaxonK8SError("Connection error: %s" % e) from e
            else:
                logger.debug("Custom object `{}` was not found".format(name))
