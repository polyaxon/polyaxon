from models.clusters import Cluster


def cluster(request):
    return {'cluster': Cluster.load()}
