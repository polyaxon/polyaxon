class DeploymentTypes(object):
    KUBERNETES = 'kubernetes'
    DOCKER_COMPOSE = 'docker-compose'
    DOCKER = 'docker'
    HEROKU = 'heroku'

    VALUES = [KUBERNETES, DOCKER_COMPOSE, DOCKER, HEROKU]
