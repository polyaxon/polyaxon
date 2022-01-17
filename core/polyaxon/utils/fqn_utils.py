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

import re
import unicodedata

from polyaxon.exceptions import PolyaxonSchemaError


def get_project_instance(owner: str, project: str) -> str:
    return "{}.{}".format(owner, project)


def get_run_instance(owner: str, project: str, run_uuid: str) -> str:
    return "{}.{}.runs.{}".format(owner, project, run_uuid)


def get_cleaner_instance(owner: str, project: str, run_uuid: str) -> str:
    return "{}.{}.cleaners.{}".format(owner, project, run_uuid)


def get_resource_name(run_uuid: str) -> str:
    return "plx-operation-{}".format(run_uuid)


def get_cleaner_resource_name(run_uuid: str) -> str:
    return "plx-cleaner-{}".format(run_uuid)


def get_resource_name_for_kind(run_uuid: str, run_kind: str = None) -> str:
    if run_kind == "cleaner":
        return get_cleaner_resource_name(run_uuid)
    # Operation
    return get_resource_name(run_uuid)


def to_fqn_name(name: str) -> str:
    if not name:
        raise ValueError("A name is required to process events.")

    value = str(name)
    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub(r"[^\w\\\/\.\s-]", "", value).strip()
    value = re.sub(r"[\\\/]+", "__", value)
    value = re.sub(r"[-\.\s]+", "-", value)
    return value


def get_entity_full_name(owner: str = None, entity: str = None) -> str:
    if owner and entity:
        return "{}/{}".format(owner, entity)
    return entity


def get_entity_info(entity):
    if not entity:
        raise PolyaxonSchemaError(
            "Received an invalid entity reference: `{}`".format(entity)
        )

    parts = entity.replace(".", "/").split("/")
    if len(parts) > 2:
        raise PolyaxonSchemaError(
            "Received an invalid entity reference: `{}`".format(entity)
        )
    if len(parts) == 2:
        owner, entity_name = parts
    else:
        owner = None
        entity_name = entity

    return owner, entity_name
