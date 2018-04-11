[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Slack](https://img.shields.io/badge/chat-on%20slack-aadada.svg?logo=slack&longCache=true)](https://join.slack.com/t/polyaxon/shared_invite/enQtMzQ0ODc2MDg1ODc0LWY2ZTdkMTNmZjBlZmRmNjQxYmYwMTBiMDZiMWJhODI2ZTk0MDU4Mjg5YzA5M2NhYzc5ZjhiMjczMDllYmQ2MDg)


# polyaxon-examples

Code for polyaxon tutorials and examples.

The code in this repo is used for training models on Polyaxon deployed on [Microsoft Azure Container Service](https://azure.microsoft.com/en-us/services/container-service/).

The code in this repo is based on tensorflow/models, and trains and evaluate a CIFAR-10 ResNet model.

This repo also contains polyaxonfiles for training: single experiments, distributed experiments, and experiments with GPU.

The tutorial provides a step by step guide to:

 * [create a Kubernetes cluster on Azure](https://docs.polyaxon.com/tutorials/kubernetes_on_azure)
 * [create volumes for data and outputs on Azure](https://docs.polyaxon.com/tutorials/persistent_volumes)
 * [train experiments with Polyaxon](https://docs.polyaxon.com/tutorials/training_experiments_on_polyaxon)

