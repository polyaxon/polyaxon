---
title: "Rabbitmq HA"
sub_link: "platform/rabbitmq-ha"
meta_title: "High availability of Rabbitmq in Polyaxon - Configuration"
meta_description: "Polyaxon offers a couple of ways to set a high available Rabbitmq."
tags:
  - configuration
  - polyaxon
  - rabbitmq
  - scaling
  - high-availability
  - kubernetes
  - docker-compose
sidebar: "setup"
---

Polyaxon ships with a default Rabbitmq based on the stable [Helm chart](https://github.com/bitnami/charts/tree/main/bitnami/rabbitmq).

You can check the chart values to extend its configuration.

## External Rabbitmq

If you prefer to have Rabbitmq managed by you or hosted outside of Kubernetes,
you need to disable the in-cluster Rabbitmq, and provide the information needed to establish a connection to the external one, e.g.:


```yaml
broker: rabbitmq

rabbitmq:
  enabled: false

externalServices:
  rabbitmq:
    user: polyaxon
    password: polyaxon
    port: 12345
    host: 35.262.163.88
```

## Disabling Rabbitmq

If you decide not to use Rabbitmq, and use Redis for handling events, please check this section on how to alter the [default broker behavior](/docs/setup/platform/broker/).

## Scheduling

If you decided to deploy Rabbitmq in-cluster make sure to set proper [node scheduling](/docs/setup/platform/common-reference/#node-and-deployment-manipulation)
to avoid running high load runs on the same node hosting Rabbitmq.
