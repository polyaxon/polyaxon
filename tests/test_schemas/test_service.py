# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

from marshmallow import ValidationError
from polyaxon_deploy.schemas.service import (
    DockerRegistryConfig,
    EventMonitorsConfig,
    PostgresqlConfig,
    RabbitmqConfig,
    RedisConfig,
    ServiceConfig,
    ThirdPartyServiceConfig
)


class TestServiceConfig(TestCase):

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
