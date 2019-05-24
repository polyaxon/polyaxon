from conf import ConfService


class ClusterConfService(ConfService):
    def get_db_handler(self):
        from conf.handlers.cluster_handler import ClusterHandler

        return ClusterHandler()
