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

import uuid

from collections import namedtuple


class SuggestionSpec(namedtuple("SuggestionSpec", "params")):
    """A structure that defines an experiment hyperparam suggestion."""

    def __eq__(self, other):
        if self.params.keys() != other.params.keys():
            return False

        for key, value in self.params.items():
            if value != other.params[key]:
                return False

        return True

    def __repr__(self):
        return ",".join(
            ["{}:{}".format(key, val) for (key, val) in sorted(self.params.items())]
        )

    def __hash__(self):
        return hash(self.__repr__())

    def uuid(self):
        return uuid.uuid5(uuid.NAMESPACE_DNS, self.__repr__())
