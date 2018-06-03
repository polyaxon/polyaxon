from django.conf import settings

API_URL = '{}//{}:{}'.format(settings.PROTOCOL,
                             settings.POLYAXON_K8S_API_HOST,
                             settings.POLYAXON_K8S_API_PORT)
