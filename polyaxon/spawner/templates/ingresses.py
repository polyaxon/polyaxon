from kubernetes import client

from polyaxon_k8s import constants as k8s_constants


def get_ingress(namespace, name, labels, annotations, paths):
    metadata = client.V1ObjectMeta(name=name,
                                   labels=labels,
                                   namespace=namespace,
                                   annotations=annotations)
    paths = paths
    rules = [client.V1beta1IngressRule(http=client.V1beta1HTTPIngressRuleValue(paths=paths))]
    spec = client.V1beta1IngressSpec(rules=rules)
    return client.V1beta1Ingress(api_version=k8s_constants.K8S_API_VERSION_V1_BETA1,
                                 kind=k8s_constants.K8S_INGRESS_KIND,
                                 metadata=metadata,
                                 spec=spec)
