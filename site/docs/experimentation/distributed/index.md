---
title: "Distributed Jobs"
sub_link: "distributed"
is_index: true
meta_title: "Distributed Jobs in Polyaxon - Experimentation"
meta_description: "Polyaxon supports distributed jobs for training or data processing via TF-Job, MPI-Job, Pytorch-Job, Spark-Job, Dask-Job."
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

In order to run TFJobs/MpiJobs/PytorchJobs/MXNetJobs/PytorchJobs you will need to deploy training operator before executing a job from Polyaxon.

### TFJob

Please check the [TFJob](/docs/experimentation/distributed/tf-jobs/) guide to learn about all details for running TfJobs in Polyaxon.

### MpiJob

Please check the [MpiJob](/docs/experimentation/distributed/mpi-jobs/) guide to learn about all details for running MpiJobs in Polyaxon.

### PytorchJob

Please check the [PytorchJob](/docs/experimentation/distributed/pytorch-jobs/) guide to learn about all details for running PytorchJobs in Polyaxon.

### MXNetJob

Please check the [MXNetJob](/docs/experimentation/distributed/mxnet-jobs/) guide to learn about all details for running MXNetJobs in Polyaxon.

### XGBoostJob

Please check the [XGBoostJob](/docs/experimentation/distributed/xgboost-jobs/) guide to learn about all details for running XGBoostJobs in Polyaxon.

## Spark

In order to run SparkJobs you will need to deploy the spark-on-k8s-operator before executing a job from Polyaxon.

Please check the [SparkJob](/docs/experimentation/distributed/spark-jobs/) guide to learn about all details for running SparkJobs in Polyaxon.

## Dask

Please check the [DaskJob](/docs/experimentation/distributed/dask-jobs/) guide to learn about all details for running DaskJobs in Polyaxon.
