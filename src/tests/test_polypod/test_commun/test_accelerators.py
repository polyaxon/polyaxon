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
from polyaxon.polypod.common.accelerators import (
    has_tpu_annotation,
    requests_gpu,
    requests_tpu,
)
from tests.utils import BaseTestCase


@pytest.mark.polypod_mark
class TestTPUs(BaseTestCase):
    def test_has_tpu_annotation(self):
        assert has_tpu_annotation(None) is False
        assert has_tpu_annotation({}) is False
        assert has_tpu_annotation({"foo": "bar"}) is False
        assert has_tpu_annotation({"tf-version.cloud-tpus.google.com": "1.13"}) is True

    def test_requests_tpu(self):
        assert (
            requests_tpu(k8s_schemas.V1ResourceRequirements(limits={"cpu": 1})) is False
        )
        assert (
            requests_tpu(
                k8s_schemas.V1ResourceRequirements(
                    limits={"cloud-tpus.google.com/v2": 1}
                )
            )
            is True
        )
        assert (
            requests_tpu(
                k8s_schemas.V1ResourceRequirements(
                    requests={"cloud-tpus.google.com/v2:": 32}
                )
            )
            is True
        )

    def test_requests_gpu(self):
        assert (
            requests_gpu(k8s_schemas.V1ResourceRequirements(limits={"cpu": 1})) is False
        )
        assert (
            requests_gpu(k8s_schemas.V1ResourceRequirements(limits={"amd.com/gpu": 1}))
            is True
        )
        assert (
            requests_gpu(
                k8s_schemas.V1ResourceRequirements(requests={"nvidia.com/gpu": 1})
            )
            is True
        )
