class ServiceTypes(object):
    LOAD_BALANCER = 'LoadBalancer'
    NODE_PORT = 'NodePort'
    CLUSTER_IP = 'clusterIP'

    VALUES = [LOAD_BALANCER, NODE_PORT, CLUSTER_IP]
