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


class OptionOwners(namedtuple("OptionOwners", "user project team organization")):
    @classmethod
    def get_owners(
        cls,
        user: int = None,
        project: int = None,
        team: int = None,
        organization: int = None,
    ) -> "OptionOwners":
        return cls(user=user, project=project, team=team, organization=organization)

    def to_dict(self):
        return dict(self._asdict())

    def __eq__(self, other):
        return (
            self.user == other.user
            and self.project == other.project
            and self.team == other.team
            and self.organization == other.organization
        )

    def __str__(self):
        return uuid.uuid5(
            namespace=uuid.NAMESPACE_DNS,
            name=f"user<{self.user}>:"
            f"project<{self.project}>:"
            f"team<{self.team}>:"
            f"organization<{self.organization}>",
        ).hex
