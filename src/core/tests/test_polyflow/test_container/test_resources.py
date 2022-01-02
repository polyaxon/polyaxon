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
# limitations under the License.

import pytest

from polyaxon.k8s import k8s_schemas
from polyaxon.polyflow.run.resources import V1RunResources
from tests.utils import BaseTestCase


@pytest.mark.container_mark
class TestRunResources(BaseTestCase):
    def test_get_resource_from_empty_container(self):
        expected = V1RunResources(memory=0, cpu=0, gpu=0, custom=0, cost=0)
        assert V1RunResources.from_container(None) == expected
        assert V1RunResources.from_container(k8s_schemas.V1Container()) == expected
        assert (
            V1RunResources.from_container(
                k8s_schemas.V1Container(resources={"requests": {"cpu": 0, "tpu": 0}})
            )
            == expected
        )

    def test_from_container_dict(self):
        expected = V1RunResources(memory=0, cpu=0, gpu=0, custom=0, cost=0)

        container = k8s_schemas.V1Container(
            resources={"requests": {"cpu": 0, "tpu": 0}}
        )
        assert V1RunResources.from_container(container) == expected

        container = k8s_schemas.V1Container(
            resources={
                "requests": {"cpu": 0.1, "tpu": 1},
                "limits": {"cpu": 1, "tpu": 1},
            }
        )
        expected.cpu = 0.1
        expected.custom = 1
        assert V1RunResources.from_container(container) == expected

        container = k8s_schemas.V1Container(
            resources={
                "requests": {"memory": "64Mi", "cpu": "250m"},
                "limits": {
                    "memory": "128Mi",
                    "cpu": "500m",
                    "cloud-tpus.google.com/v2": 8,
                    "nvidia.com/gpu": 2,
                },
            }
        )
        expected.memory = 64 * (1024 ** 2)
        expected.cpu = 0.25
        expected.gpu = 2
        expected.custom = 8
        assert V1RunResources.from_container(container) == expected

    def test_from_container_obj(self):
        expected = V1RunResources(memory=0, cpu=0, gpu=0, custom=0, cost=0)

        container = k8s_schemas.V1Container(
            resources=k8s_schemas.V1ResourceRequirements(requests={"cpu": 0, "tpu": 0})
        )
        assert V1RunResources.from_container(container) == expected

        container = k8s_schemas.V1Container(
            resources=k8s_schemas.V1ResourceRequirements(
                requests={"cpu": 0.1, "tpu": 1}, limits={"cpu": 1, "tpu": 1}
            )
        )
        expected.cpu = 0.1
        expected.custom = 1
        assert V1RunResources.from_container(container) == expected

        container = k8s_schemas.V1Container(
            resources=k8s_schemas.V1ResourceRequirements(
                requests={"memory": "64Mi", "cpu": "250m"},
                limits={
                    "memory": "128Mi",
                    "cpu": "500m",
                    "cloud-tpus.google.com/v2": 8,
                    "nvidia.com/gpu": 2,
                },
            ),
        )
        expected.memory = 64 * (1024 ** 2)
        expected.cpu = 0.25
        expected.gpu = 2
        expected.custom = 8
        assert V1RunResources.from_container(container) == expected

    def test_from_container_obj_multi_representation(self):
        expected = V1RunResources(
            memory=64 * (1024 ** 2), cpu=0.25, gpu=2, custom=8, cost=0
        )
        container = k8s_schemas.V1Container(
            resources=k8s_schemas.V1ResourceRequirements(
                requests={"memory": "64Mi", "cpu": "0.25"},
                limits={
                    "memory": "128Mi",
                    "cpu": "500m",
                    "cloud-tpus.google.com/v2": 8,
                    "nvidia.com/gpu": 2,
                },
            ),
        )
        assert V1RunResources.from_container(container) == expected

        expected = V1RunResources(memory=128974848, cpu=0.25, gpu=2, custom=8, cost=0)
        container = k8s_schemas.V1Container(
            resources=k8s_schemas.V1ResourceRequirements(
                requests={"memory": "128974848", "cpu": "250m"},
                limits={
                    "memory": "128Mi",
                    "cpu": "500m",
                    "cloud-tpus.google.com/preemptible-v2": 8,
                    "amd.com/gpu": 2,
                },
            ),
        )
        assert V1RunResources.from_container(container) == expected

        expected = V1RunResources(memory=129e6, cpu=0.00025, gpu=2, custom=8, cost=0)
        container = k8s_schemas.V1Container(
            resources=k8s_schemas.V1ResourceRequirements(
                requests={"memory": "129e6", "cpu": "250u"},
                limits={
                    "memory": "128Mi",
                    "cpu": "500m",
                    "cloud-tpus.google.com/v3": 8,
                    "nvidia.com/gpu": 2,
                },
            ),
        )
        assert V1RunResources.from_container(container) == expected

        expected = V1RunResources(
            memory=129 * 1000 ** 2, cpu=0.00000025, gpu=2, custom=8, cost=0
        )
        container = k8s_schemas.V1Container(
            resources=k8s_schemas.V1ResourceRequirements(
                requests={"memory": "129M", "cpu": "250n"},
                limits={
                    "memory": "128Mi",
                    "cpu": "500m",
                    "cloud-tpus.google.com/preemptible-v3": 8,
                    "amd.com/gpu": 2,
                },
            ),
        )
        assert V1RunResources.from_container(container) == expected

    def test_add(self):
        c1 = V1RunResources(memory=0, cpu=0, gpu=0, custom=0, cost=0)
        c2 = V1RunResources(memory=0, cpu=0, gpu=0, custom=0, cost=0)
        assert c1 + c2 == c1

        c1.cpu = 1.1
        c1.gpu = 2

        c2.memory = 0.5
        c2.cost = 100
        c2.custom = 3

        assert c1 + c2 == V1RunResources(cpu=1.1, gpu=2, memory=0.5, cost=100, custom=3)
