# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import urllib3
from kubernetes import client

from api.utils import config

K8S_CONFIG = client.Configuration()
K8S_CONFIG.api_key['authorization'] = config.get_string('POLYAXON_K8S_AUTHORISATION', is_optional=True)
K8S_CONFIG.api_key_prefix['authorization'] = 'Bearer'
K8S_CONFIG.host = config.get_string('POLYAXON_K8S_HOST')
SSL_CA_CERT = config.get_string('POLYAXON_K8S_SSL_CA_CERT', is_optional=True)
if SSL_CA_CERT:
    K8S_CONFIG.verify_ssl = True
    K8S_CONFIG.ssl_ca_cert = SSL_CA_CERT
else:
    K8S_CONFIG.verify_ssl = False
    urllib3.disable_warnings()
