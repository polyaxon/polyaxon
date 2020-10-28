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

import polyaxon_sdk


class V1ConnectionKind(polyaxon_sdk.V1ConnectionKind):
    CHOICES = (
        (
            polyaxon_sdk.V1ConnectionKind.HOST_PATH,
            polyaxon_sdk.V1ConnectionKind.HOST_PATH,
        ),
        (
            polyaxon_sdk.V1ConnectionKind.VOLUME_CLAIM,
            polyaxon_sdk.V1ConnectionKind.VOLUME_CLAIM,
        ),
        (polyaxon_sdk.V1ConnectionKind.GCS, polyaxon_sdk.V1ConnectionKind.GCS),
        (polyaxon_sdk.V1ConnectionKind.S3, polyaxon_sdk.V1ConnectionKind.S3),
        (polyaxon_sdk.V1ConnectionKind.WASB, polyaxon_sdk.V1ConnectionKind.WASB),
        (
            polyaxon_sdk.V1ConnectionKind.REGISTRY,
            polyaxon_sdk.V1ConnectionKind.REGISTRY,
        ),
        (polyaxon_sdk.V1ConnectionKind.GIT, polyaxon_sdk.V1ConnectionKind.GIT),
        (polyaxon_sdk.V1ConnectionKind.AWS, polyaxon_sdk.V1ConnectionKind.AWS),
        (polyaxon_sdk.V1ConnectionKind.GCP, polyaxon_sdk.V1ConnectionKind.GCP),
        (polyaxon_sdk.V1ConnectionKind.AZURE, polyaxon_sdk.V1ConnectionKind.AZURE),
        (polyaxon_sdk.V1ConnectionKind.MYSQL, polyaxon_sdk.V1ConnectionKind.MYSQL),
        (
            polyaxon_sdk.V1ConnectionKind.POSTGRES,
            polyaxon_sdk.V1ConnectionKind.POSTGRES,
        ),
        (polyaxon_sdk.V1ConnectionKind.ORACLE, polyaxon_sdk.V1ConnectionKind.ORACLE),
        (polyaxon_sdk.V1ConnectionKind.VERTICA, polyaxon_sdk.V1ConnectionKind.VERTICA),
        (polyaxon_sdk.V1ConnectionKind.SQLITE, polyaxon_sdk.V1ConnectionKind.SQLITE),
        (polyaxon_sdk.V1ConnectionKind.MSSQL, polyaxon_sdk.V1ConnectionKind.MSSQL),
        (polyaxon_sdk.V1ConnectionKind.REDIS, polyaxon_sdk.V1ConnectionKind.REDIS),
        (polyaxon_sdk.V1ConnectionKind.PRESTO, polyaxon_sdk.V1ConnectionKind.PRESTO),
        (polyaxon_sdk.V1ConnectionKind.MONGO, polyaxon_sdk.V1ConnectionKind.MONGO),
        (
            polyaxon_sdk.V1ConnectionKind.CASSANDRA,
            polyaxon_sdk.V1ConnectionKind.CASSANDRA,
        ),
        (polyaxon_sdk.V1ConnectionKind.FTP, polyaxon_sdk.V1ConnectionKind.FTP),
        (polyaxon_sdk.V1ConnectionKind.GRPC, polyaxon_sdk.V1ConnectionKind.GRPC),
        (polyaxon_sdk.V1ConnectionKind.HDFS, polyaxon_sdk.V1ConnectionKind.HDFS),
        (polyaxon_sdk.V1ConnectionKind.HTTP, polyaxon_sdk.V1ConnectionKind.HTTP),
        (polyaxon_sdk.V1ConnectionKind.PIG_CLI, polyaxon_sdk.V1ConnectionKind.PIG_CLI),
        (
            polyaxon_sdk.V1ConnectionKind.HIVE_CLI,
            polyaxon_sdk.V1ConnectionKind.HIVE_CLI,
        ),
        (
            polyaxon_sdk.V1ConnectionKind.HIVE_METASTORE,
            polyaxon_sdk.V1ConnectionKind.HIVE_METASTORE,
        ),
        (
            polyaxon_sdk.V1ConnectionKind.HIVE_SERVER2,
            polyaxon_sdk.V1ConnectionKind.HIVE_SERVER2,
        ),
        (polyaxon_sdk.V1ConnectionKind.JDBC, polyaxon_sdk.V1ConnectionKind.JDBC),
        (polyaxon_sdk.V1ConnectionKind.JENKINS, polyaxon_sdk.V1ConnectionKind.JENKINS),
        (polyaxon_sdk.V1ConnectionKind.SAMBA, polyaxon_sdk.V1ConnectionKind.SAMBA),
        (
            polyaxon_sdk.V1ConnectionKind.SNOWFLAKE,
            polyaxon_sdk.V1ConnectionKind.SNOWFLAKE,
        ),
        (polyaxon_sdk.V1ConnectionKind.SSH, polyaxon_sdk.V1ConnectionKind.SSH),
        (
            polyaxon_sdk.V1ConnectionKind.CLOUDANT,
            polyaxon_sdk.V1ConnectionKind.CLOUDANT,
        ),
        (
            polyaxon_sdk.V1ConnectionKind.DATABRICKS,
            polyaxon_sdk.V1ConnectionKind.DATABRICKS,
        ),
        (polyaxon_sdk.V1ConnectionKind.SEGMENT, polyaxon_sdk.V1ConnectionKind.SEGMENT),
        (polyaxon_sdk.V1ConnectionKind.SLACK, polyaxon_sdk.V1ConnectionKind.SLACK),
        (polyaxon_sdk.V1ConnectionKind.DISCORD, polyaxon_sdk.V1ConnectionKind.DISCORD),
        (
            polyaxon_sdk.V1ConnectionKind.MATTERMOST,
            polyaxon_sdk.V1ConnectionKind.MATTERMOST,
        ),
        (
            polyaxon_sdk.V1ConnectionKind.PAGERDUTY,
            polyaxon_sdk.V1ConnectionKind.PAGERDUTY,
        ),
        (
            polyaxon_sdk.V1ConnectionKind.HIPCHAT,
            polyaxon_sdk.V1ConnectionKind.HIPCHAT,
        ),
        (polyaxon_sdk.V1ConnectionKind.WEBHOOK, polyaxon_sdk.V1ConnectionKind.WEBHOOK),
        (polyaxon_sdk.V1ConnectionKind.CUSTOM, polyaxon_sdk.V1ConnectionKind.CUSTOM),
    )

    MOUNT_VALUES = {
        polyaxon_sdk.V1ConnectionKind.HOST_PATH,
        polyaxon_sdk.V1ConnectionKind.VOLUME_CLAIM,
    }

    BLOB_VALUES = {
        polyaxon_sdk.V1ConnectionKind.GCS,
        polyaxon_sdk.V1ConnectionKind.S3,
        polyaxon_sdk.V1ConnectionKind.WASB,
    }

    ARTIFACT_VALUES = BLOB_VALUES | MOUNT_VALUES

    HOST_VALUES = {
        polyaxon_sdk.V1ConnectionKind.GIT,
        polyaxon_sdk.V1ConnectionKind.REGISTRY,
    }

    @classmethod
    def is_bucket(cls, kind):
        return kind in cls.BLOB_VALUES

    @classmethod
    def is_mount(cls, kind):
        return kind in cls.MOUNT_VALUES

    @classmethod
    def is_host_path(cls, kind):
        return kind == cls.HOST_PATH

    @classmethod
    def is_volume_claim(cls, kind):
        return kind == cls.VOLUME_CLAIM

    @classmethod
    def is_artifact(cls, kind):
        return kind in cls.ARTIFACT_VALUES

    @classmethod
    def is_git(cls, kind):
        return kind == cls.GIT

    @classmethod
    def is_ssh(cls, kind):
        return kind == cls.SSH

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
