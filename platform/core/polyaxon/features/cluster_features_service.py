from conf import ConfService


class ClusterFeaturesService(ConfService):
    def get_options_handler(self):
        from conf.handlers.cluster_options_handler import ClusterOptionsHandler

        return ClusterOptionsHandler()
