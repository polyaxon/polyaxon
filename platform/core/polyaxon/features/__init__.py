from hestia.service_interface import LazyServiceWrapper

from django.conf import settings

from conf.option_manager import option_manager
from features.service import FeaturesService


def get_conf_backend():
    return settings.FEATURES_BACKEND or 'features.cluster_features_service.ClusterFeaturesService'


backend = LazyServiceWrapper(
    backend_base=FeaturesService,
    backend_path=get_conf_backend(),
    options={}
)
backend.expose(locals())

subscribe = option_manager.subscribe
