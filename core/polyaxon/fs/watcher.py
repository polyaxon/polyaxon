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
import json
import os

from collections import namedtuple
from datetime import datetime
from typing import Dict, List

from marshmallow import fields

from polyaxon.containers.contexts import CONTEXT_MOUNT_FILE_WATCHER
from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.utils.date_utils import path_last_modified
from polyaxon.utils.path_utils import get_files_and_dirs_in_path


class PathData(namedtuple("PathData", "base ts op")):
    pass


class FSWatcherSchema(BaseSchema):
    dir_mapping = fields.Dict(allow_none=True)
    file_mapping = fields.Dict(allow_none=True)

    @staticmethod
    def schema_config():
        return FSWatcherConfig


class FSWatcherConfig(BaseConfig):
    SCHEMA = FSWatcherSchema
    IDENTIFIER = "fswatcher"

    def __init__(self, dir_mapping=None, file_mapping=None, **kwargs):
        self.dir_mapping = dir_mapping
        self.file_mapping = file_mapping

    @staticmethod
    def _datetime_handler(value):
        if isinstance(value, datetime):
            return value.isoformat()
        raise TypeError("Unknown type")

    @classmethod
    def _dump(cls, obj_dict):
        return json.dumps(obj_dict, default=cls._datetime_handler)

    @staticmethod
    def _parse_mapping(mapping: Dict):
        if not mapping:
            return None
        return {
            k: PathData(v[0], datetime.fromisoformat(v[1]), v[2])
            for k, v in mapping.items()
        }

    @staticmethod
    def delete(path: str):
        if os.path.exists(path):
            os.remove(path)

    def get_dir_mapping(self):
        return self._parse_mapping(self.dir_mapping)

    def get_file_mapping(self):
        return self._parse_mapping(self.file_mapping)


class FSWatcher:
    PUT = "put"
    RM = "rm"
    NOOP = ""

    def __init__(self, dir_mapping: Dict = None, file_mapping: Dict = None):
        self._dir_mapping = dir_mapping or {}
        self._file_mapping = file_mapping or {}

    @classmethod
    def read(cls, config_path: str = CONTEXT_MOUNT_FILE_WATCHER):
        if not os.path.exists(config_path):
            return cls()
        config = FSWatcherConfig.read(config_path)
        return cls(
            dir_mapping=config.get_dir_mapping(), file_mapping=config.get_file_mapping()
        )

    def write(self, config_path: str = CONTEXT_MOUNT_FILE_WATCHER):
        config = FSWatcherConfig.read(
            {
                "dir_mapping": self._dir_mapping,
                "file_mapping": self._file_mapping,
            }
        )
        return config.write(config_path)

    def _sync_path(self, path: str, base_path: str, mapping: Dict):
        current_ts = path_last_modified(path)
        rel_path = os.path.relpath(path, base_path)
        data = mapping.get(rel_path)
        if data:
            if current_ts > data.ts:
                mapping[rel_path] = PathData(base_path, current_ts, self.PUT)
            else:
                mapping[rel_path] = PathData(base_path, data.ts, self.NOOP)
        else:
            mapping[rel_path] = PathData(base_path, current_ts, self.PUT)
        return mapping

    def sync_file(self, path: str, base_path: str):
        self._file_mapping = self._sync_path(path, base_path, self._file_mapping)

    def sync_dir(self, path: str, base_path: str):
        self._dir_mapping = self._sync_path(path, base_path, self._dir_mapping)

    def init(self):
        self._dir_mapping = {
            p: PathData(d.base, d.ts, self.RM) for p, d in self._dir_mapping.items()
        }
        self._file_mapping = {
            p: PathData(d.base, d.ts, self.RM) for p, d in self._file_mapping.items()
        }

    def sync(self, path: str, exclude: List[str] = None):
        files, dirs = get_files_and_dirs_in_path(
            path, exclude=exclude, collect_dirs=True
        )
        base_path, prefix_path = os.path.split(path)
        for file_path in files:
            self.sync_file(os.path.join(prefix_path, file_path), base_path=base_path)

        for dir_path in dirs:
            self.sync_dir(os.path.join(prefix_path, dir_path), base_path=base_path)

    def _get_mapping_by_op(self, mapping: Dict, op: str):
        return {(p.base, k) for k, p in mapping.items() if p.op == op}

    def _clean_by_op(self, mapping: Dict, op: str):
        return {k: p for k, p in mapping.items() if p.op != op}

    def get_files_to_put(self):
        return self._get_mapping_by_op(self._file_mapping, self.PUT)

    def get_files_to_rm(self):
        results = self._get_mapping_by_op(self._file_mapping, self.RM)
        self._file_mapping = self._clean_by_op(self._file_mapping, self.RM)
        return results

    def get_dirs_to_put(self):
        return self._get_mapping_by_op(self._dir_mapping, self.PUT)

    def get_dirs_to_rm(self):
        results = self._get_mapping_by_op(self._dir_mapping, self.RM)
        self._file_mapping = self._clean_by_op(self._file_mapping, self.RM)
        return results
