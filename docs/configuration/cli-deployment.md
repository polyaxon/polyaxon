---
title: "Introduction"
sub_link: "introduction"
meta_title: "Introduction to Configuring Polyaxon - Configuration & Customization"
meta_description: "Find out how to configure your deployment and override Polyaxon's default behaviour with different options. Read more 👉"
tags:
    - configuration
    - config
    - polyaxon
    - kubernetes
    - docker-compose
sidebar: "configuration"
---

## Overview

Starting form Polyaxon v0.4.0 the supported and recommended method of deploying Polyaxon will be using `polyaxon-cli`, 
There are some configuration options which are required and many other are optional.

The following articles in this section explain how to use the `cli` to create config deployment, 
as well as walk you through some of the important config options, like database, storage, notifications, ...

## Deploying Polyaxon

In order to deploy Polyaxon, you will need to a `config.yaml`. 
You can use `polyaxon deploy -f config.yaml check` to verify that your configuration file is valid, 
and then you can run `polyaxon deploy -f config.yaml install`.

Please visit the [setup](/setup/) page to learn more about how you can setup a Polyaxon deployment.

## Applying configuration changes

The general method to modify your a Polyaxon deployment is to:

 1. Make a change to the config.yaml
 2. Run `polyaxon deploy -f config.yaml check`
 3. Run `polyaxon deploy -f config.yaml upgrade --name=<RELEASE_NAME>`

    `<RELEASE_NAME>` is the parameter you passed to `--name` when installing polyaxon with `polyaxon -f config.yaml install --name=<RELEASE_NAME>`.

    If you don’t remember it, you can probably find it by doing `polyaxon deploy list`.

    If you used the default values suggested in the docs, the `<RELEASE_NAME>` should be `polyaxon`

 4. Wait for the upgrade to finish, and make sure that when you do
    `kubectl --namespace=<NAMESPACE> get pod` the pods are in Ready state.
    Your configuration change has been applied!
