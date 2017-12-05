# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from libs.redis_db import RedisToStream

from tests.utils import BaseTest


class TestRedisToStream(BaseTest):
    def test_monitor_job_resources(self):
        job_uuid = uuid.uuid4().hex
        RedisToStream.monitor_job_resources(job_uuid)
        assert RedisToStream.is_monitored_job_resources(job_uuid) is True
        RedisToStream.remove_job_resources(job_uuid)
        assert RedisToStream.is_monitored_job_resources(job_uuid) is False

    def test_monitor_job_logs(self):
        job_uuid = uuid.uuid4().hex
        RedisToStream.monitor_job_logs(job_uuid)
        assert RedisToStream.is_monitored_job_logs(job_uuid) is True
        RedisToStream.remove_job_logs(job_uuid)
        assert RedisToStream.is_monitored_job_logs(job_uuid) is False

    def test_monitor_experiment_resources(self):
        expeirment_uuid = uuid.uuid4().hex
        RedisToStream.monitor_experiment_resources(expeirment_uuid)
        assert RedisToStream.is_monitored_experiment_resources(expeirment_uuid) is True
        RedisToStream.remove_experiment_resources(expeirment_uuid)
        assert RedisToStream.is_monitored_experiment_resources(expeirment_uuid) is False

    def test_monitor_experiment_logs(self):
        expeirment_uuid = uuid.uuid4().hex
        RedisToStream.monitor_experiment_logs(expeirment_uuid)
        assert RedisToStream.is_monitored_experiment_logs(expeirment_uuid) is True
        RedisToStream.remove_experiment_logs(expeirment_uuid)
        assert RedisToStream.is_monitored_experiment_logs(expeirment_uuid) is False

    def test_set_latest_job_resources(self):
        gpu_resources = {
            'index': 0,
            'bus_id': '0000:00:1E.1',
            'memory_free': 1000,
            'memory_total': 12883853312,
            'memory_used': 8388608000,
            'memory_utilization': 0,
            'minor': 1,
            'name': 'GeForce GTX TITAN 0',
            'power_draw': 125,
            'power_limit': 250,
            'processes': [{'command': 'python',
                           'gpu_memory_usage': 4000,
                           'pid': 48448,
                           'username': 'user1'},
                          {'command': 'python',
                           'gpu_memory_usage': 4000,
                           'pid': 153223,
                           'username': 'user2'}],
            'serial': '0322917092147',
            'temperature_gpu': 80,
            'utilization_gpu': 76,
            'uuid': 'GPU-10fb0fbd-2696-43f3-467f-d280d906a107'
        }

        config_dict = {
            'job_uuid': uuid.uuid4().hex,
            'experiment_uuid': uuid.uuid4().hex,
            'container_id': '3175e88873af9077688cee20eaadc0c07746efb84d01ae696d6d17ed9bcdfbc4',
            'cpu_percentage': 0.6947691836734693,
            'percpu_percentage': [0.4564075715616173, 0.23836161211185192],
            'memory_used': 84467712,
            'memory_limit': 2096160768,
            'gpu_resources': gpu_resources
        }

        RedisToStream.set_latest_job_resources(config_dict['job_uuid'], config_dict)
        assert config_dict == RedisToStream.get_latest_job_resources(config_dict['job_uuid'])
