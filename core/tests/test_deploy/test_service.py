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

from marshmallow import ValidationError
from tests.utils import BaseTestCase

from polyaxon.deploy.schemas.service import (
    ExternalService,
    ExternalServicesConfig,
    PostgresqlConfig,
    RabbitmqConfig,
    RedisConfig,
    Service,
    ThirdPartyService,
)


class TestService(BaseTestCase):
    def service_config_test(self):
        bad_config_dicts = [
            {"image": False, "imageTag": "foo", "imagePullPolicy": "sdf"},
            {"replicas": "sdf"},
            {"concurrency": "foo"},
            {"replicas": 12, "resources": "foo"},
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises(ValidationError):
                Service.from_dict(config_dict)

        config_dict = {"image": "foo", "imageTag": "bar", "imagePullPolicy": "Always"}

        config = Service.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {"image": "foo", "replicas": 12, "concurrency": 12}

        config = Service.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            "resources": {"requests": {"cpu": 2}, "limits": {"memory": "500Mi"}}
        }

        config = Service.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_third_party_service(self):
        bad_config_dicts = [
            {"image": False, "imageTag": "foo", "imagePullPolicy": "sdf"},
            {"replicas": "sdf"},
            {"concurrency": 12},
            {"resources": "foo"},
            {"enabled": "sdf"},
            {"persistence": "sdf"},
            {"nodeSelector": "sdf"},
            {"affinity": "sdf"},
            {"tolerations": "sdf"},
        ]

        for config_dict in bad_config_dicts:
            with self.assertRaises((ValidationError, TypeError)):
                ThirdPartyService.from_dict(config_dict)

        config_dict = {
            "image": "foo",
            "imageTag": "bar",
            "imagePullPolicy": "Always",
            "replicas": 2,
        }

        config = ThirdPartyService.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            "resources": {"requests": {"cpu": 2}, "limits": {"memory": "500Mi"}},
            "tolerations": [
                {
                    "key": "key",
                    "operator": "Equal",
                    "value": "value",
                    "effect": "NoSchedule",
                }
            ],
            "affinity": {},
        }

        config = ThirdPartyService.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_postgresql_config(self):
        config_dict = {
            "postgresUser": "dsf",
            "postgresPassword": "sdf",
            "postgresDatabase": "sdf",
            "postgresHost": "sdf",
        }
        with self.assertRaises(ValidationError):
            PostgresqlConfig.from_dict(config_dict)

        config_dict = {
            "enabled": True,
            "postgresUser": "dsf",
            "postgresPassword": "sdf",
            "postgresDatabase": "sdf",
            "resources": {"requests": {"cpu": 2}, "limits": {"memory": "500Mi"}},
            "tolerations": [
                {
                    "key": "key",
                    "operator": "Equal",
                    "value": "value",
                    "effect": "NoSchedule",
                }
            ],
            "affinity": {},
        }
        config = PostgresqlConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            "postgresUser": "dsf",
            "resources": {"requests": {"cpu": 2}, "limits": {"memory": "500Mi"}},
            "tolerations": [
                {
                    "key": "key",
                    "operator": "Equal",
                    "value": "value",
                    "effect": "NoSchedule",
                }
            ],
            "affinity": {},
        }
        config = PostgresqlConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_redis_config(self):
        config_dict = {
            "usePassword": "dsf",
            "password": "sdf",
            "externalRedisHost": 123,
        }
        with self.assertRaises(ValidationError):
            RedisConfig.from_dict(config_dict)

        config_dict = {
            "enabled": True,
            "usePassword": True,
            "password": "sdf",
            "resources": {"requests": {"cpu": 2}, "limits": {"memory": "500Mi"}},
            "tolerations": [
                {
                    "key": "key",
                    "operator": "Equal",
                    "value": "value",
                    "effect": "NoSchedule",
                }
            ],
            "affinity": {},
        }
        config = RedisConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            "password": "sdf",
            "resources": {"requests": {"cpu": 2}, "limits": {"memory": "500Mi"}},
            "tolerations": [
                {
                    "key": "key",
                    "operator": "Equal",
                    "value": "value",
                    "effect": "NoSchedule",
                }
            ],
            "affinity": {},
        }
        config = RedisConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_rabbitmq_config(self):
        config_dict = {
            "rabbitmqUsername": "dsf",
            "rabbitmqPassword": "sdf",
            "externalRabbitmqHost": 123,
        }
        with self.assertRaises(ValidationError):
            RabbitmqConfig.from_dict(config_dict)

        config_dict = {
            "enabled": True,
            "rabbitmqUsername": "dsf",
            "rabbitmqPassword": "sdf",
            "resources": {"requests": {"cpu": 2}, "limits": {"memory": "500Mi"}},
            "tolerations": [
                {
                    "key": "key",
                    "operator": "Equal",
                    "value": "value",
                    "effect": "NoSchedule",
                }
            ],
            "affinity": {},
        }
        config = RabbitmqConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            "rabbitmqUsername": "dsf",
            "rabbitmqPassword": "sdf",
            "resources": {"requests": {"cpu": 2}, "limits": {"memory": "500Mi"}},
            "tolerations": [
                {
                    "key": "key",
                    "operator": "Equal",
                    "value": "value",
                    "effect": "NoSchedule",
                }
            ],
            "affinity": {},
        }
        config = RabbitmqConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_external_service_config(self):
        config_dict = {
            "user": "user",
            "password": "pass",
            "host": "123.123.123.123",
            "port": "user",
        }
        with self.assertRaises(ValidationError):
            ExternalService.from_dict(config_dict)

        config_dict = {
            "user": "user",
            "password": "pass",
            "host": "123.123.123.123",
            "port": 123231,
        }
        config = ExternalService.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            "user": "user",
            "password": "pass",
            "host": "123.123.123.123",
            "port": 123231,
            "database": "sdf",
            "usePassword": True,
            "connMaxAge": 100,
        }
        config = ExternalService.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

    def test_test_external_services_config(self):
        config_dict = {
            "postgresql": {
                "user": "user",
                "password": "pass-pg",
                "host": "123.123.123.123",
                "port": 5656,
            },
            "redis": {
                "usePassword": True,
                "password": "pass-redis",
                "host": "https://foo.com",
                "port": 2344,
            },
            "rabbitmq": {"foo": "bar"},
        }
        with self.assertRaises(ValidationError):
            ExternalServicesConfig.from_dict(config_dict)

        config_dict = {
            "redis": {
                "usePassword": True,
                "password": "pass-redis",
                "host": "https://foo.com",
                "port": 2344,
            },
            "rabbitmq": {
                "user": "mq-0user",
                "password": "pass-redis",
                "host": "https://foo.com",
                "port": 2344,
            },
        }
        config = ExternalServicesConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict

        config_dict = {
            "postgresql": {
                "user": "user",
                "password": "pass-pg",
                "host": "123.123.123.123",
                "port": 5656,
                "connMaxAge": 123,
            },
            "redis": {
                "usePassword": True,
                "password": "pass-redis",
                "host": "https://foo.com",
                "port": 2344,
            },
            "rabbitmq": {
                "user": "mq-0user",
                "password": "pass-redis",
                "host": "https://foo.com",
                "port": 2344,
            },
        }
        config = ExternalServicesConfig.from_dict(config_dict)
        assert config.to_light_dict() == config_dict
