# polyaxon-deploy

This repository contains tools to validate and deploy Polyaxon to one of the supported platforms:
 * [Single-machine Docker deployment]()
 * [Multi-machine Docker deployment]()
 * [Kubernetes deployment]()
 
 The goal of this project is to streamline the deployment of Polyaxon to any container management platform, including: 
 [Kubernetes](https://kubernetes.io), [Docker](https://www.docker.com/), [Docker Compose](https://docs.docker.com/compose/), [Docker Swarm](https://docs.docker.com/engine/swarm/), [Fargate](https://aws.amazon.com/fargate/), Netflix's [Titus](https://netflix.github.io/titus/), Apache's [Mesos](http://mesos.apache.org/documentation/latest/docker-containerizer/), [Nomad](https://www.nomadproject.io), [Heroku](http://heroku.com/) etc.
 
 ## This work is still in Private Beta phase

This project is not yet heavily tested, and there may be major bugs or regressions.

## Deploying

Starting from polyaxon v0.4.0, the recommended method of installing and managing a stable Polyaxon deployment will be through our [CLI](https://github.com/polyaxon/polyaxon-cli)


### Checking a deployment file, requirements, and dependencies:

```bash
polyaxon deploy -f polyaxon-config.yaml --check
```

### Install Polyaxon

```bash
polyaxon deploy -f polyaxon-config.yaml
```

### Upgrading a Polyaxon deployment

```bash
polyaxon deploy -f polyaxon-config.yaml --upgrade
```

### Tearing down the deployment

```bash
polyaxon teardown
```
