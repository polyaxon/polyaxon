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

from polyaxon.containers.names import (
    MAIN_JOB_CONTAINER,
    PYTORCHJOBS_CONTAINER,
    TFJOBS_CONTAINER,
)
from polyaxon.k8s.custom_resources import operation
from polyaxon.polyflow import V1RunKind


class BaseMixin:
    SPEC_KIND = operation.KIND
    API_VERSION = operation.API_VERSION
    PLURAL = operation.PLURAL
    GROUP = operation.GROUP
    K8S_LABELS_PART_OF = "polyaxon-runs"


class JobMixin(BaseMixin):
    K8S_LABELS_NAME = V1RunKind.JOB
    K8S_LABELS_COMPONENT = "polyaxon-jobs"
    MAIN_CONTAINER_ID = MAIN_JOB_CONTAINER


class NotifierMixin(BaseMixin):
    K8S_LABELS_NAME = V1RunKind.NOTIFIER
    K8S_LABELS_COMPONENT = "polyaxon-notifiers"
    MAIN_CONTAINER_ID = MAIN_JOB_CONTAINER


class ServiceMixin(BaseMixin):
    K8S_LABELS_NAME = V1RunKind.SERVICE
    K8S_LABELS_COMPONENT = "polyaxon-services"
    MAIN_CONTAINER_ID = MAIN_JOB_CONTAINER


class TFJobMixin(BaseMixin):
    K8S_LABELS_NAME = V1RunKind.TFJOB
    K8S_LABELS_COMPONENT = "polyaxon-tfjobs"
    MAIN_CONTAINER_ID = TFJOBS_CONTAINER


class PytorchJobMixin(BaseMixin):
    K8S_LABELS_NAME = V1RunKind.PYTORCHJOB
    K8S_LABELS_COMPONENT = "polyaxon-pytorch-jobs"
    MAIN_CONTAINER_ID = PYTORCHJOBS_CONTAINER


class MPIJobMixin(BaseMixin):
    K8S_LABELS_NAME = V1RunKind.MPIJOB
    K8S_LABELS_COMPONENT = "polyaxon-mpi-jobs"
    MAIN_CONTAINER_ID = MAIN_JOB_CONTAINER


MIXIN_MAPPING = {
    V1RunKind.NOTIFIER: NotifierMixin,
    V1RunKind.JOB: JobMixin,
    V1RunKind.SERVICE: ServiceMixin,
    V1RunKind.TFJOB: TFJobMixin,
    V1RunKind.PYTORCHJOB: PytorchJobMixin,
    V1RunKind.MPIJOB: MPIJobMixin,
}
