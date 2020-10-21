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

import pytest

from polyaxon.connections.schemas import V1K8sResourceSchema
from polyaxon.env_vars.keys import (
    POLYAXON_KEYS_API_VERSION,
    POLYAXON_KEYS_AUTH_TOKEN,
    POLYAXON_KEYS_AUTHENTICATION_TYPE,
    POLYAXON_KEYS_HEADER,
    POLYAXON_KEYS_HEADER_SERVICE,
    POLYAXON_KEYS_HOST,
    POLYAXON_KEYS_IS_MANAGED,
    POLYAXON_KEYS_K8S_NAMESPACE,
    POLYAXON_KEYS_K8S_POD_ID,
    POLYAXON_KEYS_RUN_INSTANCE,
    POLYAXON_KEYS_SECRET_INTERNAL_TOKEN,
    POLYAXON_KEYS_SECRET_KEY,
)
from polyaxon.exceptions import PolypodException
from polyaxon.k8s import k8s_schemas
from polyaxon.polypod.common.env_vars import (
    get_env_from_config_map,
    get_env_from_config_maps,
    get_env_from_k8s_resources,
    get_env_from_secret,
    get_env_from_secrets,
    get_env_var,
    get_env_vars_from_k8s_resources,
    get_from_config_map,
    get_from_field_ref,
    get_from_secret,
    get_items_from_config_map,
    get_items_from_secret,
    get_kv_env_vars,
    get_resources_env_vars,
    get_run_instance_env_var,
    get_service_env_vars,
    get_str_var,
)
from polyaxon.schemas.types import V1K8sResourceType
from tests.utils import BaseTestCase


@pytest.mark.polypod_mark
class TestEnvVars(BaseTestCase):
    def test_get_str_var(self):
        # String value
        var = get_str_var(value="bar")
        assert var == "bar"
        # Int value
        var = get_str_var(value=1)
        assert var == "1"
        # Dict value
        var = get_str_var(value={"moo": "bar"})
        assert var == '{"moo": "bar"}'
        # Empty value
        var = get_str_var(value=None)
        assert var == ""
        # 0 value
        var = get_str_var(value=0)
        assert var == "0"

    def test_get_env_vars(self):
        # String value
        env_var = get_env_var(name="foo", value="bar")
        assert env_var.name == "foo"
        assert env_var.value == "bar"
        # Int value
        env_var = get_env_var(name="foo", value=1)
        assert env_var.name == "foo"
        assert env_var.value == "1"
        # Dict value
        env_var = get_env_var(name="foo", value={"moo": "bar"})
        assert env_var.name == "foo"
        assert env_var.value == '{"moo": "bar"}'

    def test_get_kv_env_var(self):
        # Empty value
        assert get_kv_env_vars([]) == []
        # Non valid value
        with self.assertRaises(PolypodException):
            get_kv_env_vars([[123, "foo", "bar"]])
        with self.assertRaises(PolypodException):
            get_kv_env_vars([[123]])
        # Valid value
        env_vars = get_kv_env_vars(
            [["foo", {"moo": "bar"}], ("foo", "bar"), ["foo", 1]]
        )
        assert env_vars[0].name == "foo"
        assert env_vars[0].value == '{"moo": "bar"}'
        assert env_vars[1].name == "foo"
        assert env_vars[1].value == "bar"
        assert env_vars[2].name == "foo"
        assert env_vars[2].value == "1"

    def test_get_resources_env_vars(self):
        env_vars = get_resources_env_vars(None)
        assert len(env_vars) == 1
        assert env_vars[0].name == "NVIDIA_VISIBLE_DEVICES"
        assert env_vars[0].value == "none"

        resources = k8s_schemas.V1ResourceRequirements(limits={"cpu": 1})
        env_vars = get_resources_env_vars(resources)
        assert len(env_vars) == 1
        assert env_vars[0].name == "NVIDIA_VISIBLE_DEVICES"
        assert env_vars[0].value == "none"

        resources = k8s_schemas.V1ResourceRequirements(limits={"memory": 1})
        env_vars = get_resources_env_vars(resources)
        assert len(env_vars) == 1
        assert env_vars[0].name == "NVIDIA_VISIBLE_DEVICES"
        assert env_vars[0].value == "none"

        resources = k8s_schemas.V1ResourceRequirements(requests={"nvidia.com/gpu": 1})
        env_vars = get_resources_env_vars(resources)
        assert len(env_vars) == 0
        assert env_vars == []

    def test_get_from_config_map(self):
        env_var = get_from_config_map(
            key_name="foo", config_map_key_name="cm_key", config_map_ref_name="cm_ref"
        )
        assert env_var.name == "foo"
        assert isinstance(env_var.value_from, k8s_schemas.V1EnvVarSource)
        assert env_var.value_from.config_map_key_ref.name == "cm_ref"
        assert env_var.value_from.config_map_key_ref.key == "cm_key"

    def test_get_from_secret(self):
        env_var = get_from_secret(
            key_name="foo", secret_key_name="secret_key", secret_ref_name="secret_ref"
        )
        assert env_var.name == "foo"
        assert isinstance(env_var.value_from, k8s_schemas.V1EnvVarSource)
        assert env_var.value_from.secret_key_ref.name == "secret_ref"
        assert env_var.value_from.secret_key_ref.key == "secret_key"

    def test_get_items_from_secret(self):
        # None
        assert get_items_from_secret(None) == []
        # Secret without items
        secret = V1K8sResourceType(
            name="test", schema=V1K8sResourceSchema(name="test"), is_requested=True
        )
        assert get_items_from_secret(secret) == []
        secret = V1K8sResourceType(
            name="test",
            schema=V1K8sResourceSchema(name="test", items=[]),
            is_requested=True,
        )
        assert get_items_from_secret(secret) == []
        # Secret with items
        secret = V1K8sResourceType(
            name="test",
            schema=V1K8sResourceSchema(name="test", items=["item1", "item2"]),
            is_requested=True,
        )
        assert get_items_from_secret(secret) == [
            get_from_secret("item1", "item1", secret.schema.name),
            get_from_secret("item2", "item2", secret.schema.name),
        ]

    def get_items_from_config_map(self):
        # None
        assert get_items_from_secret(None) == []
        # Secret without items
        secret = V1K8sResourceType(
            name="test", schema=V1K8sResourceSchema(name="test"), is_requested=True
        )
        assert get_items_from_secret(secret) == []
        secret = V1K8sResourceType(
            name="test",
            schema=V1K8sResourceSchema(name="test", items=[]),
            is_requested=True,
        )
        assert get_items_from_secret(secret) == []
        # Secret with items
        secret = V1K8sResourceType(
            name="test",
            schema=V1K8sResourceSchema(name="test", items=["item1", "item2"]),
            is_requested=True,
        )
        assert get_items_from_secret(secret) == [
            get_from_config_map("item1", "item1", secret.schema.name),
            get_from_config_map("item2", "item2", secret.schema.name),
        ]

    def test_get_env_vars_from_k8s_resources(self):
        assert get_env_vars_from_k8s_resources(secrets=[], config_maps=[]) == []
        res1 = V1K8sResourceType(
            name="test", schema=V1K8sResourceSchema(name="test"), is_requested=True
        )
        res2 = V1K8sResourceType(
            name="test2", schema=V1K8sResourceSchema(name="test2"), is_requested=True
        )
        assert (
            get_env_vars_from_k8s_resources(secrets=[res1, res2], config_maps=[]) == []
        )
        assert get_env_vars_from_k8s_resources(secrets=[res1], config_maps=[res2]) == []
        assert (
            get_env_vars_from_k8s_resources(secrets=[], config_maps=[res1, res2]) == []
        )

        res1 = V1K8sResourceType(
            name="test",
            schema=V1K8sResourceSchema(name="test", items=["item1", "item2"]),
            is_requested=True,
        )
        res2 = V1K8sResourceType(
            name="test2",
            schema=V1K8sResourceSchema(name="test2", items=["item1", "item2"]),
            is_requested=True,
        )
        expected = get_items_from_secret(res1) + get_items_from_secret(res2)
        assert (
            get_env_vars_from_k8s_resources(secrets=[res1, res2], config_maps=[])
            == expected
        )
        expected = get_items_from_secret(res1) + get_items_from_config_map(res2)
        assert (
            get_env_vars_from_k8s_resources(secrets=[res1], config_maps=[res2])
            == expected
        )
        expected = get_items_from_config_map(res1) + get_items_from_config_map(res2)
        assert (
            get_env_vars_from_k8s_resources(secrets=[], config_maps=[res1, res2])
            == expected
        )

    def test_get_from_field_ref(self):
        env_var = get_from_field_ref(name="test", field_path="metadata.name")
        assert env_var.name == "test"
        assert env_var.value_from.field_ref.field_path == "metadata.name"

    def test_get_env_from_secret(self):
        # None
        assert get_env_from_secret(secret=None) is None
        # Secret with items
        secret = V1K8sResourceType(
            name="test",
            schema=V1K8sResourceSchema(name="test", items=["item1", "item2"]),
            is_requested=True,
        )
        assert get_env_from_secret(secret=secret) is None

        # Secret
        secret = V1K8sResourceType(
            name="test", schema=V1K8sResourceSchema(name="test_ref"), is_requested=True
        )

        assert get_env_from_secret(secret=secret).secret_ref == {"name": "test_ref"}

    def test_get_env_from_config_map(self):
        # None
        assert get_env_from_config_map(config_map=None) is None
        # ConfigMap with items
        config_map = V1K8sResourceType(
            name="test",
            schema=V1K8sResourceSchema(name="test", items=["item1", "item2"]),
            is_requested=True,
        )
        assert get_env_from_config_map(config_map=config_map) is None

        # ConfigMap
        config_map = V1K8sResourceType(
            name="test", schema=V1K8sResourceSchema(name="test_ref"), is_requested=True
        )

        assert get_env_from_config_map(config_map=config_map).config_map_ref == {
            "name": "test_ref"
        }

    def test_get_env_from_secrets(self):
        # None
        assert get_env_from_secrets(secrets=None) == []
        # Secret with items
        secret1 = V1K8sResourceType(
            name="test1",
            schema=V1K8sResourceSchema(name="test1", items=["item1", "item2"]),
            is_requested=True,
        )
        # Secret
        secret2 = V1K8sResourceType(
            name="test2", schema=V1K8sResourceSchema(name="test_ref"), is_requested=True
        )

        assert get_env_from_secrets(secrets=[secret1, secret2]) == [
            get_env_from_secret(secret2)
        ]

    def test_get_env_from_config_maps(self):
        # None
        assert get_env_from_config_maps(config_maps=None) == []
        # ConfigMap with items
        config_map1 = V1K8sResourceType(
            name="test1",
            schema=V1K8sResourceSchema(name="test1", items=["item1", "item2"]),
            is_requested=True,
        )
        # ConfigMap
        config_map2 = V1K8sResourceType(
            name="test2", schema=V1K8sResourceSchema(name="test_ref"), is_requested=True
        )

        assert get_env_from_config_maps(config_maps=[config_map1, config_map2]) == [
            get_env_from_config_map(config_map2)
        ]

    def test_get_env_from_k8s_resources(self):
        assert get_env_from_k8s_resources(secrets=[], config_maps=[]) == []
        res1 = V1K8sResourceType(
            name="test", schema=V1K8sResourceSchema(name="test"), is_requested=True
        )
        res2 = V1K8sResourceType(
            name="test2", schema=V1K8sResourceSchema(name="test2"), is_requested=True
        )
        expected = get_env_from_secrets(secrets=[res1, res2])
        assert (
            get_env_from_k8s_resources(secrets=[res1, res2], config_maps=[]) == expected
        )
        expected = get_env_from_secrets(secrets=[res1]) + get_env_from_config_maps(
            config_maps=[res2]
        )
        assert (
            get_env_from_k8s_resources(secrets=[res1], config_maps=[res2]) == expected
        )
        expected = get_env_from_config_maps(config_maps=[res1, res2])
        assert (
            get_env_from_k8s_resources(secrets=[], config_maps=[res1, res2]) == expected
        )

    def get_run_instance_env_var(self):
        assert get_run_instance_env_var() == get_from_field_ref(
            name=POLYAXON_KEYS_RUN_INSTANCE,
            field_path="metadata.labels['run_instance']",
        )

    def test_get_service_env_vars_raises_for_internal_and_agent_token(self):
        with self.assertRaises(PolypodException):
            get_service_env_vars(
                header=None,
                service_header=None,
                include_secret_key=False,
                include_internal_token=True,
                include_agent_token=True,
                authentication_type=None,
                polyaxon_default_secret_ref="polyaxon-secret",
                polyaxon_agent_secret_ref="polyaxon-agent",
                api_host="localhost",
                api_version="v1",
                run_instance="foo.bar.runs.run_uuid",
            )

    def test_get_service_env_vars(self):
        env_vars = get_service_env_vars(
            header=None,
            service_header=None,
            include_secret_key=False,
            include_internal_token=False,
            include_agent_token=False,
            authentication_type=None,
            polyaxon_default_secret_ref="polyaxon-secret",
            polyaxon_agent_secret_ref="polyaxon-agent",
            api_host="localhost",
            api_version="v1",
            run_instance="foo.bar.runs.run_uuid",
        )
        assert len(env_vars) == 8
        # TODO: Remove in v1.2 Compatibility API_HOST
        # assert len(env_vars) == 7
        env_var_names = [env_var.name for env_var in env_vars]
        assert POLYAXON_KEYS_K8S_POD_ID in env_var_names
        assert POLYAXON_KEYS_K8S_NAMESPACE in env_var_names
        assert POLYAXON_KEYS_HOST in env_var_names
        assert POLYAXON_KEYS_IS_MANAGED in env_var_names
        assert POLYAXON_KEYS_API_VERSION in env_var_names
        assert POLYAXON_KEYS_K8S_POD_ID in env_var_names
        assert POLYAXON_KEYS_RUN_INSTANCE in env_var_names

        env_vars = get_service_env_vars(
            header="foo",
            service_header="foo",
            include_secret_key=True,
            include_internal_token=True,
            include_agent_token=False,
            authentication_type="foo",
            polyaxon_default_secret_ref="polyaxon-secret",
            polyaxon_agent_secret_ref="polyaxon-agent",
            api_host="localhost",
            api_version="v1",
            run_instance="foo.bar.runs.run_uuid",
        )
        assert len(env_vars) == 13
        # TODO: Remove in v1.2 Compatibility API_HOST
        # assert len(env_vars) == 12
        env_var_names = [env_var.name for env_var in env_vars]
        assert POLYAXON_KEYS_K8S_POD_ID in env_var_names
        assert POLYAXON_KEYS_K8S_NAMESPACE in env_var_names
        assert POLYAXON_KEYS_HOST in env_var_names
        assert POLYAXON_KEYS_IS_MANAGED in env_var_names
        assert POLYAXON_KEYS_API_VERSION in env_var_names
        assert POLYAXON_KEYS_HEADER in env_var_names
        assert POLYAXON_KEYS_HEADER_SERVICE in env_var_names
        assert POLYAXON_KEYS_SECRET_KEY in env_var_names
        assert POLYAXON_KEYS_SECRET_INTERNAL_TOKEN in env_var_names
        assert POLYAXON_KEYS_AUTHENTICATION_TYPE in env_var_names
        assert POLYAXON_KEYS_K8S_POD_ID in env_var_names
        assert POLYAXON_KEYS_RUN_INSTANCE in env_var_names

        env_vars = get_service_env_vars(
            header="foo",
            service_header="foo",
            include_secret_key=True,
            include_internal_token=False,
            include_agent_token=True,
            authentication_type="foo",
            polyaxon_default_secret_ref="polyaxon-secret",
            polyaxon_agent_secret_ref="polyaxon-agent",
            api_host="localhost",
            api_version="v1",
            run_instance="foo.bar.runs.run_uuid",
        )
        assert len(env_vars) == 13
        # TODO: Remove in v1.2 Compatibility API_HOST
        # assert len(env_vars) == 12
        env_var_names = [env_var.name for env_var in env_vars]
        assert POLYAXON_KEYS_K8S_POD_ID in env_var_names
        assert POLYAXON_KEYS_K8S_NAMESPACE in env_var_names
        assert POLYAXON_KEYS_HOST in env_var_names
        assert POLYAXON_KEYS_IS_MANAGED in env_var_names
        assert POLYAXON_KEYS_API_VERSION in env_var_names
        assert POLYAXON_KEYS_HEADER in env_var_names
        assert POLYAXON_KEYS_HEADER_SERVICE in env_var_names
        assert POLYAXON_KEYS_SECRET_KEY in env_var_names
        assert POLYAXON_KEYS_AUTH_TOKEN in env_var_names
        assert POLYAXON_KEYS_AUTHENTICATION_TYPE in env_var_names
        assert POLYAXON_KEYS_K8S_POD_ID in env_var_names
        assert POLYAXON_KEYS_RUN_INSTANCE in env_var_names
