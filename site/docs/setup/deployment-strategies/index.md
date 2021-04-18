---
title: "Deployment Strategies"
sub_link: "deployment-strategies"
is_index: true
title_link: "Deployment Strategies"
meta_title: "How to deploy, manage, and scale Polyaxon on Kubernetes"
meta_description: "This is a set of guides to assist you through the process of deploying, managing, and scaling a Polyaxon Deployment with common strategies and best practices."
tags:
  - setup
  - kubernetes
  - install
sidebar: "setup"
---

This is a set of guides to assist you through the process of deploying, managing, and scaling a Polyaxon Deployment with common strategies and best practices.

## Overview

There are different types of deployment strategies you can take advantage of depending on your goal, expected workload, number of team members, regulations, ...
  * You may deploy Polyaxon to just give it a try, without caring about spending time with configuring artifacts stores, git providers, ...
  * You may want to scale your operations over several nodes.
  * You may want to scale your operations over several clusters or cloud providers.
  * You may want to establish some processes to separate dev/staging/production environments either on different namespaces or on different clusters.
  * You may want to isolate projects, datasets access, models, and other artifacts either on different namespaces or on different clusters.
  * You may want to authorize users and teams with different access rights to different namespaces or to different clusters.

Polyaxon provides a set of customizable and flexible deployment strategies, that can fit different use cases and requirements.

In this section, we will try to go over:
  * Some strategies of deploying Polyaxon and possibly answer frequently asked questions about how to manage and scale Polyaxon.
  * Best practices for a production-ready deployment.
