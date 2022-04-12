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

import pytest

from flaky import flaky

from rest_framework import status

from coredb.api.projects.serializers import (
    ProjectDetailSerializer,
    ProjectNameSerializer,
    ProjectSerializer,
)
from coredb.factories.projects import ProjectFactory
from coredb.factories.runs import RunFactory
from coredb.models.projects import Project
from coredb.models.runs import Run
from polyaxon.api import API_V1
from tests.base.case import BaseTest
from tests.test_projects.base import BaseTestProjectApi


@pytest.mark.projects_mark
class TestProjectCreateViewV1(BaseTest):
    serializer_class = ProjectSerializer
    model_class = Project
    factory_class = ProjectFactory

    def setUp(self):
        super().setUp()
        self.url = self.get_url()

    def get_url(self):
        return "/{}/polyaxon/projects/create".format(API_V1)

    def test_create(self):
        num_objects = self.model_class.objects.count()
        data = {}
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        data = {"name": "new_project"}

        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert self.model_class.objects.count() == num_objects + 1
        last_obj = self.model_class.objects.last()
        assert last_obj.name == "new_project"


@pytest.mark.projects_mark
class TestProjectListViewV1(BaseTest):
    serializer_class = ProjectSerializer
    model_class = Project
    factory_class = ProjectFactory
    num_objects = 3

    def setUp(self):
        super().setUp()
        self.url = "/{}/{}/projects/list/".format(API_V1, self.user.username)
        self.objects = [self.factory_class() for _ in range(self.num_objects)]
        self.queryset = self.model_class.objects.filter().order_by("-updated_at")

    def test_get(self):
        resp = self.client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == len(self.objects)

        data = resp.data["results"]
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

    @flaky(max_runs=3)
    def test_pagination(self):
        limit = self.num_objects - 1
        resp = self.client.get("{}?limit={}".format(self.url, limit))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get("next")
        assert next_page is not None
        assert resp.data["count"] == self.queryset.count()

        data = resp.data["results"]
        assert len(data) == limit
        assert data == self.serializer_class(self.queryset[:limit], many=True).data

        resp = self.client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None

        data = resp.data["results"]
        assert len(data) == 1
        assert data == self.serializer_class(self.queryset[limit:], many=True).data

    def test_get_order_pagination(self):
        queryset = self.queryset.order_by("created_at", "updated_at")
        limit = self.num_objects - 1
        resp = self.client.get(
            "{}?limit={}&{}".format(self.url, limit, "sort=created_at,updated_at")
        )
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get("next")
        assert next_page is not None
        assert resp.data["count"] == queryset.count()

        data = resp.data["results"]
        assert len(data) == limit
        assert data == self.serializer_class(queryset[:limit], many=True).data

        resp = self.client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None

        data = resp.data["results"]
        assert len(data) == 1
        assert data == self.serializer_class(queryset[limit:], many=True).data

    @pytest.mark.filterwarnings("ignore::RuntimeWarning")
    def test_get_filter(self):  # pylint:disable=too-many-statements
        # Wrong filter raises
        resp = self.client.get(self.url + "?query=created_at<2010-01-01")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        resp = self.client.get(self.url + "?query=created_at:<2010-01-01")
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == 0

        resp = self.client.get(self.url + "?query=created_at:>=2010-01-01,name:bobobob")
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == 0

        resp = self.client.get(
            self.url
            + "?query=created_at:>=2010-01-01,name:{}".format(
                "|".join([p.name for p in self.objects])
            )
        )
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == len(self.objects)

        data = resp.data["results"]
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

        # Id
        resp = self.client.get(
            self.url
            + "?query=id:{}|{}".format(
                self.objects[0].uuid.hex, self.objects[1].uuid.hex
            )
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 2

        # Name
        self.objects[0].name = "exp_foo"
        self.objects[0].save()

        resp = self.client.get(self.url + "?query=name:exp_foo")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 1

        # Name Regex
        resp = self.client.get(self.url + "?query=name:%foo")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 1

        resp = self.client.get(self.url + "?query=name:{}".format(self.objects[0].name))
        assert resp.data["next"] is None
        assert resp.data["count"] == 1


@pytest.mark.projects_mark
class TestProjectNameListViewV1(BaseTest):
    serializer_class = ProjectNameSerializer
    model_class = Project
    factory_class = ProjectFactory
    num_objects = 3

    def setUp(self):
        super().setUp()
        self.url = "/{}/{}/projects/names/".format(API_V1, self.user.username)
        self.objects = [self.factory_class() for _ in range(self.num_objects)]
        self.queryset = self.model_class.objects.filter()
        self.queryset = self.queryset.order_by("-updated_at")

    def test_get(self):
        resp = self.client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == len(self.objects)

        data = resp.data["results"]
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

    @flaky(max_runs=3)
    def test_pagination(self):
        limit = self.num_objects - 1
        resp = self.client.get("{}?limit={}".format(self.url, limit))
        assert resp.status_code == status.HTTP_200_OK

        next_page = resp.data.get("next")
        assert next_page is not None
        assert resp.data["count"] == self.queryset.count()

        data = resp.data["results"]
        assert len(data) == limit
        assert data == self.serializer_class(self.queryset[:limit], many=True).data

        resp = self.client.get(next_page)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None

        data = resp.data["results"]
        assert len(data) == 1
        assert data == self.serializer_class(self.queryset[limit:], many=True).data


@pytest.mark.projects_mark
class TestProjectDetailViewV1(BaseTestProjectApi):
    serializer_class = ProjectDetailSerializer

    def test_get(self):
        resp = self.client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK
        expected = self.serializer_class(self.object_query).data
        assert resp.data == expected

    def test_patch(self):
        new_tags = ["foo", "bar"]
        new_desc = "foo bar"
        data = {"tags": new_tags, "description": new_desc}
        assert self.project.tags != data["tags"]
        assert self.project.description != new_desc
        resp = self.client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK

        new_object = self.model_class.objects.get(id=self.project.id)
        assert new_object.description != self.project.description
        assert new_object.description == new_desc
        assert new_object.tags != self.project.tags
        assert set(new_object.tags) == set(new_tags)
        assert new_object.runs.count() == 2

        new_name = "updated_project_name"
        data = {"name": new_name}
        assert self.project.name != data["name"]
        resp = self.client.patch(self.url, data=data)
        assert resp.status_code == status.HTTP_200_OK

        new_object = self.model_class.objects.get(id=self.project.id)
        assert new_object.name != self.project.name
        assert new_object.name == new_name
        assert new_object.runs.count() == 2

    def test_delete(self):
        for _ in range(2):
            RunFactory(project=self.project, user=self.user)

        assert self.queryset.count() == 1
        assert Run.objects.count() == 4

        resp = self.client.delete(self.url)
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert self.queryset.count() == 0
        assert Project.all.filter().count() == 0
        assert Run.all.count() == 0
