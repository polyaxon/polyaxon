[![License: Apache 2](https://img.shields.io/badge/License-apache2-blue.svg?style=flat&longCache=true)](LICENSE)
[![Polyaxon API](https://img.shields.io/docker/pulls/polyaxon/polyaxon-api)](https://hub.docker.com/r/polyaxon/polyaxon-api)
[![Slack](https://img.shields.io/badge/Slack-1.4k%20members-blue.svg?style=flat&logo=slack&longCache=true)](https://polyaxon.com/slack/)

[![Docs](https://img.shields.io/badge/docs-stable-brightgreen.svg?style=flat&longCache=true)](https://polyaxon.com/docs/)
[![Release](https://img.shields.io/badge/release-v1.16.1-brightgreen.svg?longCache=true)](https://polyaxon.com/docs/releases/1-16/)
[![GitHub](https://img.shields.io/badge/issue_tracker-github-blue?style=flat&logo=github&longCache=true)](https://github.com/polyaxon/polyaxon/issues)
[![GitHub](https://img.shields.io/badge/roadmap-github-blue?style=flat&logo=github&longCache=true)](https://github.com/orgs/polyaxon/projects/5)

[![CLI](https://github.com/polyaxon/polyaxon/actions/workflows/core.yml/badge.svg)](https://github.com/polyaxon/polyaxon/actions/workflows/core.yml)
[![Traceml](https://github.com/polyaxon/polyaxon/actions/workflows/traceml.yml/badge.svg)](https://github.com/polyaxon/polyaxon/actions/workflows/traceml.yml)
[![Datatile](https://github.com/polyaxon/polyaxon/actions/workflows/datatile.yml/badge.svg)](https://github.com/polyaxon/polyaxon/actions/workflows/datatile.yml)
[![Platform](https://github.com/polyaxon/polyaxon/actions/workflows/platform.yml/badge.svg)](https://github.com/polyaxon/polyaxon/actions/workflows/platform.yml)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/90c05b6b112548c1a88b950beceacb69)](https://www.codacy.com/app/polyaxon/polyaxon?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=polyaxon/polyaxon&amp;utm_campaign=Badge_Grade)

<br>
<p align="center">
  <p align="center">
    <a href="https://polyaxon.com/?utm_source=github&utm_medium=logo" target="_blank">
      <img src="https://raw.githubusercontent.com/polyaxon/polyaxon/master/artifacts/logo/vector/primary-white-default-monochrome.svg" alt="polyaxon" height="100">
    </a>
  </p>
  <p align="center">
    Reproduce, Automate, Scale your data science.
  </p>
</p>
<br>


Welcome to Polyaxon, a platform for building, training, and monitoring large scale deep learning applications.
We are making a system to solve reproducibility, automation, and scalability for machine learning applications.

Polyaxon deploys into any data center, cloud provider, or can be hosted and managed by Polyaxon, and it supports all the major deep learning frameworks such as Tensorflow, MXNet, Caffe, Torch, etc.

Polyaxon makes it faster, easier, and more efficient to develop deep learning applications by managing workloads with smart container and node management. And it turns GPU servers into shared, self-service resources for your team or organization.

<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/polyaxon/polyaxon/master/artifacts/demo.gif" alt="demo" width="80%">
</p>
<br>

# Install

#### TL;DR;

* Install CLI

    ```bash
    # Install Polyaxon CLI
    $ pip install -U polyaxon
    ```

 * Create a deployment

    ```bash
    # Create a namespace
    $ kubectl create namespace polyaxon

    # Add Polyaxon charts repo
    $ helm repo add polyaxon https://charts.polyaxon.com

    # Deploy Polyaxon
    $ polyaxon admin deploy -f config.yaml

    # Access API
    $ polyaxon port-forward
    ```

Please check [polyaxon installation guide](https://polyaxon.com/docs/setup/)

# Quick start

#### TL;DR;

 * Start a project

    ```bash
    # Create a project
    $ polyaxon project create --name=quick-start --description='Polyaxon quick start.'
    ```

 * Train and track logs & resources

    ```bash
    # Upload code and start experiments
    $ polyaxon run -f experiment.yaml -u -l
    ```

 * Dashboard

    ```bash
    # Start Polyaxon dashboard
    $ polyaxon dashboard

    Dashboard page will now open in your browser. Continue? [Y/n]: y
    ```

<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/polyaxon/polyaxon/master/artifacts/compare.png" alt="compare" width="400">
  <img src="https://raw.githubusercontent.com/polyaxon/polyaxon/master/artifacts/dashboards.png" alt="dashboards" width="400">
</p>
<br>

 * Notebook
    ```bash
    # Start Jupyter notebook for your project
    $ polyaxon run --hub notebook
    ```

<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/polyaxon/polyaxon/master/artifacts/notebook.png" alt="compare" width="400">
</p>
<br>

 * Tensorboard
    ```bash
    # Start TensorBoard for a run's output
    $ polyaxon run --hub tensorboard -P uuid=UUID
    ```

<br>
<p align="center">
  <img src="https://raw.githubusercontent.com/polyaxon/polyaxon/master/artifacts/tensorboard.png" alt="tensorboard" width="400">
</p>
<br>

Please check our [quick start guide](https://polyaxon.com/docs/intro/quick-start/) to start training your first experiment.

# Distributed job

Polyaxon supports and simplifies distributed jobs.
Depending on the framework you are using, you need to deploy the corresponding operator, adapt your code to enable the distributed training,
and update your polyaxonfile.

Here are some examples of using distributed training: 

 * [Distributed Tensorflow](https://polyaxon.com/docs/experimentation/distributed/tf-jobs/)
 * [Distributed Pytorch](https://polyaxon.com/docs/experimentation/distributed/pytorch-jobs/)
 * [Distributed MPI](https://polyaxon.com/docs/experimentation/distributed/mpi-jobs/)
 * [Horovod](https://polyaxon.com/integrations/horovod/)
 * [Spark](https://polyaxon.com/docs/experimentation/distributed/spark-jobs/)
 * [Dask](https://polyaxon.com/docs/experimentation/distributed/dask-jobs/)

# Hyperparameters tuning

Polyaxon has a concept for suggesting hyperparameters and managing their results very similar to Google Vizier called experiment groups.
An experiment group in Polyaxon defines a search algorithm, a search space, and a model to train.

 * [Grid search](https://polyaxon.com/docs/automation/optimization-engine/grid-search/)
 * [Random search](https://polyaxon.com/docs/automation/optimization-engine/random-search/)
 * [Hyperband](https://polyaxon.com/docs/automation/optimization-engine/hyperband/)
 * [Bayesian Optimization](https://polyaxon.com/docs/automation/optimization-engine/bayesian-optimization/)
 * [Hyperopt](https://polyaxon.com/docs/automation/optimization-engine/hyperopt/)
 * [Custom Iterative Optimization](https://polyaxon.com/docs/automation/optimization-engine/iterative/)

# Parallel executions

You can run your processing or model training jobs in parallel, Polyaxon provides a [mapping](https://polyaxon.com/docs/automation/mapping/) abstraction to manage concurrent jobs.

# DAGs and workflows

[Polyaxon DAGs](https://polyaxon.com/docs/automation/flow-engine/) is a tool that provides container-native engine for running machine learning pipelines. 
A DAG manages multiple operations with dependencies. Each operation is defined by a component runtime. 
This means that operations in a DAG can be jobs, services, distributed jobs, parallel executions, or nested DAGs.
 

# Architecture

![Polyaxon architecture](artifacts/polyaxon_architecture.png)

# Documentation

Check out our [documentation](https://polyaxon.com/docs/) to learn more about Polyaxon.

# Dashboard

Polyaxon comes with a dashboard that shows the projects and experiments created by you and your team members.

To start the dashboard, just run the following command in your terminal

```bash
$ polyaxon dashboard -y
```

# Project status

Polyaxon is stable and it's running in production mode at many startups and Fortune 500 companies. 

# Contributions

Please follow the contribution guide line: *[Contribute to Polyaxon](CONTRIBUTING.md)*.


# Research

If you use Polyaxon in your academic research, we would be grateful if you could cite it.

Feel free to [contact us](mailto:contact@polyaxon.com), we would love to learn about your project and see how we can support your custom need.
