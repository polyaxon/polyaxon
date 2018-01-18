In this tutorial we will be training models on Polyaxon deployed on [Microsoft Azure Container Service](https://azure.microsoft.com/en-us/services/container-service/).

The code is based on tensorflow/models, and trains and evaluate a CIFAR-10 ResNet model.

We will be creating single experiments, distributed experiments, and experiments with GPU.

The tutorial will also provide a step by step guide to:

 * [create a Kubernetes cluster on Azure](https://docs.polyaxon.com/tutorials/kubernetes_on_azure)
 * [create volumes for data and outputs on Azure](https://docs.polyaxon.com/tutorials/persistent_volumes)
 * [train experiments with Polyaxon](https://docs.polyaxon.com/tutorials/training_experiments_on_polyaxon/)
