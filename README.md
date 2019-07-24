# Polyaxon Operator & Controller for Kubernetes

> This project is still work in progress, it's currently v1alpha1 version.

## Introduction

Kubernetes offers the facility of extending it's API through the concept of 'Operators' ([Introducing Operators: Putting Operational Knowledge into Software](https://coreos.com/blog/introducing-operators.html)). This repository contains the resources and code to deploy an Polyaxon native CRDs using a native Operator for Kubernetes.

It is a Kubernetes controller that manages and watches Customer Resource Definitions (CRDs) that define builds, jobs, experiments, notebooks, and tensorboards.

![Polyaxon Operator Architecture](artifacts/polyaxon-operator-architecture.png)

