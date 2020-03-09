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

from marshmallow import fields, validate

from polyaxon.k8s import k8s_schemas
from polyaxon.polyflow.run.kinds import V1RunKind
from polyaxon.polyflow.run.spark.replica import SparkReplicaSchema
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.swagger import SwaggerField


class V1SparkType(polyaxon_sdk.V1SparkType):
    VALUES = {
        polyaxon_sdk.V1SparkType.JAVA,
        polyaxon_sdk.V1SparkType.SCALA,
        polyaxon_sdk.V1SparkType.PYTHON,
        polyaxon_sdk.V1SparkType.R,
    }


class V1SparkDeploy(polyaxon_sdk.SparkDeployMode):
    VALUES = {
        polyaxon_sdk.SparkDeployMode.CLUSTER,
        polyaxon_sdk.SparkDeployMode.CLIENT,
        polyaxon_sdk.SparkDeployMode.IN_CLUSTER_CLIENT,
    }


class SparkSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal(V1RunKind.SPARK))
    connections = fields.List(fields.Str(), allow_none=True)
    volumes = fields.List(SwaggerField(cls=k8s_schemas.V1Volume), allow_none=True)
    type = fields.Str(allow_none=True, validate=validate.OneOf(V1SparkType.VALUES))
    sparkVersion = fields.Str(allow_none=True)
    pythonVersion = fields.Str(
        allow_none=True, validate=validate.OneOf(V1SparkDeploy.VALUES)
    )
    deployMode = fields.Str(allow_none=True)
    main_class = fields.Str(allow_none=True)
    main_application_file = fields.Str(allow_none=True)
    arguments = fields.Str(allow_none=True)
    hadoop_conf = fields.Str(allow_none=True)
    spark_conf = fields.Str(allow_none=True)
    hadoop_config_map = fields.Str(allow_none=True)
    spark_config_map = fields.Str(allow_none=True)
    executor = fields.Nested(SparkReplicaSchema, allow_none=True)
    driver = fields.Nested(SparkReplicaSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return V1Spark


class V1Spark(BaseConfig, polyaxon_sdk.V1Spark):
    SCHEMA = SparkSchema
    IDENTIFIER = V1RunKind.SPARK
    REDUCED_ATTRIBUTES = [
        "kind",
        "connections",
        "volumes",
        "type",
        "sparkVersion",
        "pythonVersion",
        "deployMode",
        "mainClass",
        "mainApplicationFile",
        "arguments",
        "hadoopConf",
        "sparkConf",
        "sparkConfigMap",
        "hadoopConfigMap",
        "executor",
        "driver",
    ]
