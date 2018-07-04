from polyaxon.config_manager import config

POLYAXON_K8S_APP_NAME = config.get_string('POLYAXON_K8S_APP_NAME')
POLYAXON_K8S_API_HOST = config.get_string('POLYAXON_K8S_API_HOST')
POLYAXON_K8S_API_PORT = config.get_int('POLYAXON_K8S_API_PORT')
POLYAXON_K8S_APP_CONFIG_NAME = config.get_string('POLYAXON_K8S_APP_CONFIG_NAME')
POLYAXON_K8S_APP_SECRET_NAME = config.get_string('POLYAXON_K8S_APP_SECRET_NAME')
POLYAXON_K8S_RABBITMQ_SECRET_NAME = config.get_string('POLYAXON_K8S_RABBITMQ_SECRET_NAME')

K8S_AUTHORISATION = config.get_string('POLYAXON_K8S_AUTHORISATION',
                                      is_optional=True,
                                      is_secret=True)
K8S_HOST = config.get_string('POLYAXON_K8S_HOST', is_optional=True)
SSL_CA_CERT = config.get_string('POLYAXON_K8S_SSL_CA_CERT', is_optional=True)

K8S_CONFIG = None
if K8S_AUTHORISATION and K8S_HOST:
    def set_config():
        import urllib3

        from kubernetes import client

        K8S_CONFIG = client.Configuration()
        K8S_CONFIG.api_key['authorization'] = K8S_AUTHORISATION
        K8S_CONFIG.api_key_prefix['authorization'] = 'Bearer'
        K8S_CONFIG.host = K8S_HOST

        if SSL_CA_CERT:
            K8S_CONFIG.verify_ssl = True
            K8S_CONFIG.ssl_ca_cert = SSL_CA_CERT
        else:
            K8S_CONFIG.verify_ssl = False
            urllib3.disable_warnings()


    set_config()

