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

import datetime

GenericDT = NaiveDT = AwareDT = datetime.datetime

ANY = "any"
INT = "int"
FLOAT = "float"
BOOL = "bool"
STR = "str"
DICT = "dict"
DICT_OF_DICTS = "dict_of_dicts"
URI = "uri"
AUTH = "auth"
LIST = "list"
GCS = "gcs"
S3 = "s3"
WASB = "wasb"
DOCKERFILE = "dockerfile"
GIT = "git"
IMAGE = "image"
EVENT = "event"
ARTIFACTS = "artifacts"
PATH = "path"
METRIC = "metric"
METADATA = "metadata"
DATE = "date"
DATETIME = "datetime"

VALUES = {
    ANY,
    INT,
    FLOAT,
    BOOL,
    STR,
    DICT,
    DICT_OF_DICTS,
    URI,
    AUTH,
    LIST,
    GCS,
    S3,
    WASB,
    DOCKERFILE,
    GIT,
    IMAGE,
    EVENT,
    ARTIFACTS,
    PATH,
    METRIC,
    METADATA,
    DATE,
    DATETIME,
}

LINEAGE_VALUES = {
    GCS,
    S3,
    WASB,
    DOCKERFILE,
    GIT,
    IMAGE,
    EVENT,
    ARTIFACTS,
    PATH,
    METRIC,
    METADATA,
}
