#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon.deploy.operators.helm import HelmOperator
from polyaxon.deploy.operators.kubectl import KubectlOperator
from polyaxon.deploy.schemas.deployment import DeploymentConfig, DeploymentTypes
from polyaxon.managers.deploy import DeployManager


class TestDeployManager(TestCase):
    def test_default_props(self):
        manager = DeployManager()
        assert manager.deployment_type == DeploymentTypes.KUBERNETES
        assert manager.is_kubernetes is True
        assert isinstance(manager.helm, HelmOperator)
        assert isinstance(manager.kubectl, KubectlOperator)

    def test_deployment_type(self):
        manager = DeployManager(
            config=DeploymentConfig.from_dict(
                {"deploymentType": DeploymentTypes.DOCKER_COMPOSE}
            )
        )
        assert manager.deployment_type == DeploymentTypes.DOCKER_COMPOSE
        assert manager.is_docker_compose is True

        manager = DeployManager(
            config=DeploymentConfig.from_dict(
                {"deploymentType": DeploymentTypes.KUBERNETES}
            )
        )
        assert manager.deployment_type == DeploymentTypes.KUBERNETES
        assert manager.is_kubernetes is True

        manager = DeployManager(
            config=DeploymentConfig.from_dict(
                {"deploymentType": DeploymentTypes.HEROKU}
            )
        )
        assert manager.deployment_type == DeploymentTypes.HEROKU
        assert manager.is_heroku is True

        manager = DeployManager(
            config=DeploymentConfig.from_dict(
                {"deploymentType": DeploymentTypes.DOCKER}
            )
        )
        assert manager.deployment_type == DeploymentTypes.DOCKER
        assert manager.is_docker is True
