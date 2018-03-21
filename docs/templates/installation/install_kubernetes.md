If you have already a kubernetes cluster, you can skip this section, and [setup helm](setup_helm).

Kubernetes’ documentation describes [many ways to set up a cluster](https://kubernetes.io/docs/setup/pick-right-solution/).

In this guide we shall provide quick instructions for the most painless and popular ways of getting
a setup in various cloud providers.

??? caution "Security and sensitive data"
    If you are about to deploy a kubernetes cluster with sensitive data,
    please reach out to your sysadmin/devops team.
    You can also check the [Kubernetes best-practices guide](http://blog.kubernetes.io/2016/08/security-best-practices-kubernetes-deployment.html)
    for information about keeping your Kubernetes infrastructure secure.


## Install Kubernetes on [Google Kubernetes Engin](https://cloud.google.com/kubernetes-engine/)

Google Kubernetes Engine (GKE) is the simplest and most common way of setting up a Kubernetes Cluster.
You may be able to receive free credits for trying it out.

GKE provides a detailed documentation on how to [set up a containerized application with Kubernetes](https://cloud.google.com/kubernetes-engine/docs/quickstart)

If you have correctly configured your account,
you should be able to create a cluster with `gcloud container clusters create`.


## Install Kubernetes on [Microsoft Azure Container Service](https://azure.microsoft.com/en-us/services/container-service/)

Microsoft Azure Container Service (ACS) provides also a very simple way to set up a [Kubernetes cluster](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough)

If you have correctly configured your account,
you should be able to create a cluster with `az group create --name=${RESOURCE_GROUP} --location=${LOCATION}`

## Install Kubernetes on [Amazon Web Services](https://kubernetes.io/docs/getting-started-guides/aws/)

Although AWS does not have native support for Kubernetes,
there are many solutions and guides for setting up Kubernetes on AWS,
such as [kops](https://kubernetes.io/docs/getting-started-guides/kops/) and [Heptio](https://s3.amazonaws.com/quickstart-reference/heptio/latest/doc/heptio-kubernetes-on-the-aws-cloud.pdf)


If you have a kubernetes cluster running, it is time to [setup helm](setup_helm)
