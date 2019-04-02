# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError
from polyaxon_deploy import reader
from polyaxon_deploy.schemas.deployment import DeploymentConfig


class TestDeploymentConfig(TestCase):

    def test_read_deploy_config_values1(self):
        config = reader.read('tests/fixtures/values1.yml')
        assert isinstance(config, DeploymentConfig)
        assert config.deploymentType == 'docker-compose'
        assert config.namespace is None
        assert config.rbac.enabled is True
        assert config.adminViewEnabled is None
        assert config.timeZone is None
        assert config.environment == 'staging'
        assert config.ingress.enabled is True
        assert config.serviceType == 'ClusterIP'
        assert config.user.to_dict() == {'password': 'root'}
        assert config.nodeSelectors is None
        assert config.tolerations is None
        assert config.affinity is None
        assert config.limitResources is None
        assert config.globalReplicas is None
        assert config.globalConcurrency is None
        assert config.api is None
        assert config.streams is None
        assert config.scheduler is None
        assert config.hpsearch is None
        assert config.eventsHandlers is None
        assert config.k8sEventsHandlers is None
        assert config.beat is None
        assert config.crons is None
        assert config.eventMonitors is None
        assert config.resourcesDaemon is None
        assert config.sidecar is None
        assert config.dockerizer is None
        assert config.hooks is None
        assert config.postgresql.install is False
        assert config.rabbitmq is None
        assert config.dockerRegistry is None
        assert config.email is None
        assert config.integrations is None
        assert config.hostName is None
        assert config.allowedHosts is None
        assert config.secretRefs is None
        assert config.configmapRefs is None
        assert config.intervals is None
        assert config.cleaningIntervals is None
        assert config.ttl is None
        assert config.privateRegistries is None
        assert config.persistence is None

    def test_read_deploy_config_values2(self):
        config = reader.read('tests/fixtures/values2.yml')
        assert isinstance(config, DeploymentConfig)
        assert config.deploymentType is None
        assert config.namespace is None
        assert config.rbac.enabled is False
        assert config.adminViewEnabled is None
        assert config.timeZone is None
        assert config.environment == 'staging'
        assert config.ingress.enabled is False
        assert config.serviceType == 'NodePort'
        assert config.user.to_dict() == {'password': 'root'}
        assert config.nodeSelectors.to_dict() == {
            'core': {'polyaxon': 'core'},
            'builds': {'polyaxon': 'core'}
        }
        assert config.tolerations is None
        assert config.affinity is None
        assert config.limitResources is None
        assert config.globalReplicas is None
        assert config.globalConcurrency is None
        assert config.api.replicas == 3
        assert config.streams is None
        assert config.scheduler.replicas == 3
        assert config.hpsearch.replicas == 3
        assert config.eventsHandlers.replicas == 3
        assert config.k8sEventsHandlers.replicas == 3
        assert config.beat is None
        assert config.crons is None
        assert config.eventMonitors.replicas == 3
        assert config.resourcesDaemon is None
        assert config.sidecar is None
        assert config.dockerizer is None
        assert config.hooks is None
        assert config.postgresql.persistence is not None
        assert config.rabbitmq is None
        assert config.dockerRegistry is None
        assert config.email is not None
        assert len(config.integrations.slack) == 2
        assert len(config.integrations.to_dict()) == 1
        assert config.hostName is None
        assert config.allowedHosts is None
        assert config.secretRefs is None
        assert config.configmapRefs is None
        assert config.intervals is None
        assert config.cleaningIntervals is None
        assert config.ttl is None
        assert len(config.privateRegistries) == 3
        assert config.persistence.logs.to_dict() == {
            'mountPath': "/tmp/logs", 'hostPath': "/tmp/logs"}
        assert config.persistence.repos.to_dict() == {
            'mountPath': "/tmp/repos", 'hostPath': "/tmp/repos"}
        assert config.persistence.upload.to_dict() == {'existingClaim': "foo"}
        assert len(config.persistence.data) == 1
        assert len(config.persistence.outputs) == 1

    def test_read_deploy_config_values3(self):
        config = reader.read('tests/fixtures/values3.yml')
        assert isinstance(config, DeploymentConfig)
        assert config.deploymentType is None
        assert config.namespace is None
        assert config.rbac.enabled is True
        assert config.adminViewEnabled is None
        assert config.timeZone is None
        assert config.environment == 'staging'
        assert config.ingress.enabled is True
        assert config.serviceType == 'ClusterIP'
        assert config.user.to_dict() == {'password': 'root'}
        assert config.nodeSelectors.to_dict() == {
            'core': {'polyaxon': 'core'},
            'builds': {'polyaxon': 'core'}
        }
        assert config.tolerations is None
        assert config.affinity is None
        assert config.limitResources is None
        assert config.globalReplicas is None
        assert config.globalConcurrency is None
        assert config.api.replicas == 3
        assert config.streams is None
        assert config.scheduler.replicas == 3
        assert config.hpsearch.replicas == 3
        assert config.eventsHandlers.replicas == 3
        assert config.k8sEventsHandlers.replicas == 3
        assert config.beat is None
        assert config.crons is None
        assert config.eventMonitors.replicas == 3
        assert config.resourcesDaemon is None
        assert config.sidecar is None
        assert config.dockerizer is None
        assert config.hooks is None
        assert config.postgresql.install is False
        assert config.rabbitmq is None
        assert config.dockerRegistry is None
        assert config.email is not None
        assert len(config.integrations.slack) == 2
        assert len(config.integrations.to_dict()) == 1
        assert config.hostName == '123.123.123.123'
        assert config.allowedHosts == ['foo.bar.com', '123.123.12.3']
        assert config.secretRefs == ['foo', 'moo']
        assert config.configmapRefs == ['foo', 'bar']
        assert config.intervals is None
        assert config.cleaningIntervals is None
        assert config.ttl is None
        assert len(config.privateRegistries) == 3
        assert config.persistence.logs is None
        assert config.persistence.repos is None
        assert config.persistence.upload is None
        assert len(config.persistence.data) == 3
        assert len(config.persistence.outputs) == 3
        assert config.trackerBackend is None
        assert config.mountCodeInNotebooks is None

    def test_read_deploy_config_values4(self):
        config = reader.read('tests/fixtures/values4.yml')
        assert isinstance(config, DeploymentConfig)
        assert config.deploymentType is None
        assert config.namespace is None
        assert config.rbac.enabled is True
        assert config.adminViewEnabled is None
        assert config.timeZone == 'Europe/Berlin'
        assert config.environment == 'staging'
        assert config.ingress.enabled is True
        assert config.serviceType == 'ClusterIP'
        assert config.user.to_dict() == {'password': 'test'}
        assert config.nodeSelectors.to_dict() == {
            'core': {'polyaxon': 'core'},
            'experiments': {'polyaxon': 'experiments'},
            'builds': {'polyaxon': 'experiments'},
            'jobs': {'polyaxon': 'experiments'},
            'tensorboards': {'polyaxon': 'experiments'},
        }
        assert config.tolerations is None
        assert config.affinity is None
        assert config.limitResources is None
        assert config.globalReplicas is None
        assert config.globalConcurrency is None
        assert config.api.replicas == 1
        assert config.streams.imageTag == 'latest'
        assert config.scheduler.replicas == 1
        assert config.hpsearch.replicas == 1
        assert config.eventsHandlers.replicas == 1
        assert config.k8sEventsHandlers.replicas == 1
        assert config.beat.imageTag == 'latest'
        assert config.crons.imageTag == 'latest'
        assert config.eventMonitors.replicas == 1
        assert config.resourcesDaemon.imageTag == 'latest'
        assert config.sidecar.imageTag == 'latest'
        assert config.dockerizer.imageTag == 'latest'
        assert config.hooks.imageTag == 'latest'
        assert config.postgresql is None
        assert config.rabbitmq is None
        assert config.dockerRegistry is None
        assert config.email is None
        assert len(config.integrations.slack) == 1
        assert len(config.integrations.to_dict()) == 1
        assert config.hostName == '19.3.50.12'
        assert config.allowedHosts == ['127.0.0.1', '123.123.12.3']
        assert config.secretRefs == ['pubsub-key']
        assert config.configmapRefs is None
        assert config.intervals is None
        assert config.cleaningIntervals is None
        assert config.ttl.watchStatuses == 10
        assert len(config.privateRegistries) == 3
        assert config.persistence.logs is not None
        assert config.persistence.repos is not None
        assert config.persistence.upload is not None
        assert len(config.persistence.data) == 2
        assert len(config.persistence.outputs) == 2
        assert config.notebookBackend == 'lab'
        assert config.notebookDockerImage == "jupyter/datascience-notebook"
        assert config.mountCodeInNotebooks is True
        assert config.trackerBackend is None
        assert config.buildBackend is None

    def test_read_deploy_config_values5(self):
        config = reader.read('tests/fixtures/values5.yml')
        assert isinstance(config, DeploymentConfig)
        assert config.deploymentType is None
        assert config.namespace is None
        assert config.rbac.enabled is True
        assert config.adminViewEnabled is None
        assert config.timeZone == 'Europe/Berlin'
        assert config.environment == 'staging'
        assert config.ingress.enabled is True
        assert config.serviceType == 'ClusterIP'
        assert config.user.to_dict() == {'password': 'test'}
        assert config.nodeSelectors.to_dict() == {
            'core': {'polyaxon': 'core'},
            'experiments': {'polyaxon': 'experiments'},
            'builds': {'polyaxon': 'experiments'},
            'jobs': {'polyaxon': 'experiments'},
            'tensorboards': {'polyaxon': 'experiments'},
        }
        assert config.tolerations is None
        assert config.affinity is None
        assert config.limitResources is None
        assert config.globalReplicas is None
        assert config.globalConcurrency is None
        assert config.api.replicas == 1
        assert config.streams.imageTag == 'latest'
        assert config.scheduler.replicas == 1
        assert config.hpsearch.replicas == 1
        assert config.eventsHandlers.replicas == 1
        assert config.k8sEventsHandlers.replicas == 1
        assert config.beat.imageTag == 'latest'
        assert config.crons.imageTag == 'latest'
        assert config.eventMonitors.replicas == 1
        assert config.resourcesDaemon.imageTag == 'latest'
        assert config.sidecar.imageTag == 'latest'
        assert config.dockerizer.imageTag == 'latest'
        assert config.hooks.imageTag == 'latest'
        assert config.postgresql is None
        assert config.rabbitmq is None
        assert config.dockerRegistry is None
        assert config.email is None
        assert len(config.integrations.slack) == 1
        assert len(config.integrations.to_dict()) == 1
        assert config.hostName == '19.3.50.12'
        assert config.allowedHosts == ['127.0.0.1', '123.123.12.3']
        assert config.secretRefs == ['pubsub-key']
        assert config.configmapRefs is None
        assert config.intervals is None
        assert config.cleaningIntervals is None
        assert config.ttl.watchStatuses == 10
        assert len(config.privateRegistries) == 3
        assert config.persistence.logs is not None
        assert config.persistence.repos is not None
        assert config.persistence.upload is not None
        assert len(config.persistence.data) == 2
        assert len(config.persistence.outputs) == 2
        assert config.notebookBackend == 'lab'
        assert config.notebookDockerImage == "jupyter/datascience-notebook"
        assert config.mountCodeInNotebooks is None
        assert config.trackerBackend == 'noop'
        assert config.buildBackend == 'kaniko'
        assert config.dirs == {
            'nvidia': {'lib': '', 'bin': '', 'libcuda': ''}
        }
        assert config.mountPaths == {
            'nvidia': {'lib': '', 'bin': '', 'libcuda': ''}
        }

    def test_read_deploy_config_wrong_values1(self):
        with self.assertRaises(ValidationError):
            reader.read('tests/fixtures/wrong_values2.yml')

    def test_read_deploy_config_wrong_values2(self):
        with self.assertRaises(ValidationError):
            reader.read('tests/fixtures/wrong_values2.yml')
