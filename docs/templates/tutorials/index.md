In this tutorial we will be training models on Polyaxon deployed on
[Microsoft Azure Container Service](https://azure.microsoft.com/en-us/services/container-service/) or
[Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine/).

The code is based on tensorflow/models, and trains and evaluate a CIFAR-10 ResNet model.

We will be creating single experiments, distributed experiments, and experiments with GPU.

The tutorial will also provide a step by step guide to:

 * Setup Kubernetes on:

     * [create a Kubernetes cluster on Azure](/tutorials/azure_deployment/kubernetes_on_azure)
     * [create volumes for data, outputs and logs on Azure](/tutorials/azure_deployment/persistent_volumes)
     * [train experiments with Polyaxon](/tutorials/azure_deployment/training_experiments_on_polyaxon/)

 * Setup Kubernetes on:

    * [create a Kubernetes cluster on GKE](/tutorials/gke_deployment/kubernetes_on_azure)
    * [create volumes for data, outputs and logs based on NFS](/tutorials/gke_deployment/persistent_volumes)
    * [train experiments with Polyaxon](/tutorials/gke_deployment/training_experiments_on_polyaxon/)
