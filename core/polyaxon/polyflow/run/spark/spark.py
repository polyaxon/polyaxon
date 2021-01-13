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

import polyaxon_sdk

from marshmallow import fields, validate

from polyaxon.k8s import k8s_schemas
from polyaxon.polyflow.run.kinds import V1RunKind
from polyaxon.polyflow.run.spark.replica import SparkReplicaSchema
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.swagger import SwaggerField


class V1SparkType(polyaxon_sdk.V1SparkType):
    pass


class V1SparkDeploy(polyaxon_sdk.SparkDeployMode):
    pass


class SparkSchema(BaseCamelSchema):
    kind = fields.Str(allow_none=True, validate=validate.Equal(V1RunKind.SPARK))
    connections = fields.List(fields.Str(), allow_none=True)
    volumes = fields.List(SwaggerField(cls=k8s_schemas.V1Volume), allow_none=True)
    type = fields.Str(
        allow_none=True, validate=validate.OneOf(V1SparkType.allowable_values)
    )
    spark_version = fields.Str(allow_none=True)
    python_version = fields.Str(
        allow_none=True, validate=validate.OneOf(V1SparkDeploy.allowable_values)
    )
    deploy_mode = fields.Str(allow_none=True)
    main_class = fields.Str(allow_none=True)
    main_application_file = fields.Str(allow_none=True)
    arguments = fields.List(fields.Str(), allow_none=True)
    hadoop_conf = fields.Dict(keys=fields.Str(), values=fields.Str(), allow_none=True)
    spark_conf = fields.Dict(keys=fields.Str(), values=fields.Str(), allow_none=True)
    hadoop_config_map = fields.Str(allow_none=True)
    spark_config_map = fields.Str(allow_none=True)
    executor = fields.Nested(SparkReplicaSchema, allow_none=True)
    driver = fields.Nested(SparkReplicaSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return V1Spark


class V1Spark(BaseConfig, polyaxon_sdk.V1Spark):
    """Spark jobs are used to run Spark applications on Kubernetes.

    [Apache Spark](https://spark.apache.org/) is data-processing engine.

    Args:
        kind: str, should be equal `spark`
        connections: List[str], optional
        volumes: List[[Kubernetes Volume](https://kubernetes.io/docs/concepts/storage/volumes/)],
                 optional
        type: str [`JAVA`, `SCALA`, `PYTHON`, `R`]
        spark_version: str, optional
        python_version: str, optional
        deploy_mode: str, optional
        main_class: str, optional
        main_application_file: str, optional
        arguments: List[str], optional
        hadoop_conf: Dict[str, str], optional
        spark_conf: Dict[str, str], optional
        hadoop_config_map: str, optional
        spark_config_map: str, optional
        executor: [V1SparkReplica](/docs/experimentation/distributed/spark-replica/)
        driver: [V1SparkReplica](/docs/experimentation/distributed/spark-replica/)

    ## YAML usage

    ```yaml
    >>> run:
    >>>   kind: spark
    >>>   connections:
    >>>   volumes:
    >>>   type:
    >>>   sparkVersion:
    >>>   deployMode:
    >>>   mainClass:
    >>>   mainApplicationFile:
    >>>   arguments:
    >>>   hadoopConf:
    >>>   sparkConf:
    >>>   hadoopConfigMap:
    >>>   sparkConfigMap:
    >>>   executor:
    >>>   driver:
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1Environment, V1Init, V1Spark, V1SparkReplica, V1SparkType
    >>> from polyaxon.k8s import k8s_schemas
    >>> spark_job = V1Spark(
    >>>     connections=["connection-name1"],
    >>>     volumes=[k8s_schemas.V1Volume(...)],
    >>>     type=V1SparkType.PYTHON,
    >>>     spark_version="3.0.0",
    >>>     spark_conf={...},
    >>>     driver=V1SparkReplica(...),
    >>>     executor=V1SparkReplica(...),
    >>> )
    ```

    ## Fields

    ### kind

    The kind signals to the CLI, client, and other tools that this component's runtime is a job.

    If you are using the python client to create the runtime,
    this field is not required and is set by default.

    ```yaml
    >>> run:
    >>>   kind: spark
    ```

    ### connections

    A list of [connection names](/docs/setup/connections/) to resolve for the job.

    <blockquote class="light">
    If you are referencing a connection it must be configured.
    All referenced connections will be checked:

     * If they are accessible in the context of the project of this run

     * If the user running the operation can have access to those connections
    </blockquote>

    After checks, the connections will be resolved and inject any volumes, secrets, configMaps,
    environment variables for your main container to function correctly.

    ```yaml
    >>> run:
    >>>   kind: spark
    >>>   connections: [connection1, connection2]
    ```

    ### volumes

    A list of [Kubernetes Volumes](https://kubernetes.io/docs/concepts/storage/volumes/)
    to resolve and mount for your jobs.

    This is an advanced use-case where configuring a connection is not an option.

    When you add a volume you need to mount it manually to your container(s).

    ```yaml
    >>> run:
    >>>   kind: spark
    >>>   volumes:
    >>>     - name: volume1
    >>>       persistentVolumeClaim:
    >>>         claimName: pvc1
    >>>   ...
    ```

    ### type

    Tells the type of the Spark application, possible values: `Java`, `Scala`, `Python`, `R`

    ```yaml
    >>> run:
    >>>   kind: spark
    >>>   type: Python
    >>>   ...
    ```

    ### sparkVersion

    The version of Spark the application uses.

    ```yaml
    >>> run:
    >>>   kind: spark
    >>>   sparkVersion: 3.0.0
    >>>   ...
    ```

    ### deployMode

    The deployment mode of the Spark application.

    ```yaml
    >>> run:
    >>>   kind: spark
    >>>   deployMode: cluster
    >>>   ...
    ```

    ### mainClass

    The fully-qualified main class of the Spark application.
    This only applies to Java/Scala Spark applications.

    ```yaml
    >>> run:
    >>>   kind: spark
    >>>   mainClass: ...
    >>>   ...
    ```

    ### mainApplicationFile

    The path to a bundled JAR, Python, or R file of the application.

    ```yaml
    >>> run:
    >>>   kind: spark
    >>>   mainApplicationFile: ...
    >>>   ...
    ```

    ### arguments

    List of arguments to be passed to the application.

    ```yaml
    >>> run:
    >>>   kind: spark
    >>>   arguments: [...]
    >>>   ...
    ```

    ### hadoopConf

    HadoopConf carries user-specified Hadoop configuration properties as they would use
    the "--conf" option in spark-submit.
    The SparkApplication controller automatically adds prefix "spark.hadoop."
    to Hadoop configuration properties.

    ```yaml
    >>> run:
    >>>   kind: spark
    >>>   hadoopConf: {...}
    >>>   ...
    ```

    ### sparkConf

    Carries user-specified Spark configuration properties as they would use the  "--conf" option in
    spark-submit.

    ```yaml
    >>> run:
    >>>   kind: spark
    >>>   sparkConf: {...}
    >>>   ...
    ```

    ### hadoopConfigMap

    Carries the name of the ConfigMap containing Spark configuration files such as log4j.properties.
    The controller will add environment variable SPARK_CONF_DIR to
    the path where the ConfigMap is mounted to.

    ```yaml
    >>> run:
    >>>   kind: spark
    >>>   hadoopConfigMap: {...}
    >>>   ...
    ```

    ### sparkConfigMap

    Carries the name of the ConfigMap containing Spark configuration files such as log4j.properties.
    The controller will add environment variable SPARK_CONF_DIR to the
    path where the ConfigMap is mounted to.

    ```yaml
    >>> run:
    >>>   kind: spark
    >>>   sparkConfigMap: {...}
    >>>   ...
    ```

    ### executor

    Executor is a spark replica specification

    ```yaml
    >>> run:
    >>>   kind: spark
    >>>   executor:
    >>>     replicas: 1
    >>>     ...
    >>>   ...
    ```

    ### driver

    Driver a spark replica specification

    ```yaml
    >>> run:
    >>>   kind: spark
    >>>   driver:
    >>>     replicas: 1
    >>>     ...
    >>>   ...
    ```
    """

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
