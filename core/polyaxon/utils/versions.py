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


def clean_version_for_compatibility(version: str):
    return "-".join(version.lstrip("v").replace(".", "-").split("-")[:3])


def clean_version_for_check(version: str):
    if not version:
        return version
    return ".".join(version.lstrip("v").replace("-", ".").split(".")[:3])


def compare_versions(current: str, reference: str, comparator: str) -> bool:

    from distutils.version import LooseVersion

    current = LooseVersion(current)
    reference = LooseVersion(reference)

    if comparator == "=":
        return current == reference

    if comparator == "!=":
        return current != reference

    if comparator == "<":
        return current < reference

    if comparator == "<=":
        return current <= reference

    if comparator == ">":
        return current > reference

    if comparator == ">=":
        return current >= reference

    raise ValueError("Comparator `{}` is not supported.".format(comparator))
