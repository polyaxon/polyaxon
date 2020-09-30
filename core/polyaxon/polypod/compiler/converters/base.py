#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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
# limitations under the License.

import copy

from typing import Any, Dict, Iterable, List, Optional

from polyaxon import pkg, settings
from polyaxon.api import VERSION_V1
from polyaxon.auxiliaries import V1PolyaxonInitContainer, V1PolyaxonSidecarContainer
from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.containers.names import INIT_PREFIX, SIDECAR_PREFIX
from polyaxon.env_vars.keys import POLYAXON_KEYS_NO_API
from polyaxon.exceptions import PolypodException
from polyaxon.k8s import k8s_schemas
from polyaxon.k8s.custom_resources.operation import get_resource_name, get_run_instance
from polyaxon.polyflow import V1Environment, V1Init, V1Plugins
from polyaxon.polypod.common.containers import (
    ensure_container_name,
    sanitize_container_command_args,
)
from polyaxon.polypod.common.env_vars import get_env_var, get_service_env_vars
from polyaxon.polypod.common.mounts import get_mounts
from polyaxon.polypod.init.artifacts import get_artifacts_path_container
from polyaxon.polypod.init.auth import get_auth_context_container
from polyaxon.polypod.init.dockerfile import get_dockerfile_init_container
from polyaxon.polypod.init.git import get_git_init_container
from polyaxon.polypod.init.store import get_store_container
from polyaxon.polypod.main.container import get_main_container
from polyaxon.polypod.pod.volumes import get_pod_volumes
from polyaxon.polypod.sidecar.container import get_sidecar_container
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.polypod.specs.replica import ReplicaSpec
from polyaxon.schemas.types import V1ConnectionType, V1K8sResourceType
from polyaxon.services.auth import AuthenticationTypes
from polyaxon.services.headers import PolyaxonServiceHeaders, PolyaxonServices
from polyaxon.utils.http_utils import clean_host
from polyaxon.utils.list_utils import to_list


class ConverterAbstract:
    def get_main_env_vars(self, **kwargs) -> Optional[List[k8s_schemas.V1EnvVar]]:
        raise NotImplementedError

    def get_polyaxon_sidecar_service_env_vars(
        self,
    ) -> Optional[List[k8s_schemas.V1EnvVar]]:
        raise NotImplementedError

    def get_auth_service_env_vars(self) -> Optional[List[k8s_schemas.V1EnvVar]]:
        raise NotImplementedError

    def get_init_service_env_vars(self) -> Optional[List[k8s_schemas.V1EnvVar]]:
        raise NotImplementedError


class BaseConverter(ConverterAbstract):
    SPEC_KIND = None
    GROUP = None
    API_VERSION = None
    PLURAL = None
    K8S_LABELS_NAME = None
    K8S_LABELS_COMPONENT = None
    K8S_LABELS_PART_OF = None
    MAIN_CONTAINER_ID = None

    def __init__(
        self,
        owner_name: str,
        project_name: str,
        run_name: str,
        run_uuid: str,
        run_path: Optional[str] = None,
        namespace: str = "default",
        internal_auth: bool = False,
        polyaxon_sidecar: V1PolyaxonSidecarContainer = None,
        polyaxon_init: V1PolyaxonInitContainer = None,
    ):
        self.is_valid()
        self.owner_name = owner_name
        self.project_name = project_name
        self.run_name = run_name
        self.run_uuid = run_uuid
        self.run_path = run_path or self.run_uuid
        self.resource_name = self.get_resource_name()
        self.run_instance = self.get_instance()
        self.namespace = namespace
        self.internal_auth = internal_auth
        self.polyaxon_sidecar = polyaxon_sidecar
        self.polyaxon_init = polyaxon_init

    def get_instance(self):
        return get_run_instance(
            owner=self.owner_name, project=self.project_name, run_uuid=self.run_uuid
        )

    def get_resource_name(self):
        return get_resource_name(self.run_uuid)

    def is_valid(self):
        if not self.SPEC_KIND:
            raise PolypodException(
                "Please make sure that a spawner subclass has a valid SPEC_KIND"
            )
        if not self.GROUP:
            raise PolypodException(
                "Please make sure that a spawner subclass has a valid GROUP"
            )
        if not self.API_VERSION:
            raise PolypodException(
                "Please make sure that a spawner subclass has a valid API_VERSION"
            )
        if not self.PLURAL:
            raise PolypodException(
                "Please make sure that a spawner subclass has a valid PLURAL"
            )
        if not self.K8S_LABELS_NAME:
            raise PolypodException(
                "Please make sure that a spawner subclass has a valid K8S_LABELS_NAME"
            )
        if not self.K8S_LABELS_COMPONENT:
            raise PolypodException(
                "Please make sure that a spawner subclass has a valid K8S_LABELS_COMPONENT"
            )
        if not self.K8S_LABELS_PART_OF:
            raise PolypodException(
                "Please make sure that a spawner subclass has a valid K8S_LABELS_PART_OF"
            )

    def get_recommended_labels(self, version: str):
        return {
            "app.kubernetes.io/name": self.run_name[:63]
            if self.run_name
            else self.run_name,
            "app.kubernetes.io/instance": self.run_uuid,
            "app.kubernetes.io/version": version,
            "app.kubernetes.io/part-of": self.K8S_LABELS_PART_OF,
            "app.kubernetes.io/component": self.K8S_LABELS_COMPONENT,
            "app.kubernetes.io/managed-by": "polyaxon",
        }

    @property
    def annotations(self):
        return {
            "operation.polyaxon.com/name": self.run_name,
            "operation.polyaxon.com/owner": self.owner_name,
            "operation.polyaxon.com/project": self.project_name,
        }

    def get_labels(self, version: str, labels: Dict):
        labels = labels or {}
        labels = copy.copy(labels)
        labels.update(self.get_recommended_labels(version=version))
        return labels

    @staticmethod
    def get_by_name(values: List[Any]):
        return {c.name: c for c in values}

    def get_main_env_vars(self, **kwargs) -> Optional[List[k8s_schemas.V1EnvVar]]:
        return None

    def get_polyaxon_sidecar_service_env_vars(
        self,
    ) -> Optional[List[k8s_schemas.V1EnvVar]]:
        if settings.CLIENT_CONFIG.no_api:
            return [get_env_var(name=POLYAXON_KEYS_NO_API, value=True)]
        return None

    def get_auth_service_env_vars(self) -> Optional[List[k8s_schemas.V1EnvVar]]:
        return None

    def get_init_service_env_vars(self) -> Optional[List[k8s_schemas.V1EnvVar]]:
        if settings.CLIENT_CONFIG.no_api:
            return [get_env_var(name=POLYAXON_KEYS_NO_API, value=True)]
        return None

    def get_main_container(
        self,
        main_container: k8s_schemas.V1Container,
        contexts: PluginsContextsSpec,
        artifacts_store: V1ConnectionType,
        connections: List[str],
        init_connections: Optional[List[V1Init]],
        connection_by_names: Dict[str, V1ConnectionType],
        log_level: str,
        secrets: Optional[Iterable[V1K8sResourceType]],
        config_maps: Optional[Iterable[V1K8sResourceType]],
        kv_env_vars: List[List] = None,
        ports: List[int] = None,
    ) -> k8s_schemas.V1Container:
        env = self.get_main_env_vars()
        volume_mounts = get_mounts(
            use_auth_context=contexts.auth,
            use_artifacts_context=False,  # Main container has a check and handling for this
            use_docker_context=contexts.docker,
            use_shm_context=contexts.shm,
        )

        return get_main_container(
            container_id=self.MAIN_CONTAINER_ID,
            main_container=main_container,
            volume_mounts=volume_mounts,
            log_level=log_level,
            contexts=contexts,
            artifacts_store=artifacts_store,
            connections=connections,
            init=init_connections,
            connection_by_names=connection_by_names,
            secrets=secrets,
            config_maps=config_maps,
            kv_env_vars=kv_env_vars,
            env=env,
            ports=ports,
            run_path=self.run_path,
        )

    def get_sidecar_containers(
        self,
        polyaxon_sidecar: V1PolyaxonSidecarContainer,
        contexts: PluginsContextsSpec,
        artifacts_store: V1ConnectionType,
        sidecar_containers: List[k8s_schemas.V1Container],
    ) -> List[k8s_schemas.V1Container]:
        sidecar_containers = [
            ensure_container_name(container=c, prefix=SIDECAR_PREFIX)
            for c in to_list(sidecar_containers, check_none=True)
        ]
        polyaxon_sidecar_container = get_sidecar_container(
            container_id=self.MAIN_CONTAINER_ID,
            polyaxon_sidecar=polyaxon_sidecar,
            env=self.get_polyaxon_sidecar_service_env_vars(),
            artifacts_store=artifacts_store,
            contexts=contexts,
            run_path=self.run_path,
        )
        containers = to_list(polyaxon_sidecar_container, check_none=True)
        containers += sidecar_containers
        return [sanitize_container_command_args(c) for c in containers]

    def handle_init_connections(
        self,
        polyaxon_init: V1PolyaxonInitContainer,
        artifacts_store: V1ConnectionType,
        init_connections: List[V1Init],
        connection_by_names: Dict[str, V1ConnectionType],
        contexts: PluginsContextsSpec,
    ) -> List[k8s_schemas.V1Container]:
        containers = []

        # Prepare connections that Polyaxon can init automatically
        for init_connection in init_connections:
            if init_connection.connection:
                connection_spec = connection_by_names.get(init_connection.connection)
                if init_connection.git:  # Update the default schema
                    connection_spec.schema.patch(init_connection.git)
                if V1ConnectionKind.is_git(connection_spec.kind):
                    containers.append(
                        get_git_init_container(
                            polyaxon_init=polyaxon_init,
                            connection=connection_spec,
                            container=init_connection.container,
                            env=self.get_init_service_env_vars(),
                            mount_path=init_connection.path,
                            contexts=contexts,
                            track=True,
                        )
                    )
                if V1ConnectionKind.is_artifact(connection_spec.kind):
                    containers.append(
                        get_store_container(
                            polyaxon_init=polyaxon_init,
                            connection=connection_spec,
                            artifacts=init_connection.artifacts,
                            container=init_connection.container,
                            env=self.get_init_service_env_vars(),
                            mount_path=init_connection.path,
                            is_default_artifacts_store=artifacts_store
                            and init_connection.connection == artifacts_store.name,
                        )
                    )
            else:
                # artifacts init without connection should default to the artifactsStore
                if init_connection.artifacts:
                    containers.append(
                        get_store_container(
                            polyaxon_init=polyaxon_init,
                            connection=artifacts_store,
                            artifacts=init_connection.artifacts,
                            container=init_connection.container,
                            env=self.get_init_service_env_vars(),
                            mount_path=init_connection.path,
                            is_default_artifacts_store=True,
                        )
                    )
                # git init without connection
                if init_connection.git:
                    git_name = init_connection.git.get_name()
                    containers.append(
                        get_git_init_container(
                            polyaxon_init=polyaxon_init,
                            connection=V1ConnectionType(
                                name=git_name,
                                kind=V1ConnectionKind.GIT,
                                schema=init_connection.git,
                                secret=None,
                            ),
                            container=init_connection.container,
                            env=self.get_init_service_env_vars(),
                            mount_path=init_connection.path,
                            contexts=contexts,
                            track=False,
                        )
                    )
                # Dockerfile initialization
                if init_connection.dockerfile:
                    containers.append(
                        get_dockerfile_init_container(
                            polyaxon_init=polyaxon_init,
                            dockerfile_args=init_connection.dockerfile,
                            env=self.get_init_service_env_vars(),
                            mount_path=init_connection.path,
                            contexts=contexts,
                            run_path=self.run_path,
                            run_instance=self.run_instance,
                        )
                    )

        return containers

    def get_init_containers(
        self,
        polyaxon_init: V1PolyaxonInitContainer,
        contexts: PluginsContextsSpec,
        artifacts_store: V1ConnectionType,
        init_connections: List[V1Init],
        init_containers: List[k8s_schemas.V1Container],
        connection_by_names: Dict[str, V1ConnectionType],
    ) -> List[k8s_schemas.V1Container]:
        init_containers = [
            ensure_container_name(container=c, prefix=INIT_PREFIX)
            for c in to_list(init_containers, check_none=True)
        ]
        init_connections = to_list(init_connections, check_none=True)
        containers = []

        # Add auth context
        if contexts and contexts.auth:
            containers.append(
                get_auth_context_container(
                    polyaxon_init=polyaxon_init, env=self.get_auth_service_env_vars()
                )
            )

        # Add outputs
        if contexts and contexts.collect_artifacts:
            containers += to_list(
                get_artifacts_path_container(
                    polyaxon_init=polyaxon_init,
                    artifacts_store=artifacts_store,
                    run_path=self.run_path,
                    auto_resume=contexts.auto_resume,
                ),
                check_none=True,
            )

        containers += self.handle_init_connections(
            polyaxon_init=polyaxon_init,
            artifacts_store=artifacts_store,
            init_connections=init_connections,
            connection_by_names=connection_by_names,
            contexts=contexts,
        )
        init_containers = containers + init_containers
        return [sanitize_container_command_args(c) for c in init_containers]

    def filter_containers_from_init(
        self, init: List[V1Init]
    ) -> List[k8s_schemas.V1Container]:
        return [i.container for i in init if not i.has_connection()]

    def filter_connections_from_init(self, init: List[V1Init]) -> List[V1Init]:
        return [i for i in init if i.has_connection()]

    def get_replica_resource(
        self,
        environment: V1Environment,
        plugins: V1Plugins,
        contexts: PluginsContextsSpec,
        volumes: List[k8s_schemas.V1Volume],
        init: List[V1Init],
        sidecars: List[k8s_schemas.V1Container],
        container: k8s_schemas.V1Container,
        artifacts_store: V1ConnectionType,
        connections: List[str],
        connection_by_names: Dict[str, V1ConnectionType],
        secrets: Optional[Iterable[V1K8sResourceType]],
        config_maps: Optional[Iterable[V1K8sResourceType]],
        default_sa: str = None,
        ports: List[int] = None,
        num_replicas: int = None,
    ) -> ReplicaSpec:
        volumes = volumes or []
        init = init or []
        sidecars = sidecars or []
        connections = connections or []
        environment = environment or V1Environment()
        environment.service_account_name = (
            environment.service_account_name or default_sa
        )

        init_connections = self.filter_connections_from_init(init=init)

        volumes = get_pod_volumes(
            contexts=contexts,
            artifacts_store=artifacts_store,
            init_connections=init_connections,
            connections=connections,
            connection_by_names=connection_by_names,
            secrets=secrets,
            config_maps=config_maps,
            volumes=volumes,
        )

        init_containers = self.get_init_containers(
            polyaxon_init=self.polyaxon_init,
            contexts=contexts,
            artifacts_store=artifacts_store,
            init_connections=init_connections,
            init_containers=self.filter_containers_from_init(init=init),
            connection_by_names=connection_by_names,
        )

        sidecar_containers = self.get_sidecar_containers(
            polyaxon_sidecar=self.polyaxon_sidecar,
            contexts=contexts,
            artifacts_store=artifacts_store,
            sidecar_containers=sidecars,
        )

        main_container = self.get_main_container(
            main_container=container,
            contexts=contexts,
            artifacts_store=artifacts_store,
            connections=connections,
            init_connections=init_connections,
            connection_by_names=connection_by_names,
            log_level=plugins.log_level,
            secrets=secrets,
            config_maps=config_maps,
            ports=ports,
        )

        labels = self.get_labels(version=pkg.VERSION, labels=environment.labels)
        return ReplicaSpec(
            volumes=volumes,
            init_containers=init_containers,
            sidecar_containers=sidecar_containers,
            main_container=main_container,
            labels=labels,
            environment=environment,
            num_replicas=num_replicas,
        )

    def get_resource(self, **kwargs) -> Dict:
        raise NotImplementedError


class PlatformConverterMixin(ConverterAbstract):
    def get_service_env_vars(
        self,
        service_header: str,
        header: str = None,
        include_secret_key: bool = False,
        include_internal_token: bool = False,
        include_agent_token: bool = False,
        authentication_type: str = None,
    ) -> List[k8s_schemas.V1EnvVar]:
        header = header or PolyaxonServiceHeaders.SERVICE
        return get_service_env_vars(
            header=header,
            service_header=service_header,
            authentication_type=authentication_type,
            include_secret_key=include_secret_key,
            include_internal_token=include_internal_token,
            include_agent_token=include_agent_token,
            polyaxon_default_secret_ref=settings.AGENT_CONFIG.app_secret_name,
            polyaxon_agent_secret_ref=settings.AGENT_CONFIG.agent_secret_name,
            api_host=clean_host(settings.CLIENT_CONFIG.host),
            api_version=VERSION_V1,
            run_instance=self.run_instance,
        )

    def get_main_env_vars(self, **kwargs):
        return self.get_service_env_vars(service_header=PolyaxonServices.RUNNER)

    def get_auth_service_env_vars(self) -> List[k8s_schemas.V1EnvVar]:
        return self.get_service_env_vars(
            service_header=PolyaxonServices.INITIALIZER,
            include_internal_token=self.internal_auth,
            include_agent_token=not self.internal_auth,
            authentication_type=(
                AuthenticationTypes.INTERNAL_TOKEN
                if self.internal_auth
                else AuthenticationTypes.TOKEN
            ),
            header=(
                PolyaxonServiceHeaders.INTERNAL
                if self.internal_auth
                else PolyaxonServiceHeaders.SERVICE
            ),
        )

    def get_polyaxon_sidecar_service_env_vars(self) -> List[k8s_schemas.V1EnvVar]:
        return self.get_service_env_vars(
            service_header=PolyaxonServices.SIDECAR,
            authentication_type=AuthenticationTypes.TOKEN,
            header=PolyaxonServiceHeaders.SERVICE,
        )

    def get_init_service_env_vars(self) -> List[k8s_schemas.V1EnvVar]:
        return self.get_service_env_vars(
            service_header=PolyaxonServices.INITIALIZER,
            authentication_type=AuthenticationTypes.TOKEN,
            header=PolyaxonServiceHeaders.SERVICE,
        )
