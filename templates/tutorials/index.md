In this tutorial we will be training models on Polyaxon deployed on [Microsoft Azure Container Service](https://azure.microsoft.com/en-us/services/container-service/).

The code is based on tensorflow/models, and trains and evaluate a CIFAR-10 ResNet model.

We will be creating single experiments, distributed experiments, and experiments with GPU:

 * A single host with one CPU;
 * Multiple hosts with CPUs/GPUs;

The tutorial will also provide a step by step guide to:

 * [create a Kubernetes cluster on Azure](kubernetes_on_azure)
 * [create a volumes for data and outputs on Azure](persistent_volumes)
 * [train experiments with Polyaxon](train_experiments)
 * [train distributed experiments with Polyaxon](train_distributed_experiments)
