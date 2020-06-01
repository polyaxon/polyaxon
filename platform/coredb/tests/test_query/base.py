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

from django.test import TestCase

from coredb.factories.projects import ProjectFactory
from coredb.factories.runs import RunFactory
from coredb.factories.users import UserFactory
from coredb.models.owners import Owner


class BaseTestQuery(TestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.owner = Owner.objects.filter(name=self.user.username).last()
        self.project = ProjectFactory(owner_id=self.owner.id)
        self.run = RunFactory(project=self.project)
