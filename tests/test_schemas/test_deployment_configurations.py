# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError

from polyaxon_cli.cli.deploy import read_deployment_config
from polyaxon_cli.schemas.deployment_configuration import (
    AffinityConfig,
    CleaningIntervalsConfig,
    DeploymentConfig,
    DockerRegistryConfig,
    EmailConfig,
    EventMonitorsConfig,
    IngressConfig,
    IntegrationsConfig,
    IntervalsConfig,
    NodeSelectorsConfig,
    PostgresqlConfig,
    RabbitmqConfig,
    RBACConfig,
    RedisConfig,
    RootUserConfig,
    ServiceConfig,
    ThirdPartyServiceConfig,
    TolerationsConfig,
    TTLConfig
)


class TestDeploymentConfig(TestCase):
    def test_rbac_config(self):
        config_dict = {'enabled': True}
        config = RBACConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config_dict = {'enabled': False}
        config = RBACConfig.from_dict(config_dict)
        assert config.to_dict() == config_dict

        config = RBACConfig.from_dict({})
        assert config.to_dict() == {}
        assert config.to_light_dict() == {}

    def test_ingress_config(self):
        config_dict = {
            'enabled': 'sdf',
        }

        with self.assertRaises(ValidationError):
            IngressConfig.from_dict(config_dict)

        config_dict = {
            'enabled': False,
        }

        config = IngressConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'enabled': False,
            'tls': {'hosts': 'bar.com'},
            'annotations': {'a': 'b'},
            'resources': {'limits': {'cpu': 0.1, 'memory': '80Mi'}}
        }

        config = IngressConfig.from_dict(config_dict)

        assert config.to_light_dict() == config_dict

    def test_root_user_config(self):
        bad_config_dicts = [
            {
                'username': False,
                'password': 'foo',
                'email': 'sdf'

            },
            {
                'username': 'sdf',
                'password': 'foo',
                'email': 'sdf'
            },
            {
                'username': 'sdf',
                'password': 'foo',
                'email': 'sdf@boo'
            },

        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                RootUserConfig.from_dict(config_dict)

        config_dict = {
            'username': 'sdf',
            'password': 'foo',

        }

        config = RootUserConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'username': 'sdf',
            'password': 'foo',
            'email': 'foo@bar.com'

        }

        config = RootUserConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_node_selectors_config(self):
        bad_config_dicts = [
            {
                'core': False,
            },
            {
                'experiments': 'foo',
            },
            {
                'builds': 'foo',
            },
            {
                'jobs': 'foo',
            },
            {
                'tensorboards': 123,
            },
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                NodeSelectorsConfig.from_dict(config_dict)

        config_dict = {
            'core': {}

        }

        config = NodeSelectorsConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'experiments': {
                'polyaxon.com': 'experiments'
            },
            'tensorboards': {
                'polyaxon.jobs': 'jobs',
                'polyaxon.tensorboards': 'tensorboards'
            }
        }

        config = NodeSelectorsConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_affinity_config(self):
        bad_config_dicts = [
            {
                'core': False,
            },
            {
                'experiments': 'foo',
            },
            {
                'builds': 'foo',
            },
            {
                'jobs': 'foo',
            },
            {
                'tensorboards': 123,
            },
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                AffinityConfig.from_dict(config_dict)

        config_dict = {
            'core': {}

        }

        config = AffinityConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'experiments': {
                'podAffinity': {
                    'preferredDuringSchedulingIgnoredDuringExecution':
                        [
                            {'weight': 100},
                        ]
                }
            }
        }

        config = NodeSelectorsConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_tolerations_config(self):
        bad_config_dicts = [
            {
                'core': False,
            },
            {
                'experiments': 'foo',
            },
            {
                'builds': 'foo',
            },
            {
                'jobs': 'foo',
            },
            {
                'tensorboards': 123,
            },
            {
                'core': {},
                'tensorboards': [],
            },
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                TolerationsConfig.from_dict(config_dict)

        config_dict = {
            'core': []
        }

        config = TolerationsConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'core': [
                {
                    'key': 'key',
                    'operator': 'Equal',
                    'value': 'value',
                    'effect': 'NoSchedule',
                }
            ],
            'experiments': [
                {
                    'key': 'key',
                    'operator': 'Equal',
                    'value': 'value',
                    'effect': 'NoSchedule',
                },
                {
                    'key': 'key',
                    'operator': 'Exists',
                    'effect': 'NoSchedule',
                }
            ],
        }

        config = TolerationsConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def service_config_test(self):
        bad_config_dicts = [
            {
                'image': False,
                'imageTag': 'foo',
                'imagePullPolicy': 'sdf'

            },
            {
                'replicas': 'sdf',
            },
            {
                'concurrency': 'foo',
            },
            {
                'replicas': 12,
                'resources': 'foo'
            }

        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                ServiceConfig.from_dict(config_dict)

        config_dict = {
            'image': 'foo',
            'imageTag': 'bar',
            'imagePullPolicy': 'Always'

        }

        config = ServiceConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'image': 'foo',
            'replicas': 12,
            'concurrency': 12,

        }

        config = ServiceConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'resources': {'requests': {'cpu': 2}, 'limits': {'memory': '500Mi'}},
        }

        config = ServiceConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_events_monitor_config(self):
        bad_config_dicts = [
            {
                'replicas': 'sdf',
            },
            {
                'namespace': 'foo',
            },
            {
                'replicas': 12,
                'statuses': 'foo'
            }

        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                EventMonitorsConfig.from_dict(config_dict)

        config_dict = {
            'replicas': 12,
            'namespace': {
                'image': 'foo',
                'imageTag': 'bar',
                'imagePullPolicy': 'Always'

            },

        }

        config = EventMonitorsConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'statuses': {
                'resources': {
                    'requests': {'cpu': 2}, 'limits': {'memory': '500Mi'}
                },
            }
        }

        config = EventMonitorsConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_third_party_service(self):
        bad_config_dicts = [
            {
                'image': False,
                'imageTag': 'foo',
                'imagePullPolicy': 'sdf'

            },
            {
                'replicas': 'sdf',
            },
            {
                'concurrency': 12,
            },
            {
                'resources': 'foo'
            },
            {
                'install': 'sdf'
            },
            {
                'persistence': 'sdf'
            },
            {
                'nodeSelector': 'sdf'
            },
            {
                'affinity': 'sdf'
            },
            {
                'tolerations': 'sdf'
            },
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises((ValidationError, TypeError)):
                ThirdPartyServiceConfig.from_dict(config_dict)

        config_dict = {
            'image': 'foo',
            'imageTag': 'bar',
            'imagePullPolicy': 'Always',
            'replicas': 2

        }

        config = ThirdPartyServiceConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'resources': {'requests': {'cpu': 2}, 'limits': {'memory': '500Mi'}},
            'tolerations': [
                {
                    'key': 'key',
                    'operator': 'Equal',
                    'value': 'value',
                    'effect': 'NoSchedule',
                }
            ],
            'affinity': {}
        }

        config = ThirdPartyServiceConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_postgresql_config(self):
        config_dict = {
            'postgresUser': 'dsf',
            'postgresPassword': 'sdf',
            'postgresDatabase': 'sdf',
            'externalPostgresHost': 123
        }
        with self.assertRaises(ValidationError):
            PostgresqlConfig.from_dict(config_dict)

        config_dict = {
            'install': True,
            'postgresUser': 'dsf',
            'postgresPassword': 'sdf',
            'postgresDatabase': 'sdf',
            'externalPostgresHost': 'sdf',
            'resources': {'requests': {'cpu': 2}, 'limits': {'memory': '500Mi'}},
            'tolerations': [
                {
                    'key': 'key',
                    'operator': 'Equal',
                    'value': 'value',
                    'effect': 'NoSchedule',
                }
            ],
            'affinity': {}
        }
        config = PostgresqlConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'postgresUser': 'dsf',
            'externalPostgresHost': 'sdf',
            'resources': {'requests': {'cpu': 2}, 'limits': {'memory': '500Mi'}},
            'tolerations': [
                {
                    'key': 'key',
                    'operator': 'Equal',
                    'value': 'value',
                    'effect': 'NoSchedule',
                }
            ],
            'affinity': {}
        }
        config = PostgresqlConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_redis_config(self):
        config_dict = {
            'usePassword': 'dsf',
            'redisPassword': 'sdf',
            'externalRedisHost': 123
        }
        with self.assertRaises(ValidationError):
            RedisConfig.from_dict(config_dict)

        config_dict = {
            'install': True,
            'usePassword': True,
            'redisPassword': 'sdf',
            'externalRedisHost': 'sd123',
            'resources': {'requests': {'cpu': 2}, 'limits': {'memory': '500Mi'}},
            'tolerations': [
                {
                    'key': 'key',
                    'operator': 'Equal',
                    'value': 'value',
                    'effect': 'NoSchedule',
                }
            ],
            'affinity': {}
        }
        config = RedisConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'redisPassword': 'sdf',
            'externalRedisHost': 'sd123',
            'resources': {'requests': {'cpu': 2}, 'limits': {'memory': '500Mi'}},
            'tolerations': [
                {
                    'key': 'key',
                    'operator': 'Equal',
                    'value': 'value',
                    'effect': 'NoSchedule',
                }
            ],
            'affinity': {}
        }
        config = RedisConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_rabbitmq_config(self):
        config_dict = {
            'rabbitmqUsername': 'dsf',
            'rabbitmqPassword': 'sdf',
            'externalRabbitmqHost': 123
        }
        with self.assertRaises(ValidationError):
            RabbitmqConfig.from_dict(config_dict)

        config_dict = {
            'install': True,
            'rabbitmqUsername': 'dsf',
            'rabbitmqPassword': 'sdf',
            'externalRabbitmqHost': 'sd123',
            'resources': {'requests': {'cpu': 2}, 'limits': {'memory': '500Mi'}},
            'tolerations': [
                {
                    'key': 'key',
                    'operator': 'Equal',
                    'value': 'value',
                    'effect': 'NoSchedule',
                }
            ],
            'affinity': {}
        }
        config = RabbitmqConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'rabbitmqUsername': 'dsf',
            'rabbitmqPassword': 'sdf',
            'resources': {'requests': {'cpu': 2}, 'limits': {'memory': '500Mi'}},
            'tolerations': [
                {
                    'key': 'key',
                    'operator': 'Equal',
                    'value': 'value',
                    'effect': 'NoSchedule',
                }
            ],
            'affinity': {}
        }
        config = RabbitmqConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_docker_registry_config(self):
        config_dict = {
            'registryUser': 'dsf',
            'registryPassword': 'sdf',
            'externalRegistryHost': 123
        }
        with self.assertRaises(ValidationError):
            DockerRegistryConfig.from_dict(config_dict)

        config_dict = {
            'install': True,
            'registryUser': 'dsf',
            'registryPassword': 'sdf',
            'externalRegistryHost': 'sd123',
            'resources': {'requests': {'cpu': 2}, 'limits': {'memory': '500Mi'}},
            'tolerations': [
                {
                    'key': 'key',
                    'operator': 'Equal',
                    'value': 'value',
                    'effect': 'NoSchedule',
                }
            ],
            'affinity': {}
        }
        config = DockerRegistryConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'registryUser': 'dsf',
            'registryPassword': 'sdf',
            'resources': {'requests': {'cpu': 2}, 'limits': {'memory': '500Mi'}},
            'tolerations': [
                {
                    'key': 'key',
                    'operator': 'Equal',
                    'value': 'value',
                    'effect': 'NoSchedule',
                }
            ],
            'affinity': {}
        }
        config = DockerRegistryConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_email_config(self):
        config_dict = {
            'host': 'dsf',
            'port': 'sdf',
            'useTls': 123,
            'hostUser': 'sdf',
            'hostPassword': 'sdf'
        }
        with self.assertRaises(ValidationError):
            EmailConfig.from_dict(config_dict)

        config_dict = {
            'host': 'dsf',
            'port': 123,
            'useTls': False,
            'hostUser': 'sdf',
            'hostPassword': 'sdf'
        }
        config = EmailConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_integrations_config(self):
        bad_config_dicts =[
            {
                'slack': 'dsf',
            },
            {
                'hipchat': 'dsf',
            },
            {
                'mattermost': 'dsf',
            },
            {
                'discord': 'dsf',
            },
            {
                'pagerduty': 'dsf',
            },
            {
                'webhooks': 'dsf',
            },
            {
                'webhooks': ['dsf'],
            }
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                IntegrationsConfig.from_dict(config_dict)

        config_dict = {
            'slack': [{'url': 'dsf'}, {'url': 'dsf'}],
            'webhooks': [{'url': 'dsf'}, {'url': 'dsf'}],
        }
        config = IntegrationsConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_intervals_config(self):
        bad_config_dicts = [
            {
                'experimentsScheduler': 'dsf',
            },
            {
                'experimentsSync': 'dsf',
            },
            {
                'clustersUpdateSystemInfo': 'dsf',
            },
            {
                'clustersUpdateSystemNodes': 'dsf',
            },
            {
                'operationsDefaultRetryDelay': 'dsf',
            },
            {
                'operationsMaxRetryDelay': ['dsf'],
            }
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                IntervalsConfig.from_dict(config_dict)

        config_dict = {
            'experimentsScheduler': 12,
            'experimentsSync': 12,
            'clustersUpdateSystemInfo': 12,
            'clustersUpdateSystemNodes': 12,
            'pipelinesScheduler': 12,
            'operationsDefaultRetryDelay': 12,
            'operationsMaxRetryDelay': 12,
        }
        config = IntervalsConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_cleaning_intervals_config(self):
        bad_config_dicts = [
            {
                'archived': 'dsf',
            },
            {
                'archived': ['dsf'],
            }
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                CleaningIntervalsConfig.from_dict(config_dict)

        config_dict = {
            'archived': 12,
        }
        config = CleaningIntervalsConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_ttl_config(self):
        bad_config_dicts = [
            {
                'token': 'dsf',
            },
            {
                'ephemeralToken': ['dsf'],
            },
            {
                'heartbeat': 'heartbeat'
            }
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                TTLConfig.from_dict(config_dict)

        config_dict = {
            'token': 12,
        }
        config = TTLConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            'token': 12,
            'ephemeralToken': 12,
            'heartbeat': 21,
        }
        config = TTLConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_read_deploy_config_values1(self):
        config = read_deployment_config('tests/fixtures/values1.yml')
        assert isinstance(config, DeploymentConfig)
        assert config.deploymentType == 'docker-compose'
        assert config.namespace is None
        assert config.rbac.enabled is True
        assert config.adminViewEnabled is None
        assert config.timeZone is None
        assert config.environment == 'staging'
        assert config.ingress.enabled is True
        assert config.serviceType == 'clusterIP'
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
        assert config.reourcesDaemon is None
        assert config.sidecar is None
        assert config.dockerizer is None
        assert config.hooks is None
        assert config.postgresql.install is False
        assert config.rabbitmq is None
        assert config.dockerRegistry is None
        assert config.email is None
        assert config.integrations is None
        assert config.apiHost is None
        assert config.allowedHosts is None
        assert config.secretRefs is None
        assert config.configmapRefs is None
        assert config.intervals is None
        assert config.cleaningIntervals is None
        assert config.ttl is None
        assert config.privateRegistries is None
        assert config.persistence is None

    def test_read_deploy_config_values2(self):
        config = read_deployment_config('tests/fixtures/values2.yml')
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
        assert config.reourcesDaemon is None
        assert config.sidecar is None
        assert config.dockerizer is None
        assert config.hooks is None
        assert config.postgresql.persistence is not None
        assert config.rabbitmq is None
        assert config.dockerRegistry is None
        assert config.email is not None
        assert len(config.integrations.slack) == 2
        assert len(config.integrations.to_dict()) == 1
        assert config.apiHost is None
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
        config = read_deployment_config('tests/fixtures/values3.yml')
        assert isinstance(config, DeploymentConfig)
        assert config.deploymentType is None
        assert config.namespace is None
        assert config.rbac.enabled is True
        assert config.adminViewEnabled is None
        assert config.timeZone is None
        assert config.environment == 'staging'
        assert config.ingress.enabled is True
        assert config.serviceType == 'clusterIP'
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
        assert config.reourcesDaemon is None
        assert config.sidecar is None
        assert config.dockerizer is None
        assert config.hooks is None
        assert config.postgresql.install is False
        assert config.rabbitmq is None
        assert config.dockerRegistry is None
        assert config.email is not None
        assert len(config.integrations.slack) == 2
        assert len(config.integrations.to_dict()) == 1
        assert config.apiHost is None
        assert config.allowedHosts is None
        assert config.secretRefs is None
        assert config.configmapRefs is None
        assert config.intervals is None
        assert config.cleaningIntervals is None
        assert config.ttl is None
        assert len(config.privateRegistries) == 3
        assert config.persistence.logs is None
        assert config.persistence.repos is None
        assert config.persistence.upload is None
        assert len(config.persistence.data) == 3
        assert len(config.persistence.outputs) == 3

    def test_read_deploy_config_wrong_values1(self):
        with self.assertRaises(SystemExit):
            read_deployment_config('tests/fixtures/wrong_values2.yml')

    def test_read_deploy_config_wrong_values2(self):
        with self.assertRaises(SystemExit):
            read_deployment_config('tests/fixtures/wrong_values2.yml')
