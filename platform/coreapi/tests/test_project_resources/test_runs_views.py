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

import json
import pytest

from unittest.mock import patch

from rest_framework import status

from coredb.api.artifacts.queries import project_runs_artifacts
from coredb.api.artifacts.serializers import RunArtifactLightSerializer
from coredb.api.project_resources.serializers import (
    OperationCreateSerializer,
    RunSerializer,
)
from coredb.factories.artifacts import ArtifactFactory
from coredb.factories.projects import ProjectFactory
from coredb.factories.runs import RunFactory
from coredb.managers.statuses import new_run_status
from coredb.models.artifacts import Artifact, ArtifactLineage
from coredb.models.runs import Run
from polyaxon.api import API_V1
from polyaxon.lifecycle import V1StatusCondition, V1Statuses
from polyaxon.polyboard.artifacts import V1ArtifactKind
from polyaxon.polyflow import V1CloningKind, V1RunKind
from polycommon.celery.tasks import CoreSchedulerCeleryTasks
from tests.base.case import BaseTest


@pytest.mark.projects_resources_mark
class TestProjectRunsTagViewV1(BaseTest):
    model_class = Run
    factory_class = RunFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.objects = []
        self.objects.append(
            self.factory_class(
                project=self.project,
                user=self.user,
                tags=["tag11"],
            )
        )
        self.objects.append(
            self.factory_class(
                project=self.project,
                user=self.user,
                tags=["new", "tag21", "tag22"],
            )
        )
        self.objects.append(self.factory_class(project=self.project, user=self.user))
        self.objects.append(self.factory_class(project=self.project, user=self.user))
        self.url = "/{}/{}/{}/runs/tag/".format(
            API_V1, self.user.username, self.project.name
        )
        self.queryset = self.model_class.objects.filter(project=self.project).order_by(
            "created_at"
        )

    def test_tag(self):
        data = {
            "uuids": [
                self.objects[0].uuid.hex,
                self.objects[1].uuid.hex,
                self.objects[2].uuid.hex,
            ],
            "tags": ["new", "tags"],
        }
        assert [
            set(i) if i else i for i in self.queryset.values_list("tags", flat=True)
        ] == [{"tag11"}, {"new", "tag21", "tag22"}, None, None]
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert [
            set(i) if i else i for i in self.queryset.values_list("tags", flat=True)
        ] == [
            {"tag11", "new", "tags"},
            {"new", "tag21", "tag22", "tags"},
            {"new", "tags"},
            None,
        ]


@pytest.mark.projects_resources_mark
class TestProjectRunsStopViewV1(BaseTest):
    model_class = Run
    factory_class = RunFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.objects = [
            self.factory_class(project=self.project, user=self.user) for _ in range(4)
        ]
        self.url = "/{}/{}/{}/runs/stop/".format(
            API_V1, self.user.username, self.project.name
        )

    @patch("polycommon.workers.send")
    def test_stop(self, _):
        for obj in self.objects:
            obj.status = V1Statuses.RUNNING
            obj.save()
        data = {"uuids": [self.objects[0].uuid.hex, self.objects[1].uuid.hex]}
        assert set(Run.objects.only("status").values_list("status", flat=True)) == {
            V1Statuses.RUNNING
        }
        with patch("polycommon.auditor.record") as auditor_record:
            resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert set(Run.objects.only("status").values_list("status", flat=True)) == {
            V1Statuses.STOPPING,
            V1Statuses.RUNNING,
        }

        assert auditor_record.call_count == 2

    @patch("polycommon.workers.send")
    def test_safe_stop(self, _):
        self.objects[0].status = V1Statuses.QUEUED
        self.objects[0].save()
        self.objects[1].status = V1Statuses.COMPILED
        self.objects[1].save()
        data = {"uuids": [self.objects[0].uuid.hex, self.objects[1].uuid.hex]}
        assert set(Run.objects.only("status").values_list("status", flat=True)) == {
            V1Statuses.QUEUED,
            V1Statuses.COMPILED,
            V1Statuses.CREATED,
        }
        with patch("polycommon.auditor.record") as auditor_record:
            resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert set(Run.objects.only("status").values_list("status", flat=True)) == {
            V1Statuses.STOPPED,
            V1Statuses.STOPPING,
            V1Statuses.CREATED,
        }

        assert auditor_record.call_count == 1


@pytest.mark.projects_resources_mark
class TestProjectRunsApproveViewV1(BaseTest):
    model_class = Run
    factory_class = RunFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.objects = [
            self.factory_class(project=self.project, user=self.user, is_approved=False)
            for _ in range(4)
        ]
        self.url = "/{}/{}/{}/runs/approve/".format(
            API_V1, self.user.username, self.project.name
        )

    @patch("polycommon.workers.send")
    def test_approve(self, workers_send):
        data = {"uuids": [self.objects[0].uuid.hex, self.objects[1].uuid.hex]}
        assert set(
            Run.objects.only("is_approved").values_list("is_approved", flat=True)
        ) == {False}
        with patch("polycommon.auditor.record") as auditor_record:
            resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert set(
            Run.objects.only("is_approved").values_list("is_approved", flat=True)
        ) == {True}
        assert auditor_record.call_count == 2


@pytest.mark.projects_resources_mark
class TestProjectRunsDeleteViewV1(BaseTest):
    model_class = Run
    factory_class = RunFactory
    HAS_AUTH = True

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.objects = [
            self.factory_class(project=self.project, user=self.user) for _ in range(3)
        ]

        self.url = "/{}/{}/{}/runs/delete/".format(
            API_V1, self.user.username, self.project.name
        )

    def test_delete_auditor(self):
        data = {"uuids": [self.objects[0].uuid.hex, self.objects[1].uuid.hex]}
        assert Run.objects.count() == 3
        with patch("polycommon.auditor.record") as auditor_record:
            resp = self.client.delete(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert Run.objects.count() == 1
        assert Run.all.count() == 3
        assert auditor_record.call_count == 2

    def test_delete_worker_send(self):
        data = {"uuids": [self.objects[0].uuid.hex, self.objects[1].uuid.hex]}
        assert Run.objects.count() == 3
        with patch("polycommon.workers.send") as workers_send:
            resp = self.client.delete(self.url, data)
        assert resp.status_code == status.HTTP_200_OK
        assert Run.objects.count() == 1
        assert Run.all.count() == 3
        assert workers_send.call_count == 2
        assert {c[0][0] for c in workers_send.call_args_list} == {
            CoreSchedulerCeleryTasks.RUNS_DELETE,
        }


@pytest.mark.projects_resources_mark
class TestProjectRunsArtifactsViewV1(BaseTest):
    serializer_class = RunArtifactLightSerializer
    model_class = Artifact
    factory_class = ArtifactFactory
    queryset = project_runs_artifacts
    num_objects = 3

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()
        self.objects = [
            RunFactory(project=self.project, user=self.user) for _ in range(3)
        ]
        self.url = "/{}/polyaxon/{}/runs/artifacts_lineage/".format(
            API_V1,
            self.project.name,
        )
        obj = self.factory_class(name="in1", state=self.project.uuid)
        ArtifactLineage.objects.create(run=self.objects[0], artifact=obj)
        ArtifactLineage.objects.create(run=self.objects[1], artifact=obj)
        obj = self.factory_class(name="in2", state=self.project.uuid)
        ArtifactLineage.objects.create(run=self.objects[0], artifact=obj)
        obj = self.factory_class(name="out1", state=self.project.uuid)
        ArtifactLineage.objects.create(
            run=self.objects[0],
            artifact=obj,
            is_input=False,
        )

        self.query = self.queryset.filter(run__project=self.project)

    def test_get(self):
        resp = self.client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == 3

        resp = self.client.get(self.url + "?query=run:{}".format(self.objects[1].uuid))
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == 1

        resp = self.client.get(
            self.url
            + "?query=run:{}".format(
                "|".join([self.objects[0].uuid.hex, self.objects[1].uuid.hex])
            )
        )
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == 3

        data = resp.data["results"]
        assert len(data) == self.query.count()
        assert data == self.serializer_class(self.query, many=True).data

    @pytest.mark.filterwarnings("ignore::RuntimeWarning")
    def test_get_filter(self):  # pylint:disable=too-many-statements
        # Name
        resp = self.client.get(self.url + "?query=name:in1")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 1

        resp = self.client.get(self.url + "?query=name:out1")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 1

        resp = self.client.get(self.url + "?query=name:out3")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 0

        # Kind
        resp = self.client.get(self.url + f"?query=kind:{V1ArtifactKind.METRIC}")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 3

        resp = self.client.get(self.url + f"?query=kind:{V1ArtifactKind.HISTOGRAM}")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 0


@pytest.mark.projects_resources_mark
class TestProjectRunListViewV1(BaseTest):
    serializer_class = RunSerializer
    model_class = Run
    factory_class = RunFactory
    num_objects = 3

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()

        self.url = "/{}/polyaxon/{}/runs/".format(API_V1, self.project.name)
        self.objects = [
            self.factory_class(project=self.project, user=self.user)
            for _ in range(self.num_objects)
        ]
        self.queryset = self.model_class.objects.filter(project=self.project).order_by(
            "-updated_at"
        )
        # one object that does not belong to the filter
        self.other_project = ProjectFactory()
        self.other_url = "/{}/polyaxon/{}/runs/".format(API_V1, self.other_project.name)
        self.other_object = self.factory_class(
            project=self.other_project,
        )

    def test_get(self):
        resp = self.client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == len(self.objects)

        data = resp.data["results"]
        assert len(data) == self.queryset.count()
        assert data == self.serializer_class(self.queryset, many=True).data

        # Test other
        resp = self.client.get(self.other_url)
        assert resp.status_code == status.HTTP_200_OK
        data = resp.data["results"]
        assert len(data) == 1

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

    def test_get_order(self):
        resp = self.client.get(self.url + "?sort=created_at,updated_at")
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == len(self.objects)

        data = resp.data["results"]
        assert len(data) == self.queryset.count()
        assert data != self.serializer_class(self.queryset, many=True).data
        assert (
            data
            == self.serializer_class(
                self.queryset.order_by("created_at", "updated_at"), many=True
            ).data
        )

        resp = self.client.get(self.url + "?sort=-started_at")
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == len(self.objects)

        data = resp.data["results"]
        assert len(data) == self.queryset.count()
        assert (
            data
            == self.serializer_class(
                self.queryset.order_by("-started_at"), many=True
            ).data
        )

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

        resp = self.client.get(
            self.url + "?query=created_at:>=2010-01-01,status:Finished"
        )
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == 0

        resp = self.client.get(
            self.url + "?query=created_at:>=2010-01-01,status:created|running"
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
            + "?query=uuid:{}|{}".format(
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

        resp = self.client.get(
            self.url + "?query=project.name:{}".format(self.project.name)
        )
        assert resp.data["next"] is None
        assert resp.data["count"] == len(self.objects)

        # Archived
        resp = self.client.get(self.url + "?query=live_state:0")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 0

        # Set metrics
        optimizers = ["sgd", "sgd", "adam"]
        tags = [["tag1"], ["tag1", "tag2"], ["tag2"]]
        losses = [0.1, 0.2, 0.9]
        for i, obj in enumerate(self.objects[:3]):
            obj.outputs = {"loss": losses[i]}
            obj.inputs = {"optimizer": optimizers[i]}
            obj.tags = tags[i]
            obj.save()

        resp = self.client.get(
            self.url + "?query=created_at:>=2010-01-01,"
            "params.optimizer:sgd,"
            "metrics.loss:>=0.2,"
            "tags:tag1"
        )
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == 1

        # Test that metrics works as well
        resp = self.client.get(
            self.url + "?query=created_at:>=2010-01-01,"
            "params.optimizer:sgd,"
            "metrics.loss:>=0.2,"
            "tags:tag1"
        )
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == 1

        resp = self.client.get(
            self.url + "?query=created_at:>=2010-01-01,"
            "params.optimizer:sgd|adam,"
            "metrics.loss:>=0.2,"
            "tags:tag1|tag2"
        )
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == 2

        # Order by metrics
        resp = self.client.get(self.url + "?sort=-metrics.loss")
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == len(self.objects)

        data = resp.data["results"]
        assert len(data) == self.queryset.count()
        assert data == [
            self.serializer_class(obj).data for obj in reversed(self.objects)
        ]

        resp = self.client.get(self.url + "?sort=metrics.loss")
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == len(self.objects)

        data = resp.data["results"]
        assert len(data) == self.queryset.count()
        assert data == [self.serializer_class(obj).data for obj in self.objects]

        # Order by metrics
        resp = self.client.get(self.url + "?sort=-metrics.loss")
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == len(self.objects)

        data = resp.data["results"]
        assert len(data) == self.queryset.count()
        assert data == [
            self.serializer_class(obj).data for obj in reversed(self.objects)
        ]

        resp = self.client.get(self.url + "?sort=metrics.loss")
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == len(self.objects)

        data = resp.data["results"]
        assert len(data) == self.queryset.count()
        assert data == [self.serializer_class(obj).data for obj in self.objects]

        # Order by params
        resp = self.client.get(self.url + "?sort=-params.optimizer")
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == len(self.objects)

        data = resp.data["results"]
        assert len(data) == self.queryset.count()
        assert data[0]["inputs"]["optimizer"] > data[-1]["inputs"]["optimizer"]

        resp = self.client.get(self.url + "?sort=params.optimizer")
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == len(self.objects)

        data = resp.data["results"]
        assert len(data) == self.queryset.count()
        assert data[0]["inputs"]["optimizer"] < data[-1]["inputs"]["optimizer"]

        # Artifacts
        resp = self.client.get(
            self.url + "?query=in_artifact_kind:{}".format(V1ArtifactKind.METRIC)
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 0

        resp = self.client.get(
            self.url + "?query=in_artifact_kind:~{}".format(V1ArtifactKind.METRIC)
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == len(self.objects)

        # Add meta
        self.objects[0].meta_info = {"has_events": True, "kind": V1RunKind.JOB}
        self.objects[0].save()
        self.objects[1].meta_info = {"has_tensorboard": True, "kind": V1RunKind.SERVICE}
        self.objects[1].save()

        resp = self.client.get(self.url + "?query=meta_flags.has_events:1")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 1

        resp = self.client.get(self.url + "?query=meta_flags.has_tensorboard:1")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 1

        resp = self.client.get(
            self.url + "?query=meta_info.kind:{}".format(V1RunKind.JOB)
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 1

        resp = self.client.get(
            self.url + "?query=meta_info.kind:~{}".format(V1RunKind.SERVICE)
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 1

        # Add artifacts
        obj = ArtifactFactory(name="m1", state=self.project.uuid)
        ArtifactLineage.objects.create(run=self.objects[0], artifact=obj, is_input=True)
        obj = ArtifactFactory(
            name="in1",
            state=self.project.uuid,
            kind=V1ArtifactKind.DOCKERFILE,
        )
        ArtifactLineage.objects.create(
            run=self.objects[0], artifact=obj, is_input=False
        )
        obj = ArtifactFactory(name="m2", state=self.project.uuid)
        ArtifactLineage.objects.create(run=self.objects[1], artifact=obj)

        resp = self.client.get(
            self.url + "?query=in_artifact_kind:{}".format(V1ArtifactKind.METRIC)
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 1

        resp = self.client.get(
            self.url + "?query=in_artifact_kind:~{}".format(V1ArtifactKind.METRIC)
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == len(self.objects) - 1

        resp = self.client.get(
            self.url + "?query=out_artifact_kind:{}".format(V1ArtifactKind.METRIC)
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 1

        resp = self.client.get(
            self.url + "?query=in_artifact_kind:{}".format(V1ArtifactKind.DOCKERFILE)
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 0

        resp = self.client.get(
            self.url + "?query=out_artifact_kind:{}".format(V1ArtifactKind.DOCKERFILE)
        )
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 0

        # Add commit
        resp = self.client.get(self.url + "?query=commit:commit1")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 0

        resp = self.client.get(self.url + "?query=commit:~commit1")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == len(self.objects)

        obj = ArtifactFactory(
            name="commit1",
            state=self.project.uuid,
            kind=V1ArtifactKind.CODEREF,
        )
        ArtifactLineage.objects.create(
            run=self.objects[0], artifact=obj, is_input=False
        )

        resp = self.client.get(self.url + "?query=commit:commit1")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == 1

        resp = self.client.get(self.url + "?query=commit:~commit1")
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["next"] is None
        assert resp.data["count"] == len(self.objects) - 1

    def test_get_runs_for_original(self):
        self.factory_class(
            project=self.project,
            user=self.user,
            cloning_kind=V1CloningKind.CACHE,
            original=self.objects[0],
        )
        self.factory_class(
            project=self.project,
            user=self.user,
            cloning_kind=V1CloningKind.RESTART,
            original=self.objects[0],
        )
        resp = self.client.get(
            self.url + f"?query=original.uuid:{self.objects[0].uuid.hex}"
        )
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == 2

        resp = self.client.get(self.url + f"?query=cloning_kind:cache")
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == 1

        resp = self.client.get(self.url + f"?query=cloning_kind:cache")
        assert resp.status_code == status.HTTP_200_OK

        assert resp.data["next"] is None
        assert resp.data["count"] == 1

    def test_get_filter_pagination(self):
        limit = self.num_objects - 1
        resp = self.client.get(
            "{}?limit={}&{}".format(
                self.url, limit, "?query=created_at:>=2010-01-01,status:created|running"
            )
        )
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


@pytest.mark.projects_resources_mark
class TestProjectRunCreateViewV1(BaseTest):
    serializer_class = OperationCreateSerializer
    model_class = Run
    factory_class = RunFactory
    num_objects = 3

    def setUp(self):
        super().setUp()
        self.project = ProjectFactory()

        self.url = "/{}/polyaxon/{}/runs/".format(API_V1, self.project.name)

    def test_create_is_managed_and_and_meta(self):
        data = {"is_managed": False}
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        xp = Run.objects.last()
        assert xp.is_managed is False
        assert xp.is_approved is True

        data = {"is_managed": False, "is_approved": False}
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        xp = Run.objects.last()
        assert xp.is_managed is False
        assert xp.is_approved is True  # Since it's not managed

        data = {"is_managed": False, "is_approved": True}
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        xp = Run.objects.last()
        assert xp.is_managed is False
        assert xp.is_approved is True

        data = {"is_managed": False, "meta_info": {"foo": "bar"}}
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_201_CREATED
        xp = Run.objects.last()
        assert xp.is_managed is False
        assert xp.is_approved is True
        assert xp.meta_info == {"foo": "bar"}

    def test_create_with_invalid_config(self):
        data = {"content": "bar"}
        resp = self.client.post(self.url, data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_create(self):
        resp = self.client.post(self.url)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

        data = {"is_managed": False}
        with patch("polycommon.auditor.record") as auditor_record:
            resp = self.client.post(self.url, data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert auditor_record.call_count == 1
        assert Run.objects.count() == 1

    def test_create_op(self):
        data = {
            "content": json.dumps(
                {
                    "version": 1.1,
                    "kind": "operation",
                    "name": "foo",
                    "description": "a description",
                    "tags": ["tag1", "tag2"],
                    "trigger": "all_succeeded",
                    "component": {
                        "name": "service-template",
                        "tags": ["backend", "lab"],
                        "run": {
                            "kind": V1RunKind.JOB,
                            "container": {"image": "test"},
                            "init": [{"connection": "foo", "git": {"revision": "dev"}}],
                        },
                    },
                }
            )
        }
        with patch("polycommon.auditor.record") as auditor_record:
            resp = self.client.post(self.url, data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert auditor_record.call_count == 1
        assert Run.objects.count() == 1
        last_run = Run.objects.last()
        assert last_run.is_managed is True
        assert last_run.is_approved is True

        # Meta and is_approved
        data["is_approved"] = False
        data["meta_info"] = {"test": "works"}
        with patch("polycommon.auditor.record") as auditor_record:
            resp = self.client.post(self.url, data)

        assert resp.status_code == status.HTTP_201_CREATED
        assert auditor_record.call_count == 2
        assert Run.objects.count() == 2
        last_run = Run.objects.last()
        assert last_run.is_managed is True
        assert last_run.is_approved is False
        assert last_run.meta_info == {"test": "works"}
