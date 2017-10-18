# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from kubernetes import client

from polyaxon_schemas.k8s.templates import constants
from polyaxon_schemas.utils import to_list


def get_service(name, labels, ports, service_type=None, external_i_ps=None):
    external_i_ps = to_list(external_i_ps)
    ports = to_list(ports)
    metadata = client.V1ObjectMeta(name=name, labels=labels)
    service_ports = [client.V1ServicePort(port=port, target_port=port) for port in ports]
    spec = client.V1ServiceSpec(selector=labels,
                                type=service_type,
                                external_i_ps=external_i_ps,
                                ports=service_ports)
    return client.V1Service(api_version=constants.K8S_API_VERSION_V1,
                            kind=constants.K8S_SERVICE_KIND,
                            metadata=metadata,
                            spec=spec)
