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
import os

from typing import List

from polyaxon import pkg
from polyaxon.containers.names import MAIN_JOB_CONTAINER
from polyaxon.containers.pull_policy import PullPolicy
from polyaxon.k8s import k8s_schemas
from polyaxon.schemas.services import BaseServiceConfig, BaseServiceSchema
from polyaxon.schemas.types import V1ConnectionType


def get_cleaner_resources() -> k8s_schemas.V1ResourceRequirements:
    return k8s_schemas.V1ResourceRequirements(
        limits={"cpu": "0.5", "memory": "1000Mi"},
        requests={"cpu": "0.1", "memory": "80Mi"},
    )


class PolyaxonCleanerSchema(BaseServiceSchema):
    @staticmethod
    def schema_config():
        return V1PolyaxonCleaner


class V1PolyaxonCleaner(BaseServiceConfig):
    """Polyaxon cleaner is a helper job that gets scheduled to clean artifacts when a run is deleted.

    Polyaxon CE and Polyaxon Agent are deployed with default values for the cleaner,
    however if you need to control or update one or several aspects
    of how the cleaner is scheduled, this guide walks through the possible options.

    Args:
        image: str, optional.
        image_tag: str, optional.
        image_pull_policy: str, optional.
        resources: V1ResourceRequirements, optional.
        node_selector: Dict, optional
        affinity: V1Affinity, optional
        tolerations: List[V1Toleration], optional
        image_pull_secrets: List[str]

    ## YAML usage

    ```yaml
    >>> cleaner:
    >>>   image: polyaxon/polyaxon-init
    >>>   imageTag: v1.x
    >>>   imagePullPolicy: IfNotPresent
    >>>   resources: requests:
    >>>     memory: "64Mi"
    >>>     cpu: "50m"
    >>>   nodeSelector:
    >>>     foo: bar
    ```

    ## Fields

    ### image

    The container image to use.

    ```yaml
    >>> cleaner:
    >>>   image: polyaxon/polyaxon-init
    ```

    ### imageTag

    The container image tag to use.

    ```yaml
    >>> cleaner:
    >>>   imageTag: dev
    ```

    ### imagePullPolicy

    The image pull policy to use, it must be a valid policy supported by Kubernetes.

    ```yaml
    >>> cleaner:
    >>>   imagePullPolicy: Always
    ```

    ### resources

    The resources requirements to allocate to the container.

    ```yaml
    >>> cleaner:
    >>>   resources:
    >>>     memory: "64Mi"
    >>>     cpu: "50m"
    ```

    ### nodeSelector

    From [Kubernetes docs](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector)  # noqa

    > nodeSelector is the simplest recommended form of node selection constraint.
    > nodeSelector is a field of PodSpec. It specifies a map of key-value pairs.
    > For the pod to be eligible to run on a node, the node must have each of
    > the indicated key-value pairs as labels (it can have additional labels as well).
    > The most common usage is one key-value pair.

    ```yaml
    >>> cleaner:
    >>>   nodeSelector:
    >>>     node_label: node_value
    ```

    ### affinity

    From [Kubernetes docs](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity)  # noqa

    > The affinity/anti-affinity feature, greatly expands the types of constraints you can express.

    The affinity to use for scheduling the job.

    ```yaml
    >>> cleaner:
    >>>   affinity:
    >>>     podAffinity:
    >>>       preferredDuringSchedulingIgnoredDuringExecution:
    >>>         ...
    ```


    ### tolerations

    From [Kubernetes docs](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)  # noqa

    > Tolerations are applied to pods, and allow (but do not require)
    > the pods to schedule onto nodes with matching taints.

    ```yaml
    >>> cleaner:
    >>>   tolerations:
    >>>     - key: "key"
    >>>       operator: "Exists"
    >>>       effect: "NoSchedule"
    ```

    ### imagePullSecrets

    From [Kubernetes docs](https://kubernetes.io/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod)  # noqa

    > ImagePullSecrets is a list of references to secrets in the same namespace
    > to use for pulling any images in pods that reference this ServiceAccount.
    > ImagePullSecrets are distinct from Secrets because Secrets can be mounted in the pod,
    > but ImagePullSecrets are only accessed by the kubelet.

    ```yaml
    >>> cleaner:
    >>>   imagePullSecrets: ['secret1', 'secret2']
    ```
    """

    SCHEMA = PolyaxonCleanerSchema
    IDENTIFIER = "cleaner"

    def get_image(self):
        image = self.image or "polyaxon/polyaxon-init"
        image_tag = self.image_tag if self.image_tag is not None else pkg.VERSION
        return "{}:{}".format(image, image_tag) if image_tag else image

    def get_resources(self):
        return self.resources if self.resources else get_cleaner_resources()


def get_default_cleaner_container(
    store: V1ConnectionType,
    run_uuid: str,
    run_kind: str,
    cleaner: V1PolyaxonCleaner = None,
):
    subpath = os.path.join(store.store_path, run_uuid)

    clean_args = "polyaxon clean-artifacts {} --subpath={}".format(
        store.kind.replace("_", "-"), subpath
    )
    wait_args = "polyaxon wait --uuid={} --kind={}".format(run_uuid, run_kind)
    image = "polyaxon/polyaxon-init"
    image_tag = pkg.VERSION
    image_pull_policy = PullPolicy.IF_NOT_PRESENT.value
    resources = get_cleaner_resources()
    if cleaner:
        image = cleaner.image or image
        image_tag = cleaner.image_tag or image_tag
        image_pull_policy = cleaner.image_pull_policy or image_pull_policy
        resources = cleaner.resources or resources
    return k8s_schemas.V1Container(
        name=MAIN_JOB_CONTAINER,
        image="{}:{}".format(image, image_tag),
        image_pull_policy=image_pull_policy,
        command=["/bin/bash", "-c"],
        args=["{} && {}".format(wait_args, clean_args)],
        resources=resources,
    )


def get_batch_cleaner_container(
    store: V1ConnectionType,
    paths: List[str],
    cleaner: V1PolyaxonCleaner = None,
):
    subpaths = [os.path.join(store.store_path, subpath) for subpath in paths]
    subpaths = " ".join(["-sp={}".format(sp) for sp in subpaths])

    clean_args = "polyaxon clean-artifacts {} {}".format(
        store.kind.replace("_", "-"), subpaths
    )
    image = "polyaxon/polyaxon-init"
    image_tag = pkg.VERSION
    image_pull_policy = PullPolicy.IF_NOT_PRESENT.value
    resources = get_cleaner_resources()
    if cleaner:
        image = cleaner.image or image
        image_tag = cleaner.image_tag or image_tag
        image_pull_policy = cleaner.image_pull_policy or image_pull_policy
        resources = cleaner.resources or resources
    return k8s_schemas.V1Container(
        name=MAIN_JOB_CONTAINER,
        image="{}:{}".format(image, image_tag),
        image_pull_policy=image_pull_policy,
        command=["/bin/bash", "-c"],
        args=[clean_args],
        resources=resources,
    )
