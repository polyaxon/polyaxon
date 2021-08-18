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
from polyaxon.fs.fs import get_default_fs
from polyaxon.fs.types import FSSystem


class AppFS:
    FS = None

    @classmethod
    async def set_fs(cls) -> FSSystem:
        fs = await get_default_fs()
        cls.FS = fs
        return cls.FS

    @classmethod
    async def close_fs(cls):
        if cls.FS and hasattr(cls.FS, "close_session"):
            cls.FS.close_session(cls.FS.loop, cls.FS.session)

    @classmethod
    async def get_fs(cls) -> FSSystem:
        if not cls.FS:
            return await cls.set_fs()
        return cls.FS
