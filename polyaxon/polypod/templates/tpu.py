import conf

from options.registry.k8s import K8S_TPU_TF_VERSION


def get_tpu_annotations():
    return {'tf-version.cloud-tpus.google.com': conf.get(K8S_TPU_TF_VERSION)}


def requests_tpu(resources):
    return resources and resources.tpu
