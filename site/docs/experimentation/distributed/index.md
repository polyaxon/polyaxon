---
title: "Distributed Jobs"
sub_link: "distributed"
is_index: true
meta_title: "Distributed Jobs in Polyaxon - Experimentation"
meta_description: "Polyaxon supports distributed jobs for training or data processing via TF-Job, MPI-Job, PyTorch-Job."
tags:
  - concepts
  - polyaxon
  - experimentation
  - experiments
  - architecture
sidebar: "experimentation"
---

Polyaxon supports distributed jobs for model training or data processing via several Kubernetes operators.

By default, Polyaxon does not deploy the operators required for running distributed jobs to keep the deployment process lightweight.
In order to use a distributed jobs operator, you need to make sure that your namespace/cluster has the operator deployed
or you should deploy the operator(s) before starting an execution.

> When you start a distributed job, Polyaxon will stream and archive logs from all replicas.

## Training operator

In order to run TFJobs/MpiJobs/PyTorchJobs/MXNetJobs/PyTorchJobs you will need to deploy training operator before executing a job from Polyaxon.

### TFJob

Please check the [TFJob](/docs/experimentation/distributed/tf-jobs/) guide to learn about all details for running TfJobs in Polyaxon.

### MpiJob

Please check the [MpiJob](/docs/experimentation/distributed/mpi-jobs/) guide to learn about all details for running MpiJobs in Polyaxon.

### PyTorchJob

Please check the [PyTorchJob](/docs/experimentation/distributed/pytorch-jobs/) guide to learn about all details for running PyTorchJobs in Polyaxon.
