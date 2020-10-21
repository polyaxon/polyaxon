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
from polyaxon import settings
from polyaxon.auxiliaries import V1PolyaxonInitContainer, V1PolyaxonSidecarContainer
from polyaxon.connections.kinds import V1ConnectionKind
from polyaxon.connections.schemas import (
    V1BucketConnection,
    V1ClaimConnection,
    V1GitConnection,
    V1K8sResourceSchema,
)
from polyaxon.k8s import k8s_schemas
from polyaxon.polyflow import V1Init, V1Plugins
from polyaxon.polypod.common.mounts import get_mounts
from polyaxon.polypod.compiler.converters import PlatformJobConverter
from polyaxon.polypod.init.artifacts import get_artifacts_path_container
from polyaxon.polypod.init.auth import get_auth_context_container
from polyaxon.polypod.init.dockerfile import get_dockerfile_init_container
from polyaxon.polypod.init.git import get_git_init_container
from polyaxon.polypod.init.store import get_store_container
from polyaxon.polypod.main.container import get_main_container
from polyaxon.polypod.sidecar.container import get_sidecar_container
from polyaxon.polypod.specs.contexts import PluginsContextsSpec
from polyaxon.schemas.types import (
    V1ArtifactsType,
    V1ConnectionType,
    V1DockerfileType,
    V1K8sResourceType,
)
from polyaxon.services.headers import PolyaxonServices
from tests.utils import BaseTestCase


class DummyConverter(PlatformJobConverter):
    SPEC_KIND = "dumy"
    K8S_ANNOTATIONS_KIND = "dummy-name"
    MAIN_CONTAINER_ID = "dummy"


class TestJobConverter(BaseTestCase):
    SET_AGENT_SETTINGS = True

    def setUp(self):
        super().setUp()
        settings.AGENT_CONFIG.app_secret_name = "polyaxon"
        settings.AGENT_CONFIG.agent_secret_name = "agent"
        settings.CLIENT_CONFIG.host = "https://polyaxon.com"
        self.converter = DummyConverter(
            owner_name="owner-name",
            project_name="project-name",
            run_name="run-name",
            run_uuid="run_uuid",
        )

    def test_get_main_env_vars(self):
        env_vars = self.converter.get_main_env_vars()
        assert env_vars == self.converter.get_service_env_vars(
            service_header=PolyaxonServices.RUNNER
        )

    def test_get_init_containers_with_auth(self):
        containers = self.converter.get_init_containers(
            polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(collect_logs=False, collect_artifacts=False, auth=True)
            ),
            artifacts_store=None,
            init_connections=None,
            connection_by_names={},
            init_containers=[],
        )
        assert containers == [
            get_auth_context_container(
                polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
                env=self.converter.get_auth_service_env_vars(),
            )
        ]

    def test_get_init_containers_none(self):
        containers = self.converter.get_init_containers(
            polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
            contexts=None,
            artifacts_store=None,
            init_connections=None,
            connection_by_names={},
            init_containers=[],
        )
        assert containers == []

    def test_get_init_containers_with_claim_outputs(self):
        store = V1ConnectionType(
            name="test_claim",
            kind=V1ConnectionKind.VOLUME_CLAIM,
            schema=V1ClaimConnection(
                mount_path="/claim/path", volume_claim="claim", read_only=True
            ),
        )

        # No context to enable the outputs
        containers = self.converter.get_init_containers(
            contexts=None,
            artifacts_store=store.name,
            init_connections=None,
            connection_by_names={},
            init_containers=[],
            polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
        )
        assert containers == []

        # Enable outputs
        containers = self.converter.get_init_containers(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(collect_artifacts=True, collect_logs=False)
            ),
            artifacts_store=store,
            connection_by_names={},
            init_connections=None,
            init_containers=[],
            polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
        )
        assert containers == [
            get_artifacts_path_container(
                polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
                artifacts_store=store,
                run_path=self.converter.run_path,
                auto_resume=True,
            ),
        ]

        # Use store for init
        containers = self.converter.get_init_containers(
            contexts=None,
            artifacts_store=None,
            connection_by_names={store.name: store},
            init_connections=[V1Init(connection=store.name)],
            init_containers=[],
            polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
        )
        assert containers == [
            get_store_container(
                polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
                connection=store,
                artifacts=None,
                env=self.converter.get_init_service_env_vars(),
            )
        ]

        # Use store for init and outputs
        containers = self.converter.get_init_containers(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(collect_artifacts=True, collect_logs=False)
            ),
            artifacts_store=store,
            init_connections=[V1Init(connection=store.name)],
            connection_by_names={store.name: store},
            init_containers=[],
            polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
        )
        assert containers == [
            get_artifacts_path_container(
                polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
                artifacts_store=store,
                run_path=self.converter.run_path,
                auto_resume=True,
            ),
            get_store_container(
                polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
                connection=store,
                artifacts=None,
                env=self.converter.get_init_service_env_vars(),
                is_default_artifacts_store=True,
            ),
        ]

        # Add Store
        store1 = V1ConnectionType(
            name="test_gcs",
            kind=V1ConnectionKind.S3,
            schema=V1BucketConnection(bucket="s3://foo"),
            secret=None,
        )

        containers = self.converter.get_init_containers(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(collect_artifacts=True, collect_logs=False, auth=True)
            ),
            artifacts_store=store,
            init_connections=[
                V1Init(
                    connection=store.name,
                    artifacts=V1ArtifactsType(files=["/foo", "/bar"]),
                ),
                V1Init(
                    connection=store1.name,
                    artifacts=V1ArtifactsType(files=["/foo", "/bar"]),
                ),
            ],
            connection_by_names={store.name: store, store1.name: store1},
            init_containers=[],
            polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
        )
        assert containers == [
            get_auth_context_container(
                polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
                env=self.converter.get_auth_service_env_vars(),
            ),
            get_artifacts_path_container(
                polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
                artifacts_store=store,
                run_path=self.converter.run_path,
                auto_resume=True,
            ),
            get_store_container(
                polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
                connection=store,
                artifacts=V1ArtifactsType(files=["/foo", "/bar"]),
                env=self.converter.get_init_service_env_vars(),
                is_default_artifacts_store=True,
            ),
            get_store_container(
                polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
                connection=store1,
                artifacts=V1ArtifactsType(files=["/foo", "/bar"]),
                env=self.converter.get_init_service_env_vars(),
            ),
        ]

    def test_get_init_containers_with_dockerfiles(self):
        dockerfile_args1 = V1DockerfileType(
            image="foo/test", lang_env="LANG", env=[], run=["step1", "step2"]
        )
        dockerfile_args2 = V1DockerfileType(
            image="foo/test",
            lang_env="LANG",
            env=[],
            run=["step1", "step2"],
            filename="dockerfile2",
            path="/test",
        )
        containers = self.converter.get_init_containers(
            contexts=None,
            artifacts_store=None,
            init_connections=[
                V1Init(dockerfile=dockerfile_args1),
                V1Init(dockerfile=dockerfile_args2, path="/test"),
            ],
            init_containers=[],
            connection_by_names={},
            polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
        )
        for container in containers:
            container.name = ""
        expected_containers = [
            get_dockerfile_init_container(
                dockerfile_args=dockerfile_args1,
                polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
                env=self.converter.get_init_service_env_vars(),
                contexts=None,
                run_path=self.converter.run_path,
                run_instance=self.converter.run_instance,
            ),
            get_dockerfile_init_container(
                dockerfile_args=dockerfile_args2,
                polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
                env=self.converter.get_init_service_env_vars(),
                mount_path="/test",
                contexts=None,
                run_path=self.converter.run_path,
                run_instance=self.converter.run_instance,
            ),
        ]
        for container in expected_containers:
            container.name = ""

        assert expected_containers == containers

    def test_get_init_containers_with_git_without_connection(self):
        git1 = V1GitConnection(revision="test", url="https://test.com")
        git2 = V1GitConnection(revision="test", url="https://test.com")
        containers = self.converter.get_init_containers(
            contexts=None,
            artifacts_store=None,
            init_connections=[
                V1Init(git=git1, container=k8s_schemas.V1Container(name="test")),
                V1Init(git=git2, path="/test"),
            ],
            init_containers=[],
            connection_by_names={},
            polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
        )
        assert containers == [
            get_git_init_container(
                connection=V1ConnectionType(
                    name=git1.get_name(), kind=V1ConnectionKind.GIT, schema=git1
                ),
                polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
                env=self.converter.get_init_service_env_vars(),
                contexts=None,
            ),
            get_git_init_container(
                container=k8s_schemas.V1Container(name="test"),
                connection=V1ConnectionType(
                    name=git2.get_name(), kind=V1ConnectionKind.GIT, schema=git1
                ),
                mount_path="/test",
                polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
                env=self.converter.get_init_service_env_vars(),
                contexts=None,
            ),
        ]

    def test_get_init_containers_with_store_outputs(self):
        store = V1ConnectionType(
            name="test_gcs",
            kind=V1ConnectionKind.S3,
            schema=V1BucketConnection(bucket="s3://foo"),
        )

        # No context
        containers = self.converter.get_init_containers(
            contexts=None,
            artifacts_store=store,
            init_connections=[],
            init_containers=[],
            connection_by_names={},
            polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
        )
        assert containers == []

        # With context
        containers = self.converter.get_init_containers(
            contexts=PluginsContextsSpec.from_config(
                V1Plugins(collect_artifacts=True, collect_logs=False, auth=True)
            ),
            artifacts_store=store,
            init_connections=[],
            init_containers=[],
            connection_by_names={},
            polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
        )
        assert containers == [
            get_auth_context_container(
                polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
                env=self.converter.get_auth_service_env_vars(),
            ),
            get_artifacts_path_container(
                polyaxon_init=V1PolyaxonInitContainer(image="foo/foo"),
                artifacts_store=store,
                run_path=self.converter.run_path,
                auto_resume=True,
            ),
        ]

    def test_get_sidecars(self):
        assert (
            self.converter.get_sidecar_containers(
                contexts=None,
                artifacts_store=None,
                sidecar_containers=[],
                polyaxon_sidecar=V1PolyaxonSidecarContainer(
                    image="sidecar/sidecar", sleep_interval=12, sync_interval=-1
                ),
            )
            == []
        )

        # Store with single path, no secret is passed and not required
        store = V1ConnectionType(
            name="test",
            kind=V1ConnectionKind.S3,
            schema=V1BucketConnection(bucket="s3://foo"),
        )
        contexts = PluginsContextsSpec.from_config(
            V1Plugins(collect_logs=True, collect_artifacts=True, auth=True)
        )
        assert self.converter.get_sidecar_containers(
            contexts=contexts,
            artifacts_store=store,
            sidecar_containers=[],
            polyaxon_sidecar=V1PolyaxonSidecarContainer(
                image="sidecar/sidecar", sleep_interval=12, sync_interval=12
            ),
        ) == [
            get_sidecar_container(
                container_id="dummy",
                contexts=contexts,
                env=self.converter.get_polyaxon_sidecar_service_env_vars(),
                polyaxon_sidecar=V1PolyaxonSidecarContainer(
                    image="sidecar/sidecar", sleep_interval=12, sync_interval=12
                ),
                artifacts_store=store,
                run_path=self.converter.run_path,
            )
        ]

        secret1 = V1K8sResourceType(
            name="test1",
            schema=V1K8sResourceSchema(name="ref1", items=["item1", "item2"]),
            is_requested=True,
        )
        store.secret = secret1.schema

        polyaxon_sidecar = V1PolyaxonSidecarContainer(
            image="sidecar/sidecar",
            image_pull_policy=None,
            sleep_interval=12,
            sync_interval=-1,
        )

        assert self.converter.get_sidecar_containers(
            contexts=contexts,
            artifacts_store=store,
            polyaxon_sidecar=polyaxon_sidecar,
            sidecar_containers=[],
        ) == [
            get_sidecar_container(
                container_id="dummy",
                contexts=contexts,
                env=self.converter.get_polyaxon_sidecar_service_env_vars(),
                polyaxon_sidecar=polyaxon_sidecar,
                artifacts_store=store,
                run_path=self.converter.run_path,
            )
        ]

    def test_main_container(self):
        store = V1ConnectionType(
            name="test_gcs",
            kind=V1ConnectionKind.S3,
            schema=V1BucketConnection(bucket="s3://foo"),
            secret=None,
        )
        contexts = PluginsContextsSpec.from_config(
            V1Plugins.from_dict({}), default_auth=True
        )
        main_container = k8s_schemas.V1Container(
            name="main",
            image="foo/test",
            image_pull_policy="IfNotPresent",
            command=["foo", "bar"],
            args=["arg1", "arg2"],
        )
        container = self.converter.get_main_container(
            main_container=main_container,
            contexts=contexts,
            artifacts_store=store,
            init_connections=[],
            connections=[],
            connection_by_names={},
            log_level="info",
            secrets=[],
            config_maps=[],
            kv_env_vars=[],
            ports=None,
        )
        expected_container = get_main_container(
            container_id="dummy",
            main_container=main_container,
            contexts=contexts,
            volume_mounts=get_mounts(
                use_auth_context=True,
                use_artifacts_context=False,
                use_docker_context=False,
                use_shm_context=False,
            ),
            log_level="info",
            artifacts_store=store,
            connections=[],
            init=[],
            connection_by_names={},
            secrets=[],
            config_maps=[],
            kv_env_vars=[],
            env=self.converter.get_main_env_vars(),
            ports=None,
            run_path="/test",
        )

        assert container == expected_container
