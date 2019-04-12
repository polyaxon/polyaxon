# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from polyaxon_deploy.operators.helm import HelmOperator
from polyaxon_deploy.operators.kubectl import KubectlOperator
from polyaxon_deploy.schemas.deployment import DeploymentConfig, DeploymentTypes

from polyaxon_cli.managers.deploy import DeployManager


class TestDeployManager(TestCase):
    def test_default_props(self):
        manager = DeployManager()
        assert manager.deployment_type == DeploymentTypes.KUBERNETES
        assert manager.is_kubernetes is True
        assert isinstance(manager.helm, HelmOperator)
        assert isinstance(manager.kubectl, KubectlOperator)

    def test_deployment_type(self):
        manager = DeployManager(
            config=DeploymentConfig.from_dict({'deploymentType': DeploymentTypes.DOCKER_COMPOSE}))
        assert manager.deployment_type == DeploymentTypes.DOCKER_COMPOSE
        assert manager.is_docker_compose is True

        manager = DeployManager(
            config=DeploymentConfig.from_dict({'deploymentType': DeploymentTypes.KUBERNETES}))
        assert manager.deployment_type == DeploymentTypes.KUBERNETES
        assert manager.is_kubernetes is True

        manager = DeployManager(
            config=DeploymentConfig.from_dict({'deploymentType': DeploymentTypes.HEROKU}))
        assert manager.deployment_type == DeploymentTypes.HEROKU
        assert manager.is_heroku is True

        manager = DeployManager(
            config=DeploymentConfig.from_dict({'deploymentType': DeploymentTypes.DOCKER}))
        assert manager.deployment_type == DeploymentTypes.DOCKER
        assert manager.is_docker is True
