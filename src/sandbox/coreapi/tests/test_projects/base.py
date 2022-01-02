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

from coredb.factories.projects import ProjectFactory
from coredb.factories.runs import RunFactory
from coredb.factories.users import UserFactory
from coredb.models.projects import Project
from polyaxon.api import API_V1
from tests.base.case import BaseTest


class BaseTestProjectApi(BaseTest):
    model_class = Project
    factory_class = ProjectFactory

    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.project = self.factory_class()
        self.url = "/{}/{}/{}/".format(API_V1, self.user.username, self.project.name)
        self.queryset = self.model_class.objects.filter()
        self.object_query = self.model_class.objects.get(id=self.project.id)

        # Create related fields
        for _ in range(2):
            RunFactory(user=self.user, project=self.project)
