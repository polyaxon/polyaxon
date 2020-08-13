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

from typing import Dict, Iterable, Optional

from polyaxon.polyflow import V1CompiledOperation, V1Plugins, V1Service  # noqa
from polyaxon.polypod.compiler.converters import BaseConverter
from polyaxon.polypod.compiler.converters.base import PlatformConverterMixin
from polyaxon.polypod.custom_resources import get_service_custom_resource
from polyaxon.polypod.mixins import ServiceMixin
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.schemas.types import V1ConnectionType, V1K8sResourceType


class ServiceConverter(ServiceMixin, BaseConverter):
    def get_resource(
        self,
        compiled_operation: V1CompiledOperation,
        artifacts_store: V1ConnectionType,
        connection_by_names: Dict[str, V1ConnectionType],
        secrets: Optional[Iterable[V1K8sResourceType]],
        config_maps: Optional[Iterable[V1K8sResourceType]],
        default_sa: str = None,
        default_auth: bool = False,
    ) -> Dict:
        service = compiled_operation.run  # type: V1Service
        plugins = compiled_operation.plugins or V1Plugins()
        contexts = PluginsContextsSpec.from_config(plugins, default_auth=default_auth)
        replica_spec = self.get_replica_resource(
            plugins=plugins,
            contexts=contexts,
            environment=service.environment,
            volumes=service.volumes,
            init=service.init,
            sidecars=service.sidecars,
            container=service.container,
            artifacts_store=artifacts_store,
            connections=service.connections,
            connection_by_names=connection_by_names,
            secrets=secrets,
            config_maps=config_maps,
            default_sa=default_sa,
            ports=service.ports,
        )
        return get_service_custom_resource(
            namespace=self.namespace,
            main_container=replica_spec.main_container,
            sidecar_containers=replica_spec.sidecar_containers,
            init_containers=replica_spec.init_containers,
            resource_name=self.resource_name,
            volumes=replica_spec.volumes,
            environment=replica_spec.environment,
            termination=compiled_operation.termination,
            collect_logs=contexts.collect_logs,
            sync_statuses=contexts.sync_statuses,
            notifications=plugins.notifications,
            labels=replica_spec.labels,
            annotations=self.annotations,
            ports=service.ports,
        )


class PlatformServiceConverter(PlatformConverterMixin, ServiceConverter):
    pass
