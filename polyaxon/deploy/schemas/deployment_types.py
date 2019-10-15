class DeploymentTypes(object):
    KUBERNETES = 'kubernetes'
    MINIKUBE = 'minikube'
    MICRO_K8S = 'microk8s'
    DOCKER_COMPOSE = 'docker-compose'
    DOCKER = 'docker'
    HEROKU = 'heroku'

    VALUES = [KUBERNETES, MINIKUBE, MICRO_K8S, DOCKER_COMPOSE, DOCKER, HEROKU]
