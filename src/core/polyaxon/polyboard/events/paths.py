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


def get_resource_path(run_path: str, kind: str = None, name: str = None) -> str:
    _path = "{}/resources".format(run_path)
    if kind:
        _path = "{}/{}".format(_path, kind)
    if name:
        _path = "{}/{}.plx".format(_path, name)

    return _path


def get_event_path(run_path: str, kind: str = None, name: str = None) -> str:
    _path = "{}/events".format(run_path)
    if kind:
        _path = "{}/{}".format(_path, kind)
    if name:
        _path = "{}/{}.plx".format(_path, name)

    return _path


def get_event_assets_path(run_path: str, kind: str = None) -> str:
    _path = "{}/assets".format(run_path)
    if kind:
        _path = "{}/{}".format(_path, kind)
    return _path


def get_asset_path(
    run_path: str, kind: str = None, name: str = None, step: int = None, ext=None
) -> str:
    _path = get_event_assets_path(run_path, kind)
    if name:
        _path = "{}/{}".format(_path, name)
    if step is not None:
        _path = "{}_{}".format(_path, step)
    if ext:
        _path = "{}.{}".format(_path, ext)

    return _path
