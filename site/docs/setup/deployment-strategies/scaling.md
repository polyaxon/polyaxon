---
title: "Scaling Strategies"
sub_link: "deployment-strategies/scaling"
title_link: "Scaling Strategies"
meta_title: "How to scale Polyaxon on Kubernetes"
meta_description: "This is a guide to assist you through the process of scaling a Polyaxon Deployment."
tags:
  - setup
  - kubernetes
  - install
sidebar: "setup"
---

This is a guide to assist you through the process of scaling a Polyaxon Deployment.

## Overview

Scaling a Polyaxon deployment depends on the type of strategy you want to achieve and the type of Polyaxon distribution you are using.

## Scaling horizontally and vertically

In both Polyaxon CE and Polyaxon EE, you can scale your deployment horizontally by increasing the number of replicas of
the core components and services to handle more traffic and more users.

> Please check the services replication [guide](/docs/setup/platform/replication-concurrency/#services-replication) for more details.

Polyaxon also comes with a scheduler for handling and processing events and submissions in the background using async workers.
This scheduler can be enabled to handle more incoming submissions to compile them and queue them before sending them to Kubernetes to be executed.

> Please check [Celery integration guide](/integrations/celery/) for more details.

You can combine both of these scaling approaches and tune your configuration to handle any amount of traffic you expect for your Polyaxon deployment.

## Scaling with Agents

For users with a Polyaxon EE or Polyaxon Cloud subscription, you can additionally scale your deployment over multiple clusters by deploying multiple Polyaxon Agents.

> Please check [Polyaxon Agent setup](/docs/setup/agent/) for more details.
