This page describes the tools and requirements needed to deploy Polyaxon, to provide some more contextual information.

## Computational resources

In order to run Polyaxon you need some computational resources,

 * Computing
 * Disk space
 * GPU
 * Networking (both internal and external)
 * Creating, resizing, and deleting clusters

these resources could be your personal computer, university server,
or some other organization that hosts computational resources that can be accessed remotely.

Polyaxon will work fine with a cloud provider or a custom cluster deployments as well.
For these materials, any cluster with Kubernetes installed will work with Polyaxon.


## Container Technology

Container technology is essentially the idea of bundling all of the necessary components to run a piece of software.
There are many ways to do this, in the case of Polyaxon we use Docker to bundle the users dependencies required
to the code.


## Kubernetes

[Kubernetes](https://kubernetes.io/) is a service that runs on cloud infrastructures.
It provides a single point of contact with the machinery of your cluster deployment,
and allows a user to specify the computational requirements that they need
(e.g., how many machines, how many CPUs per machine, how much RAM).
Then, it handles the resources on the cluster and ensures that these resources are always available.
If something goes down, kubernetes will try to automatically bring it back up.


## Helm

[Helm](https://helm.sh/) is a package manager for Kubernetes,
 and a way of specifying kubernetes objects with a standard template.

Polyaxon is installed into Kubernetes using Helm.


## Polyaxon

[Polyaxon](https://polyaxon.com/) is an open-source system that abstracts and simplifies training, monitoring,
and scaling deep learning applications on Kubernetes clusters.

## Requirements

In order to run Polyaxon on top of Kubernetes, we need:

 * Access to internet to Pull images, unless you have all the images you need
   for running your experiments accessible to Kubernetes through a locally deployed registry.
 * Kubernetes with a version >= 1.8.0. Polyaxon might work with previous versions, but we recommend recent versions.
 * Helm with a version ≥ 2.5. Polyaxon might work with previous versions, but we recommend recent versions.
 * Persistence for data, outputs, logs, and code.


