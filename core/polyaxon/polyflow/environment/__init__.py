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
from polyaxon.schemas.base import BaseCamelSchema, BaseConfig
from polyaxon.schemas.fields.swagger import SwaggerField


class EnvironmentSchema(BaseCamelSchema):
    labels = fields.Dict(values=fields.Str(), keys=fields.Str(), allow_none=True)
    annotations = fields.Dict(values=fields.Str(), keys=fields.Str(), allow_none=True)
    node_selector = fields.Dict(values=fields.Str(), keys=fields.Str(), allow_none=True)
    affinity = SwaggerField(cls=k8s_schemas.V1Affinity, allow_none=True)
    tolerations = fields.List(
        SwaggerField(cls=k8s_schemas.V1Toleration), allow_none=True
    )
    node_name = fields.Str(allow_none=True)
    service_account_name = fields.Str(allow_none=True)
    host_aliases = fields.List(
        SwaggerField(cls=k8s_schemas.V1HostAlias), allow_none=True
    )
    security_context = SwaggerField(cls=k8s_schemas.V1SecurityContext, allow_none=True)
    image_pull_secrets = fields.List(fields.Str(), allow_none=True)
    host_network = fields.Bool(allow_none=True)
    dns_policy = fields.Str(allow_none=True)
    dns_config = SwaggerField(cls=k8s_schemas.V1PodDNSConfig, allow_none=True)
    scheduler_name = fields.Str(allow_none=True)
    priority_class_name = fields.Str(allow_none=True)
    priority = fields.Int(allow_none=True)
    restart_policy = fields.Str(
        allow_none=True, validate=validate.OneOf(["Always", "OnFailure", "Never"])
    )

    @staticmethod
    def schema_config():
        return V1Environment


class V1Environment(BaseConfig, polyaxon_sdk.V1Environment):
    """The environment section allows to alter the
    configuration of the runtime of your jobs, experiments, and services.

    Based on this section you can define several information
    that will be injected into the pod running on Kubernetes, e.g. the node selector.

    Args:
        labels: Dict, optional
        annotations: Dict, optional
        node_selector: Dict, optional
        affinity: V1Affinity, optional
        tolerations: V1Affinity, optional
        node_name: str, optional
        service_account_name: str, optional
        host_aliases: V1HostAlias, optional
        security_context: V1SecurityContext, optional
        image_pull_secrets: List[str], optional
        host_network: bool, optional
        dns_policy: str, optional
        dns_config: V1PodDNSConfig, optional
        scheduler_name: str, optional
        priority_class_name: str, optional
        priority: int, optional
        restart_policy: str, optional

    ## YAML usage

    ```yaml
    >>> environment:
    >>>   labels:
    >>>   annotations:
    >>>   nodeSelector:
    >>>   affinity:
    >>>   tolerations:
    >>>   nodeName:
    >>>   serviceAccountName:
    >>>   hostAliases:
    >>>   securityContext:
    >>>   imagePullSecrets:
    >>>   hostNetwork:
    >>>   dnsPolicy:
    >>>   dnsConfig:
    >>>   schedulerName:
    >>>   priorityClassName:
    >>>   priority:
    >>>   restartPolicy:
    ```

    ## Python usage

    ```python
    >>> from polyaxon.polyflow import V1Environment
    >>> environment = V1Environment(
    >>>     labels={
    >>>         "key1" : "value1",
    >>>         "key2" : "value2"
    >>>     },
    >>>     annotations={
    >>>         "key1" : "value1",
    >>>         "key2" : "value2"
    >>>     },
    >>>     node_selector={
    >>>         "node_label": "node_value"
    >>>     },
    >>>     affinity=V1Affinity(...),
    >>>     tolerations=V1Affinity(...),
    >>>     node_name="name",
    >>>     service_account_name="name",
    >>>     host_aliases=V1HostAlias(...),
    >>>     security_context=V1SecurityContext(...),
    >>>     image_pull_secrets=["secret1", "secret2", ...],
    >>>     host_network=False,
    >>>     dns_policy="Default",
    >>>     dns_config=V1PodDNSConfig(...),
    >>>     scheduler_name="name",
    >>>     priority_class_name="name",
    >>>     priority=0,
    >>>     restart_policy="Never",
    >>> )
    ```

    ## Fields

    ### labels

    From [Kubernetes docs](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)  # noqa

    > Labels are key/value pairs that are attached to objects, such as pods.
      Labels are intended to be used to specify identifying attributes of objects that
      are meaningful and relevant to users, but do not directly imply semantics to the core system.

    Polyaxon injects several labels to all operations it manages,
    users can leverage those labels or extend them.

    ```yaml
    >>> environment:
    >>>   labels:
    >>>     key1: "label1"
    >>>     key2: "label2"
    ```

    ### annotations

    From [Kubernetes docs](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/)  # noqa

    > You can use Kubernetes annotations to attach arbitrary non-identifying metadata to objects.
      Clients such as tools and libraries can retrieve this metadata.

    ```yaml
    >>> environment:
    >>>   annotations:
    >>>     key1: "value1"
    >>>     key2: "value2"
    ```

    ### nodeSelector

    From [Kubernetes docs](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector)  # noqa

    > nodeSelector is the simplest recommended form of node selection constraint.
      nodeSelector is a field of PodSpec. It specifies a map of key-value pairs.
      For the pod to be eligible to run on a node, the node must have each of
      the indicated key-value pairs as labels (it can have additional labels as well).
      The most common usage is one key-value pair.

    ```yaml
    >>> environment:
    >>>   nodeSelector:
    >>>     node_label: node_value
    ```

    ### affinity

    From [Kubernetes docs](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity)  # noqa

    > The affinity/anti-affinity feature, greatly expands the types of constraints you can express.

    The affinity to use for the scheduling the job.

    ```yaml
    >>> environment:
    >>>   affinity:
    >>>     podAffinity:
    >>>       preferredDuringSchedulingIgnoredDuringExecution:
    >>>         ...
    ```


    ### tolerations

    From [Kubernetes docs](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)  # noqa

    > Tolerations are applied to pods, and allow (but do not require)
      the pods to schedule onto nodes with matching taints.

    ```yaml
    >>> environment:
    >>>   tolerations:
    >>>     - key: "key"
    >>>       operator: "Exists"
    >>>       effect: "NoSchedule"
    ```

    ### nodeName

    From [Kubernetes docs](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodename)  # noqa

    > nodeName is the simplest form of node selection constraint,
      but due to its limitations it is typically not used. nodeName is a field of PodSpec.
      If it is non-empty, the scheduler ignores the pod and the kubelet running on the named
      node tries to run the pod. Thus, if nodeName is provided in the PodSpec,
      it takes precedence over the above methods for node selection.

    ```yaml
    >>> environment:
    >>>   nodeName: kube-01
    ```

    ### serviceAccountName

    From [Kubernetes docs](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/)  # noqa

    > A service account provides an identity for processes that run in a Pod.

    ```yaml
    >>> environment:
    >>>   serviceAccountName: build-robot
    ```

    In order for the custom service account to function correctly
    with Polyaxon sidecars/initializers, we recommend to include these rules in your custom service accounts:

    ```yaml
    >>> rules:
    >>>   - apiGroups: [""]
    >>>     resources: ["pods"]
    >>>     verbs: ["get", "watch", "list"]
    >>>   - apiGroups: ["metrics.k8s.io"]
    >>>     resources: ["pods", "nodes", "apis"]
    >>>     verbs: ["get", "list", "watch"]
    >>>   - apiGroups: ["", "*"]
    >>>     resources: ["events", "pods/status", "pods/log"]
    >>>     verbs: ["watch", "get", "list"]
    ```

    ### hostAliases

    From [Kubernetes docs](https://kubernetes.io/docs/concepts/services-networking/add-entries-to-pod-etc-hosts-with-host-aliases/)  # noqa

    > Adding entries to a Pod’s /etc/hosts file provides Pod-level override of hostname resolution
      when DNS and other options are not applicable. In 1.7,
      users can add these custom entries with the HostAliases field in PodSpec.

    ```yaml
    >>> environment:
    >>>   hostAliases:
    >>>   - ip: "127.0.0.1"
    >>>     hostnames:
    >>>     - "foo.local"
    >>>     - "bar.local"
    ```


    ### securityContext

    From [Kubernetes docs](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)  # noqa

    > A security context defines privilege and access control settings for a Pod or Container.

    ```yaml
    >>> environment:
    >>>   securityContext:
    >>>     runAsUser: 1000
    >>>     runAsGroup: 3000
    >>>     fsGroup: 2000
    ```

    ### imagePullSecrets

    From [Kubernetes docs](https://kubernetes.io/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod)  # noqa

    > ImagePullSecrets is a list of references to secrets in the same namespace
      to use for pulling any images in pods that reference this ServiceAccount.
      ImagePullSecrets are distinct from Secrets because Secrets can be mounted in the pod,
      but ImagePullSecrets are only accessed by the kubelet.

    ```yaml
    >>> environment:
    >>>   imagePullSecrets: ['secret1', 'secret2']
    ```

    ### hostNetwork

    From [Kubernetes docs](https://kubernetes.io/docs/concepts/policy/pod-security-policy/#host-namespaces)  # noqa

    > Controls whether the pod may use the node network namespace.
      Doing so gives the pod access to the loopback device, services listening on localhost,
      and could be used to snoop on network activity of other pods on the same node.

    ```yaml
    >>> environment:
    >>>   hostNetwork: false
    ```

    ### dnsPolicy

    From [Kubernetes docs](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#pods-dns-policy)  # noqa

    > Set DNS policy for the pod.
      Defaults to "ClusterFirst".
      Valid values are 'ClusterFirstWithHostNet', 'ClusterFirst', 'Default' or 'None'.
      DNS parameters given in DNSConfig will be merged with the policy selected with DNSPolicy.
      To have DNS options set along with hostNetwork, you have to specify DNS policy
      explicitly to 'ClusterFirstWithHostNet'.

    ```yaml
    >>> environment:
    >>>   dnsPolicy: ClusterFirst
    ```

    ### dnsConfig

    From [Kubernetes docs](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#pods-dns-config)  # noqa

    > Pod’s DNS Config allows users more control on the DNS settings for a Pod.

    ```yaml
    >>> environment:
    >>>   dnsConfig:
    >>>     nameservers:
    >>>       - 1.2.3.4
    >>>     searches:
    >>>       - ns1.svc.cluster-domain.example
    >>>       - my.dns.search.suffix
    >>>     options:
    >>>       - name: ndots
    >>>         value: "2"
    >>>       - name: edns0
    ```

    ### schedulerName

    From [Kubernetes docs](https://kubernetes.io/docs/tasks/administer-cluster/configure-multiple-schedulers/)  # noqa

    > If specified, the pod will be dispatched by specified scheduler.
      Or it will be dispatched by workflow scope scheduler if specified.
      If neither specified, the pod will be dispatched by default scheduler.

    ```yaml
    >>> environment:
    >>>   schedulerName: default-scheduler
    ```

    ### priorityClassName

    From [Kubernetes docs](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/)  # noqa

    > Pods can have priority.
      Priority indicates the importance of a Pod relative to other Pods.
      If a Pod cannot be scheduled, the scheduler tries to preempt (evict)
      lower priority Pods to make scheduling of the pending Pod possible.

    ```yaml
    >>> environment:
    >>>   priorityClassName: high
    ```

    ### priority

    From [Kubernetes docs](https://kubernetes.io/docs/concepts/configuration/pod-priority-preemption/)  # noqa

    > Pods can have priority.
      Priority indicates the importance of a Pod relative to other Pods.
      If a Pod cannot be scheduled, the scheduler tries to preempt (evict)
      lower priority Pods to make scheduling of the pending Pod possible.

    ```yaml
    >>> environment:
    >>>   priority: 10
    ```

    ### restartPolicy

    From [Kubernetes docs](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy)  # noqa

    > A PodSpec has a restartPolicy field with possible values Always, OnFailure, and Never.
      The default value is Always.


    ```yaml
    >>> environment:
    >>>   restartPolicy: Never
    ```
    """

    IDENTIFIER = "environment"
    SCHEMA = EnvironmentSchema
    REDUCED_ATTRIBUTES = [
        "labels",
        "annotations",
        "nodeSelector",
        "affinity",
        "tolerations",
        "nodeName",
        "serviceAccountName",
        "hostAliases",
        "securityContext",
        "imagePullSecrets",
        "hostNetwork",
        "dnsPolicy",
        "dnsConfig",
        "schedulerName",
        "priorityClassName",
        "priority",
        "restartPolicy",
    ]
