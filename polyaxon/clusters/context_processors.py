from clusters.models import Cluster


def cluster(request):
    return {'cluster': Cluster.load()}
