#!/usr/bin/python
#
# Copyright 2019 Polyaxon, Inc.
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

# coding: utf-8
from polyaxon_sdk import V1ConnectionKind


class ConnectionKind(V1ConnectionKind):
    VALUES = {
        V1ConnectionKind.HOST_PATH,
        V1ConnectionKind.VOLUME_CLAIM,
        V1ConnectionKind.FTP,
        V1ConnectionKind.GCP,
        V1ConnectionKind.GCS,
        V1ConnectionKind.GCPCLOUDSQL,
        V1ConnectionKind.GRPC,
        V1ConnectionKind.HDFS,
        V1ConnectionKind.HTTP,
        V1ConnectionKind.PIG_CLI,
        V1ConnectionKind.HIVE_CLI,
        V1ConnectionKind.HIVE_METASTORE,
        V1ConnectionKind.HIVE_SERVER2,
        V1ConnectionKind.JDBC,
        V1ConnectionKind.JENKINS,
        V1ConnectionKind.MYSQL,
        V1ConnectionKind.POSTGRES,
        V1ConnectionKind.ORACLE,
        V1ConnectionKind.VERTICA,
        V1ConnectionKind.SQLITE,
        V1ConnectionKind.MSSQL,
        V1ConnectionKind.REDIS,
        V1ConnectionKind.PRESTO,
        V1ConnectionKind.MONGO,
        V1ConnectionKind.CASSANDRA,
        V1ConnectionKind.SAMBA,
        V1ConnectionKind.AWS,
        V1ConnectionKind.S3,
        V1ConnectionKind.EMR,
        V1ConnectionKind.SNOWFLAKE,
        V1ConnectionKind.SSH,
        V1ConnectionKind.CLOUDANT,
        V1ConnectionKind.DATABRICKS,
        V1ConnectionKind.SEGMENT,
        V1ConnectionKind.AZURE_DATA_LAKE,
        V1ConnectionKind.AZURE_COSMOS,
        V1ConnectionKind.WASB,
        V1ConnectionKind.GIT,
        V1ConnectionKind.REGISTRY,
    }

    MOUNT_VALUES = {V1ConnectionKind.HOST_PATH, V1ConnectionKind.VOLUME_CLAIM}

    BLOB_VALUES = {V1ConnectionKind.GCS, V1ConnectionKind.S3, V1ConnectionKind.WASB}

    ARTIFACT_VALUES = BLOB_VALUES | MOUNT_VALUES

    @classmethod
    def is_blob(cls, kind):
        return kind in cls.BLOB_VALUES

    @classmethod
    def is_mount(cls, kind):
        return kind in cls.MOUNT_VALUES

    @classmethod
    def is_artifact(cls, kind):
        return kind in cls.ARTIFACT_VALUES

    @classmethod
    def is_git(cls, kind):
        return kind == cls.GIT

    @classmethod
    def is_registry(cls, kind):
        return kind == cls.REGISTRY

    @classmethod
    def is_s3(cls, kind):
        return kind == cls.S3

    @classmethod
    def is_wasb(cls, kind):
        return kind == cls.WASB

    @classmethod
    def is_gcs(cls, kind):
        return kind == cls.GCS
