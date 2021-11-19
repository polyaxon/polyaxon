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

from polyaxon.polypod.custom_resources.job import get_job_custom_resource
from polyaxon.polypod.custom_resources.kubeflow import (
    get_mpi_job_custom_resource,
    get_mx_job_custom_resource,
    get_pytorch_job_custom_resource,
    get_tf_job_custom_resource,
    get_xgb_job_custom_resource,
)
from polyaxon.polypod.custom_resources.service import get_service_custom_resource
