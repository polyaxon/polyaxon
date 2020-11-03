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

from polyaxon import pkg, types
from polyaxon.config_reader.utils import deep_update
from polyaxon.containers.names import MAIN_JOB_CONTAINER
from polyaxon.polyaxonfile import OperationSpecification
from polyaxon.polyflow import V1Component, V1Operation, V1RunKind
from polyaxon.schemas.patch_strategy import V1PatchStrategy
from polyaxon.utils.tz_utils import now
from tests.utils import BaseTestCase


@pytest.mark.polyaxonfile_mark
class TestPatchSpecifications(BaseTestCase):
    DEFAULT_INT_VALUE = 2
    DEFAULT_DT_VALUE = now().isoformat()
    DEFAULT_STR_VALUE = "test"
    PATCH_INT_VALUE = 13
    PATCH_DT_VALUE = now().isoformat()
    PATCH_STR_VALUE = "patch"

    def get_empty_operation(self):
        return OperationSpecification.read(
            {"version": pkg.SCHEMA_VERSION, "hubRef": "test"}
        )

    def get_full_operation(self):
        return OperationSpecification.read(
            {
                "version": pkg.SCHEMA_VERSION,
                "name": self.DEFAULT_STR_VALUE,
                "description": self.DEFAULT_STR_VALUE,
                "tags": [
                    "{}1".format(self.DEFAULT_STR_VALUE),
                    "{}2".format(self.DEFAULT_STR_VALUE),
                ],
                "presets": [self.DEFAULT_STR_VALUE],
                "queue": "{}/{}".format(self.DEFAULT_STR_VALUE, self.DEFAULT_STR_VALUE),
                "cache": {
                    "disable": False,
                    "ttl": self.DEFAULT_INT_VALUE,
                },
                "termination": {
                    "maxRetries": self.DEFAULT_INT_VALUE,
                    "ttl": self.DEFAULT_INT_VALUE,
                    "timeout": self.DEFAULT_INT_VALUE,
                },
                "plugins": {
                    "auth": False,
                    "shm": False,
                    "collectLogs": False,
                    "collectArtifacts": False,
                    "collectResources": False,
                },
                "actions": [
                    {"hubRef": "{}1".format(self.DEFAULT_STR_VALUE)},
                    {
                        "hubRef": "{}2".format(self.DEFAULT_STR_VALUE),
                        "label": "customLabel",
                        "many": True,
                    },
                ],
                "hooks": [
                    {
                        "trigger": "succeeded",
                        "connection": "{}1".format(self.DEFAULT_STR_VALUE),
                    },
                    {
                        "connection": "{}1".format(self.DEFAULT_STR_VALUE),
                        "hubRef": "{}2".format(self.DEFAULT_STR_VALUE),
                    },
                ],
                "params": {
                    "patch-key1": {"value": "{}2".format(self.DEFAULT_STR_VALUE)},
                    "patch-key2": {"value": "{}1".format(self.DEFAULT_STR_VALUE)},
                },
                "runPatch": {
                    "init": [
                        {
                            "connection": self.DEFAULT_STR_VALUE,
                            "git": {"revision": self.DEFAULT_STR_VALUE},
                        }
                    ],
                    "connections": [
                        "{}1".format(self.DEFAULT_STR_VALUE),
                        "{}2".format(self.DEFAULT_STR_VALUE),
                    ],
                    "container": {
                        "resources": {"requests": {"cpu": self.DEFAULT_INT_VALUE}}
                    },
                    "environment": {
                        "nodeSelector": {"polyaxon": "core"},
                        "serviceAccountName": self.DEFAULT_STR_VALUE,
                        "imagePullSecrets": [
                            "{}1".format(self.DEFAULT_STR_VALUE),
                            "{}2".format(self.DEFAULT_STR_VALUE),
                        ],
                    },
                },
                "schedule": {
                    "kind": "cron",
                    "cron": "0 0 * * *",
                    "startAt": self.DEFAULT_DT_VALUE,
                    "endAt": self.DEFAULT_DT_VALUE,
                },
                "events": None,
                "matrix": {
                    "concurrency": self.DEFAULT_INT_VALUE,
                    "kind": "mapping",
                    "values": [
                        {"a": self.DEFAULT_INT_VALUE},
                        {"b": self.DEFAULT_INT_VALUE},
                    ],
                },
                "dependencies": [
                    "{}1".format(self.DEFAULT_STR_VALUE),
                    "{}2".format(self.DEFAULT_STR_VALUE),
                ],
                "trigger": "all_succeeded",
                "conditions": self.DEFAULT_STR_VALUE,
                "skipOnUpstreamSkip": True,
                "hubRef": self.DEFAULT_STR_VALUE,
            }
        )

    def get_full_operation_with_component(self):
        operation = self.get_full_operation()
        config_dict = {
            "inputs": [{"name": "param1", "type": types.INT}],
            "run": {"kind": V1RunKind.JOB, "container": {"image": "test"}},
        }
        operation.component = V1Component.from_dict(config_dict)
        return operation

    def get_full_preset(self):
        return OperationSpecification.read(
            {
                "version": pkg.SCHEMA_VERSION,
                "name": self.PATCH_STR_VALUE,
                "isPreset": True,
                "description": self.PATCH_STR_VALUE,
                "tags": [
                    "{}1".format(self.PATCH_STR_VALUE),
                    "{}2".format(self.PATCH_STR_VALUE),
                ],
                "presets": [self.PATCH_STR_VALUE],
                "queue": "{}/{}".format(self.PATCH_STR_VALUE, self.PATCH_STR_VALUE),
                "cache": {
                    "disable": True,
                    "ttl": self.PATCH_INT_VALUE,
                },
                "termination": {
                    "maxRetries": self.PATCH_INT_VALUE,
                    "ttl": self.PATCH_INT_VALUE,
                    "timeout": self.PATCH_INT_VALUE,
                },
                "plugins": {
                    "auth": True,
                    "shm": True,
                    "collectLogs": True,
                    "collectArtifacts": True,
                    "collectResources": True,
                },
                "actions": [
                    {"hubRef": "{}1".format(self.PATCH_STR_VALUE)},
                    {
                        "hubRef": "{}2".format(self.PATCH_STR_VALUE),
                        "label": "customLabel",
                        "many": True,
                    },
                ],
                "hooks": [
                    {
                        "trigger": "succeeded",
                        "connection": "{}1".format(self.PATCH_STR_VALUE),
                    },
                    {
                        "connection": "{}1".format(self.PATCH_STR_VALUE),
                        "hubRef": "{}2".format(self.PATCH_STR_VALUE),
                    },
                ],
                "params": {
                    "patch-key1": {"value": "{}2".format(self.PATCH_STR_VALUE)},
                    "patch-key2": {"value": "{}1".format(self.PATCH_STR_VALUE)},
                },
                "runPatch": {
                    "init": [
                        {"connection": self.PATCH_STR_VALUE, "git": {"revision": "dev"}}
                    ],
                    "connections": [
                        "{}1".format(self.PATCH_STR_VALUE),
                        "{}2".format(self.PATCH_STR_VALUE),
                    ],
                    "container": {
                        "resources": {
                            "requests": {
                                "cpu": self.PATCH_INT_VALUE,
                                "memory": self.PATCH_INT_VALUE,
                            }
                        }
                    },
                    "environment": {
                        "nodeSelector": {"polyaxon-patch": "core"},
                        "serviceAccountName": self.PATCH_STR_VALUE,
                        "imagePullSecrets": [
                            "{}1".format(self.PATCH_STR_VALUE),
                            "{}2".format(self.PATCH_STR_VALUE),
                        ],
                    },
                },
                "schedule": {"kind": "datetime", "startAt": self.PATCH_DT_VALUE},
                "events": None,
                "matrix": {
                    "concurrency": self.PATCH_INT_VALUE,
                    "kind": "mapping",
                    "values": [
                        {"a": self.PATCH_INT_VALUE},
                        {"c": self.PATCH_INT_VALUE},
                    ],
                },
                "dependencies": [
                    "{}1".format(self.PATCH_STR_VALUE),
                    "{}2".format(self.PATCH_STR_VALUE),
                ],
                "trigger": "all_succeeded",
                "conditions": "",
                "skipOnUpstreamSkip": True,
            }
        )

    def get_empty_preset(self):
        return OperationSpecification.read(
            {
                "version": pkg.SCHEMA_VERSION,
                "name": None,
                "isPreset": True,
                "description": "",
                "tags": [],
                "presets": [],
                "queue": "",
                "cache": {},
                "termination": {},
                "plugins": {},
                "actions": [],
                "hooks": [],
                "params": {},
                "runPatch": {
                    "init": [],
                    "connections": [],
                    "container": {},
                    "environment": {
                        "nodeSelector": {},
                        "serviceAccountName": "",
                        "imagePullSecrets": [],
                    },
                },
                "schedule": None,
                "events": None,
                "matrix": None,
                "dependencies": [],
                "trigger": None,
                "conditions": None,
                "skipOnUpstreamSkip": None,
            }
        )

    def test_patch_replace_empty_values_with_empty_preset(self):
        operation = self.get_empty_operation()
        tmp_operation = self.get_empty_operation()
        result = tmp_operation.patch(
            V1Operation(is_preset=True), strategy=V1PatchStrategy.REPLACE
        )
        assert result.to_dict() == operation.to_dict()

        tmp_operation = self.get_empty_operation()
        preset = self.get_empty_preset()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.REPLACE)
        result_dict = result.to_dict()
        assert result_dict.pop("hubRef") == operation.hub_ref
        expected = preset.to_dict()
        expected.pop("isPreset")
        assert result_dict == expected

    def test_patch_replace_empty_values_with_full_preset(self):
        operation = self.get_empty_operation()
        tmp_operation = self.get_empty_operation()
        preset = self.get_full_preset()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.REPLACE)
        result_dict = result.to_dict()
        assert result_dict.pop("hubRef") == operation.hub_ref
        expected = preset.to_dict()
        expected.pop("isPreset")
        assert result_dict == expected

    def test_patch_replace_full_values_with_empty_preset(self):
        operation = self.get_full_operation()
        tmp_operation = self.get_full_operation()
        result = tmp_operation.patch(
            V1Operation(is_preset=True), strategy=V1PatchStrategy.REPLACE
        )
        assert result.to_dict() == operation.to_dict()

        tmp_operation = self.get_full_operation()
        preset = self.get_empty_preset()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.REPLACE)
        result_dict = result.to_dict()
        assert result_dict.pop("hubRef") == operation.hub_ref
        assert result_dict.pop("name") == operation.name
        assert result_dict.pop("trigger") == operation.trigger
        assert result_dict.pop("conditions") == operation.conditions
        assert result_dict.pop("skipOnUpstreamSkip") == operation.skip_on_upstream_skip
        assert result_dict.pop("schedule") == operation.schedule.to_dict()
        assert result_dict.pop("matrix") == operation.matrix.to_dict()
        assert result_dict.pop("cache") == operation.cache.to_dict()
        assert result_dict.pop("plugins") == operation.plugins.to_dict()
        assert result_dict.pop("termination") == operation.termination.to_dict()
        expected = preset.to_dict()
        expected.pop("isPreset")
        expected.pop("cache")
        expected.pop("plugins")
        expected.pop("termination")
        assert result_dict == expected

    def test_patch_replace_full_values_with_full_preset(self):
        operation = self.get_full_operation()
        tmp_operation = self.get_full_operation()
        preset = self.get_full_preset()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.REPLACE)
        result_dict = result.to_dict()
        assert result_dict.pop("hubRef") == operation.hub_ref
        expected = preset.to_dict()
        expected.pop("isPreset")
        assert result_dict == expected

    def test_patch_isnull_empty_values_with_empty_preset(self):
        operation = self.get_empty_operation()
        tmp_operation = self.get_empty_operation()
        result = tmp_operation.patch(
            V1Operation(is_preset=True), strategy=V1PatchStrategy.ISNULL
        )
        assert result.to_dict() == operation.to_dict()

        tmp_operation = self.get_empty_operation()
        preset = self.get_empty_preset()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.ISNULL)
        result_dict = result.to_dict()
        assert result_dict.pop("hubRef") == operation.hub_ref
        expected = preset.to_dict()
        expected.pop("isPreset")
        assert result_dict == expected

    def test_patch_isnull_empty_values_with_full_preset(self):
        operation = self.get_empty_operation()
        tmp_operation = self.get_empty_operation()
        result = tmp_operation.patch(
            V1Operation(is_preset=True), strategy=V1PatchStrategy.ISNULL
        )
        assert result.to_dict() == operation.to_dict()

        tmp_operation = self.get_empty_operation()
        preset = self.get_empty_preset()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.ISNULL)
        result_dict = result.to_dict()
        assert result_dict.pop("hubRef") == operation.hub_ref
        expected = preset.to_dict()
        expected.pop("isPreset")
        assert result_dict == expected

    def test_patch_isnull_full_values_with_empty_preset(self):
        operation = self.get_full_operation()
        tmp_operation = self.get_full_operation()
        result = tmp_operation.patch(
            V1Operation(is_preset=True), strategy=V1PatchStrategy.ISNULL
        )
        assert result.to_dict() == operation.to_dict()

        tmp_operation = self.get_full_operation()
        preset = self.get_empty_preset()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.ISNULL)
        assert result.to_dict() == operation.to_dict()

    def test_patch_isnull_full_values_with_full_preset(self):
        operation = self.get_full_operation()
        tmp_operation = self.get_full_operation()
        preset = self.get_full_preset()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.ISNULL)
        assert result.to_dict() == operation.to_dict()

    def test_patch_post_merge_empty_values_with_empty_preset(self):
        operation = self.get_empty_operation()
        tmp_operation = self.get_empty_operation()
        result = tmp_operation.patch(
            V1Operation(is_preset=True), strategy=V1PatchStrategy.POST_MERGE
        )
        assert result.to_dict() == operation.to_dict()

        tmp_operation = self.get_empty_operation()
        preset = self.get_empty_preset()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.POST_MERGE)
        result_dict = result.to_dict()
        assert result_dict.pop("hubRef") == operation.hub_ref
        expected = preset.to_dict()
        expected.pop("isPreset")
        assert result_dict == expected

    def test_patch_post_merge_empty_values_with_full_preset(self):
        operation = self.get_empty_operation()
        tmp_operation = self.get_empty_operation()
        preset = self.get_full_preset()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.POST_MERGE)
        result_dict = result.to_dict()
        assert result_dict.pop("hubRef") == operation.hub_ref
        expected = preset.to_dict()
        expected.pop("isPreset")
        assert result_dict == expected

    def test_patch_post_merge_full_values_with_empty_preset(self):
        operation = self.get_full_operation()
        tmp_operation = self.get_full_operation()
        result = tmp_operation.patch(
            V1Operation(is_preset=True), strategy=V1PatchStrategy.POST_MERGE
        )
        assert result.to_dict() == operation.to_dict()

        tmp_operation = self.get_full_operation()
        preset = self.get_empty_preset()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.POST_MERGE)
        result_dict = result.to_dict()
        assert result_dict["description"] == ""
        result_dict["description"] = self.DEFAULT_STR_VALUE
        assert result_dict["queue"] == ""
        result_dict["queue"] = "{}/{}".format(
            self.DEFAULT_STR_VALUE, self.DEFAULT_STR_VALUE
        )
        result_dict["presets"] = [self.DEFAULT_STR_VALUE]
        # Since there's no component to validate the runPatch section it stays the same
        assert result_dict == operation.to_dict()

        operation = self.get_full_operation_with_component()
        tmp_operation = self.get_full_operation_with_component()
        preset = self.get_empty_preset()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.POST_MERGE)
        result_dict = result.to_dict()
        assert result_dict["description"] == ""
        result_dict["description"] = self.DEFAULT_STR_VALUE
        assert result_dict["queue"] == ""
        result_dict["queue"] = "{}/{}".format(
            self.DEFAULT_STR_VALUE, self.DEFAULT_STR_VALUE
        )
        # Run patch was validated and merged
        assert result_dict["runPatch"]["environment"]["serviceAccountName"] == ""
        result_dict["runPatch"]["environment"][
            "serviceAccountName"
        ] = operation.run_patch["environment"]["serviceAccountName"]
        assert result_dict["runPatch"]["container"].pop("name") == MAIN_JOB_CONTAINER
        assert result_dict == operation.to_dict()

    def test_patch_post_merge_full_values_with_full_preset(self):
        operation = self.get_full_operation()
        tmp_operation = self.get_full_operation()
        preset = self.get_full_preset()
        expected = preset.to_dict()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.POST_MERGE)
        result_dict = result.to_dict()
        expected.pop("isPreset")
        expected["tags"] = operation.tags + expected["tags"]
        expected["presets"] = operation.presets + expected["presets"]
        expected["actions"] = [i.to_dict() for i in operation.actions] + expected[
            "actions"
        ]
        expected["hooks"] = [i.to_dict() for i in operation.hooks] + expected["hooks"]
        expected["dependencies"] = operation.dependencies + expected["dependencies"]
        expected["matrix"]["values"] = (
            operation.matrix.values + expected["matrix"]["values"]
        )
        # Since there's no component to validate the runPatch section it stays the same
        expected["runPatch"] = operation.run_patch
        assert result_dict.pop("hubRef") == operation.hub_ref
        assert result_dict == expected

        operation = self.get_full_operation_with_component()
        tmp_operation = self.get_full_operation_with_component()
        preset = self.get_full_preset()
        expected = preset.to_dict()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.POST_MERGE)
        result_dict = result.to_dict()
        expected.pop("isPreset")
        expected["tags"] = operation.tags + expected["tags"]
        expected["presets"] = operation.presets + expected["presets"]
        expected["actions"] = [i.to_dict() for i in operation.actions] + expected[
            "actions"
        ]
        expected["hooks"] = [i.to_dict() for i in operation.hooks] + expected["hooks"]
        expected["dependencies"] = operation.dependencies + expected["dependencies"]
        expected["matrix"]["values"] = (
            operation.matrix.values + expected["matrix"]["values"]
        )
        # Run patch was validated and merged
        assert result_dict["runPatch"]["container"].pop("name") == MAIN_JOB_CONTAINER
        assert (
            result_dict["runPatch"]["connections"]
            == operation.run_patch["connections"] + expected["runPatch"]["connections"]
        )
        result_dict["runPatch"]["connections"] = expected["runPatch"]["connections"]
        assert (
            result_dict["runPatch"]["init"]
            == operation.run_patch["init"] + expected["runPatch"]["init"]
        )
        result_dict["runPatch"]["init"] = expected["runPatch"]["init"]
        assert (
            result_dict["runPatch"]["environment"]["imagePullSecrets"]
            == operation.run_patch["environment"]["imagePullSecrets"]
            + expected["runPatch"]["environment"]["imagePullSecrets"]
        )
        result_dict["runPatch"]["environment"]["imagePullSecrets"] = expected[
            "runPatch"
        ]["environment"]["imagePullSecrets"]

        assert result_dict["runPatch"]["environment"]["nodeSelector"] == {
            **operation.run_patch["environment"]["nodeSelector"],
            **expected["runPatch"]["environment"]["nodeSelector"],
        }
        result_dict["runPatch"]["environment"]["nodeSelector"] = expected["runPatch"][
            "environment"
        ]["nodeSelector"]

        assert result_dict.pop("hubRef") == operation.hub_ref
        assert result_dict.pop("component") == operation.component.to_dict()
        expected["runPatch"]["container"].pop("name")
        assert result_dict == expected

    def test_patch_pre_merge_empty_values_with_empty_preset(self):
        operation = self.get_empty_operation()
        tmp_operation = self.get_empty_operation()
        result = tmp_operation.patch(
            V1Operation(is_preset=True), strategy=V1PatchStrategy.PRE_MERGE
        )
        assert result.to_dict() == operation.to_dict()

        tmp_operation = self.get_empty_operation()
        preset = self.get_empty_preset()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.PRE_MERGE)
        result_dict = result.to_dict()
        assert result_dict.pop("hubRef") == operation.hub_ref
        expected = preset.to_dict()
        expected.pop("isPreset")
        assert result_dict == expected

    def test_patch_pre_merge_empty_values_with_full_preset(self):
        operation = self.get_empty_operation()
        tmp_operation = self.get_empty_operation()
        preset = self.get_full_preset()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.PRE_MERGE)
        result_dict = result.to_dict()
        assert result_dict.pop("hubRef") == operation.hub_ref
        expected = preset.to_dict()
        expected.pop("isPreset")
        assert result_dict == expected

    def test_patch_pre_merge_full_values_with_empty_preset(self):
        operation = self.get_full_operation()
        tmp_operation = self.get_full_operation()
        result = tmp_operation.patch(
            V1Operation(is_preset=True), strategy=V1PatchStrategy.PRE_MERGE
        )
        assert result.to_dict() == operation.to_dict()

        tmp_operation = self.get_full_operation()
        preset = self.get_empty_preset()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.PRE_MERGE)
        result_dict = result.to_dict()
        # Since there's no component to validate the runPatch section it stays the same
        assert result_dict == operation.to_dict()

        operation = self.get_full_operation_with_component()
        tmp_operation = self.get_full_operation_with_component()
        preset = self.get_empty_preset()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.PRE_MERGE)
        result_dict = result.to_dict()
        assert result_dict["runPatch"]["container"].pop("name") == MAIN_JOB_CONTAINER
        # Run patch was validated and merged
        assert result_dict == operation.to_dict()

    def test_patch_pre_merge_full_values_with_full_preset(self):
        operation = self.get_full_operation()
        tmp_operation = self.get_full_operation()
        preset = self.get_full_preset()
        preset_dict = preset.to_dict()
        expected = operation.to_dict()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.PRE_MERGE)
        result_dict = result.to_dict()
        expected["tags"] = preset_dict["tags"] + operation.tags
        expected["presets"] = preset_dict["presets"] + operation.presets
        expected["actions"] = preset_dict["actions"] + [
            i.to_dict() for i in operation.actions
        ]
        expected["hooks"] = preset_dict["hooks"] + [
            i.to_dict() for i in operation.hooks
        ]
        expected["dependencies"] = preset_dict["dependencies"] + operation.dependencies
        expected["matrix"]["values"] = (
            preset_dict["matrix"]["values"] + operation.matrix.values
        )
        assert result_dict == expected

        operation = self.get_full_operation_with_component()
        tmp_operation = self.get_full_operation_with_component()
        preset = self.get_full_preset()
        preset_dict = preset.to_dict()
        expected = operation.to_dict()
        result = tmp_operation.patch(preset, strategy=V1PatchStrategy.PRE_MERGE)
        result_dict = result.to_dict()
        expected["tags"] = preset_dict["tags"] + operation.tags
        expected["presets"] = preset_dict["presets"] + operation.presets
        expected["actions"] = preset_dict["actions"] + [
            i.to_dict() for i in operation.actions
        ]
        expected["hooks"] = preset_dict["hooks"] + [
            i.to_dict() for i in operation.hooks
        ]
        expected["dependencies"] = preset_dict["dependencies"] + operation.dependencies
        expected["matrix"]["values"] = (
            preset_dict["matrix"]["values"] + operation.matrix.values
        )
        # Run patch was validated and merged
        assert result_dict["runPatch"]["container"].pop("name") == MAIN_JOB_CONTAINER
        assert result_dict["runPatch"]["container"].pop("resources") == deep_update(
            preset_dict["runPatch"]["container"]["resources"],
            expected["runPatch"]["container"]["resources"],
        )
        result_dict["runPatch"]["container"]["resources"] = expected["runPatch"][
            "container"
        ]["resources"]
        assert (
            result_dict["runPatch"]["connections"]
            == preset_dict["runPatch"]["connections"]
            + expected["runPatch"]["connections"]
        )
        result_dict["runPatch"]["connections"] = expected["runPatch"]["connections"]
        assert (
            result_dict["runPatch"]["init"]
            == preset_dict["runPatch"]["init"] + expected["runPatch"]["init"]
        )
        result_dict["runPatch"]["init"] = expected["runPatch"]["init"]
        assert (
            result_dict["runPatch"]["environment"]["imagePullSecrets"]
            == preset_dict["runPatch"]["environment"]["imagePullSecrets"]
            + expected["runPatch"]["environment"]["imagePullSecrets"]
        )
        result_dict["runPatch"]["environment"]["imagePullSecrets"] = expected[
            "runPatch"
        ]["environment"]["imagePullSecrets"]

        assert result_dict["runPatch"]["environment"]["nodeSelector"] == {
            **preset_dict["runPatch"]["environment"]["nodeSelector"],
            **expected["runPatch"]["environment"]["nodeSelector"],
        }
        result_dict["runPatch"]["environment"]["nodeSelector"] = expected["runPatch"][
            "environment"
        ]["nodeSelector"]

        assert result_dict == expected


class BaseTestApplyPreset(BaseTestCase):
    def setUp(self):
        super().setUp()
        op_spec = OperationSpecification.read(
            {
                "version": 1.1,
                "kind": "operation",
                "name": "foo",
                "description": "a description",
                "tags": ["tag1", "tag2"],
                "trigger": "all_succeeded",
                "component": {
                    "name": "build-template",
                    "tags": ["tag1", "tag2"],
                    "run": {
                        "kind": V1RunKind.JOB,
                        "container": {"image": "test"},
                        "init": [{"connection": "foo", "git": {"revision": "dev"}}],
                    },
                },
            }
        )
        self.compiled_operation = OperationSpecification.compile_operation(op_spec)
        self.preset = {"runPatch": {}, "patchStrategy": V1PatchStrategy.POST_MERGE}


@pytest.mark.polyaxonfile_mark
class TestApplyPresetEnvironment(BaseTestApplyPreset):
    def assert_environment(self, environment1, environment2):
        self.preset["runPatch"]["environment"] = environment1
        assert self.compiled_operation.run.environment is None
        assert (
            OperationSpecification.apply_preset(
                config=self.compiled_operation,
                preset=self.preset,
            )
            == self.compiled_operation
        )
        assert self.compiled_operation.run.environment is not None
        env = self.compiled_operation.run.environment.to_dict()
        assert env == environment1

        # Updating the preset
        self.preset["patchStrategy"] = V1PatchStrategy.REPLACE
        self.preset["runPatch"]["environment"] = environment2
        assert (
            OperationSpecification.apply_preset(
                config=self.compiled_operation,
                preset=self.preset,
            )
            == self.compiled_operation
        )
        assert self.compiled_operation.run.environment is not None
        env = self.compiled_operation.run.environment.to_dict()
        assert env == environment2

    def test_compile_injects_labels(self):
        environment1 = {"labels": {"label1": "value1"}}
        environment2 = {"labels": {"label1": "value11"}}
        self.assert_environment(environment1, environment2)

        # Updating the preset
        environment3 = {"labels": {"label2": "value2"}}
        self.preset["runPatch"]["environment"] = environment3
        env = self.compiled_operation.run.environment.to_dict()
        assert env == environment2
        assert (
            OperationSpecification.apply_preset(
                config=self.compiled_operation,
                preset=self.preset,
            )
            == self.compiled_operation
        )
        assert self.compiled_operation.run.environment is not None
        env = self.compiled_operation.run.environment.to_dict()
        assert env == {"labels": {"label2": "value2"}}

    def test_compile_injects_annotations(self):
        environment1 = {"annotations": {"anno1": "value1"}}
        environment2 = {"annotations": {"anno1": "value11"}}
        self.assert_environment(environment1, environment2)

        # Updating the preset
        environment3 = {"annotations": {"anno2": "value2"}}
        self.preset["runPatch"]["environment"] = environment3
        assert (
            OperationSpecification.apply_preset(
                config=self.compiled_operation,
                preset=self.preset,
            )
            == self.compiled_operation
        )
        assert self.compiled_operation.run.environment is not None
        env = self.compiled_operation.run.environment.to_dict()
        assert env == {"annotations": {"anno2": "value2"}}

    def test_compile_injects_node_selector(self):
        environment1 = {"nodeSelector": {"plx": "selector1"}}
        environment2 = {"nodeSelector": {"plx": "selector2"}}
        self.assert_environment(environment1, environment2)

    def test_compile_injects_affinity(self):
        environment1 = {"affinity": {"podAffinity": {}}}
        environment2 = {"affinity": {"podAffinity": {"foo": "bar"}}}
        self.assert_environment(environment1, environment2)

    def test_compile_injects_tolerations(self):
        environment1 = {"tolerations": [{"key": "key1", "operator": "Exists"}]}
        environment2 = {"tolerations": [{"key": "key2", "operator": "NotExists"}]}
        self.assert_environment(environment1, environment2)

    def test_compile_injects_service_account_name(self):
        environment1 = {"serviceAccountName": "sa1"}
        environment2 = {"serviceAccountName": "sa2"}
        self.assert_environment(environment1, environment2)

    def test_compile_injects_image_pull_secrets(self):
        environment1 = {"imagePullSecrets": ["ps1", "ps2"]}
        environment2 = {"imagePullSecrets": ["ps3"]}
        self.assert_environment(environment1, environment2)

    def test_compile_injects_security_context(self):
        environment1 = {"securityContext": {"runAsUser": 1000, "runAsGroup": 3000}}
        environment2 = {"securityContext": {"runAsUser": 100, "runAsGroup": 300}}
        self.assert_environment(environment1, environment2)


@pytest.mark.polyaxonfile_mark
class TestApplyPresetPlugins(BaseTestApplyPreset):
    def assert_plugins(self, plugins1, plugins2):
        self.preset["plugins"] = plugins1
        assert self.compiled_operation.plugins is None
        assert (
            OperationSpecification.apply_preset(
                config=self.compiled_operation,
                preset=self.preset,
            )
            == self.compiled_operation
        )
        assert self.compiled_operation.plugins is not None
        env = self.compiled_operation.plugins.to_dict()
        assert env == plugins1

        # Updating the preset
        self.preset["plugins"] = plugins2
        plugins = self.compiled_operation.plugins.to_dict()
        assert plugins == plugins1
        assert (
            OperationSpecification.apply_preset(
                config=self.compiled_operation,
                preset=self.preset,
            )
            == self.compiled_operation
        )
        assert self.compiled_operation.plugins is not None
        plugins = self.compiled_operation.plugins.to_dict()
        assert plugins == plugins2

    def test_compile_injects_log_level(self):
        plugins = {"logLevel": "DEBUG"}
        plugins2 = {"logLevel": "INFO"}
        self.assert_plugins(plugins, plugins2)

    def test_compile_injects_auth(self):
        plugins = {"auth": True}
        plugins2 = {"auth": False}
        self.assert_plugins(plugins, plugins2)

    def test_compile_injects_docker(self):
        plugins = {"docker": True}
        plugins2 = {"docker": False}
        self.assert_plugins(plugins, plugins2)

    def test_compile_injects_shm(self):
        plugins = {"shm": True}
        plugins2 = {"shm": False}
        self.assert_plugins(plugins, plugins2)


@pytest.mark.polyaxonfile_mark
class TestApplyPresetTermination(BaseTestApplyPreset):
    def assert_termination(self, termination1, termination2):
        self.preset["termination"] = termination1
        assert self.compiled_operation.termination is None
        assert (
            OperationSpecification.apply_preset(
                config=self.compiled_operation,
                preset=self.preset,
            )
            == self.compiled_operation
        )
        assert self.compiled_operation.termination is not None
        assert self.compiled_operation.termination.to_dict() == termination1

        # Updating the preset
        self.preset["termination"] = termination2
        assert self.compiled_operation.termination.to_dict() == termination1
        assert (
            OperationSpecification.apply_preset(
                config=self.compiled_operation,
                preset=self.preset,
            )
            == self.compiled_operation
        )
        assert self.compiled_operation.termination is not None
        assert self.compiled_operation.termination.to_dict() == termination2

    def test_compile_injects_max_retries(self):
        termination1 = {"maxRetries": 10}
        termination2 = {"maxRetries": 1}
        self.assert_termination(termination1, termination2)

    def test_compile_injects_timeout(self):
        termination1 = {"timeout": 10}
        termination2 = {"timeout": 1}
        self.assert_termination(termination1, termination2)

    def test_compile_injects_ttl(self):
        termination1 = {"ttl": 10}
        termination2 = {"ttl": 1}
        self.assert_termination(termination1, termination2)


@pytest.mark.polyaxonfile_mark
class TestApplyPreset(BaseTestApplyPreset):
    def test_patch_does_not_alter_with_no_preset(self):
        assert (
            OperationSpecification.apply_preset(
                config=self.compiled_operation,
                preset=None,
            )
            == self.compiled_operation
        )

    def test_patch_does_not_alter_with_preset_with_no_environment_or_contexts_or_termination(
        self,
    ):
        assert (
            OperationSpecification.apply_preset(
                config=self.compiled_operation,
                preset=self.preset,
            )
            == self.compiled_operation
        )

    def test_patch_environment_and_termination(self):
        termination1 = {"maxRetries": 1, "timeout": 1, "ttl": 1}
        environment1 = {
            "labels": {"label1": "value1"},
            "annotations": {"anno1": "value1"},
            "nodeSelector": {"plx": "selector1"},
            "affinity": {"podAffinity": {}},
            "tolerations": [{"key": "key1", "operator": "Exists"}],
            "serviceAccountName": "sa1",
            "imagePullSecrets": ["ps1", "ps2"],
            "securityContext": {"runAsUser": 1000, "runAsGroup": 3000},
        }
        plugins1 = {
            "logLevel": "DEBUG",
            "auth": True,
            "docker": True,
            "shm": True,
        }

        self.preset["termination"] = termination1
        self.preset["runPatch"]["environment"] = environment1
        self.preset["plugins"] = plugins1
        assert self.compiled_operation.termination is None
        assert (
            OperationSpecification.apply_preset(
                config=self.compiled_operation,
                preset=self.preset,
            )
            == self.compiled_operation
        )
        assert self.compiled_operation.termination is not None
        assert self.compiled_operation.termination.to_dict() == termination1
        assert self.compiled_operation.run.environment is not None
        env = self.compiled_operation.run.environment.to_dict()
        assert env == environment1
        assert self.compiled_operation.plugins is not None
        assert self.compiled_operation.plugins.to_dict() == plugins1

        termination2 = {"maxRetries": 10, "timeout": 10, "ttl": 10}
        environment2 = {
            "labels": {"label1": "value12"},
            "annotations": {"anno1": "value12"},
            "nodeSelector": {"plx": "selector12"},
            "affinity": {"podAffinity": {"k": "v"}},
            "tolerations": [{"key": "key11", "operator": "NotExists"}],
            "serviceAccountName": "sa2",
            "imagePullSecrets": ["ps2", "ps22"],
            "securityContext": {"runAsUser": 100, "runAsGroup": 300},
        }
        plugins2 = {
            "logLevel": "INFO",
            "auth": False,
            "docker": False,
            "shm": False,
        }

        # Updating the preset
        self.preset["termination"] = termination2
        self.preset["runPatch"]["environment"] = environment2
        self.preset["plugins"] = plugins2
        self.preset["patchStrategy"] = V1PatchStrategy.REPLACE

        assert (
            OperationSpecification.apply_preset(
                config=self.compiled_operation,
                preset=self.preset,
            )
            == self.compiled_operation
        )
        assert self.compiled_operation.termination is not None
        assert self.compiled_operation.termination.to_dict() == termination2
        assert self.compiled_operation.termination is not None
        env = self.compiled_operation.run.environment.to_dict()
        assert env == environment2
        assert self.compiled_operation.plugins is not None
        assert self.compiled_operation.plugins.to_dict() == plugins2

        termination3 = {"maxRetries": 15}
        environment3 = {
            "labels": {},
            "annotations": {},
            "nodeSelector": {},
            "affinity": {"podAffinity": {"k": "v"}},
            "tolerations": [],
            "securityContext": {"runAsUser": 10, "runAsGroup": 30},
            "serviceAccountName": "sa2",
            "imagePullSecrets": ["ps2", "ps22"],
        }

        # Updating the preset
        self.preset["termination"] = termination3
        self.preset["runPatch"]["environment"] = environment3
        self.preset["patchStrategy"] = V1PatchStrategy.REPLACE
        assert (
            OperationSpecification.apply_preset(
                config=self.compiled_operation,
                preset=self.preset,
            )
            == self.compiled_operation
        )
        assert self.compiled_operation.termination is not None
        assert self.compiled_operation.termination.to_dict() == {
            "maxRetries": 15,
            "timeout": 10,
            "ttl": 10,
        }
        assert self.compiled_operation.termination is not None
        env = self.compiled_operation.run.environment.to_dict()
        assert env == environment3
        assert self.compiled_operation.plugins is not None
        assert self.compiled_operation.plugins.to_dict() == plugins2
