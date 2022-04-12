#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from typing import Any

import redis


class BaseRedisDb:
    REDIS_POOL = None

    @classmethod
    def _get_redis(cls) -> Any:
        return redis.Redis(
            connection_pool=cls.REDIS_POOL, retry_on_timeout=True, socket_keepalive=True
        )

    @classmethod
    def connection(cls) -> Any:
        return cls._get_redis()
