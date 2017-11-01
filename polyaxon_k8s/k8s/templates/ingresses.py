from kubernetes import client

from polyaxon_k8s.k8s.templates import constants


def get_ingress(name, labels, paths):
    metadata = client.V1ObjectMeta(name=name, labels=labels)
    paths = paths
    rules = [client.V1beta1IngressRule(http=client.V1beta1HTTPIngressRuleValue(paths=paths))]
    spec = client.V1beta1IngressSpec(rules=rules)
    return client.V1beta1Ingress(api_version=constants.K8S_API_VERSION_V1_BETA1,
                                 kind=constants.K8S_INGRESS_KIND,
                                 metadata=metadata,
                                 spec=spec)
