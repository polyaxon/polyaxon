---
title: "PostgreSQL HA"
sub_link: "postgresql-ha"
meta_title: "High availability of postgresql database in Polyaxon - Configuration"
meta_description: "Keeping database records of your users, projects, experiments, and jobs is very important. Polyaxon offers a couple of ways to set a high available database."
tags:
    - configuration
    - polyaxon
    - postgresql
    - scaling
    - high-availability
    - kubernetes
    - docker-compose
sidebar: "configuration"
---

Polyaxon ships with a default Rabbitmq based on the stable [Helm chart](https://github.com/helm/charts/tree/master/stable/rabbitmq-ha).

You can check the chart values to extend it's configuration.

## External Rabbitmq

If you prefer to have Rabbitmq managed by you or hosted outside of Kubernetes, 
you need to disable the in-cluster Rabbitmq, and provide the information needed to establish a connection to the external one, e.g.:


```yaml
rabbitmq-hq:
  enabled: false

externalServices:
  rabbitmq:
    user: polyaxon
    password: polyaxon
    port: 12345
    host: 35.262.163.88
```

## Not using Rabbitmq

If you decide not to use Rabbitmq, and use Redis for handling events, please check this section on how to alter the [default broker behaviour](/configuration/broker/).
