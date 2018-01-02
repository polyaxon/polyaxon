# Introduction

Welcome to Polyaxon, a platform for building, training and monitoring large scale deep learning applications.

Polyaxon deploys into any data center, cloud provider,
or can be hosted and managed by Polyaxon,
and it supports all the major deep learning frameworks such as Tensorflow, MXNet, Caffe, Torch, etc.

Polyaxon makes it faster, easier, and more efficient to develop deep learning applications
by managing workloads with smart container and node management,
and turning GPU servers into shared, self-service resources for your team or organization.

Here  you will find a comprehensive guides for setting up Polyaxon on your cluster,
and information for training and monitoring your deep learning and AI applications.

We do our best to make this documentation clear and user friendly,
but If you see anything that is incorrect or have any questions,
feel free to reach out at the [issues page](https://github.com/polyaxon/polyaxon/issues),
[forum](https://gitter.im/polyaxon/polyaxon) or [contact us](mailto:contact@polyaxon.com).


## Get Started

This documentation start with quick start example,
and then walks through the steps required to install and configure a complete Polyaxon deployment in
the cloud or on your own infrastructure.
Using Kubernetes and the Polyaxon Helm chart provides sensible defaults for an initial deployment.

To get started, go to [Quick start with Polyaxon](quick_start) to start your first experiment.

To setup a Polyaxon deployment, go to [Installation requirements and setup](installation/introduction).

Once you have a Polyaxon deployment, you can learn how to organize your [experimentation workflow](experimentation/concepts).


## Management

 * [Admins management](management/admins)
 * [Users management](management/users)

## Customization

 * [Extending Polyaxon deployment](customization/extend_deployments)
 * [Customizing run environment](customization/customize_run_environment)


## References

 * [Command Line Interface Reference](polyaxon_cli/introduction)
 * [Polyaxon Specification Reference](polyaxonfile_specification/introduction)
 * [Polyaxon-Lib Reference](polyaxon_lib/introduction)
 * [Helm Chart Configuration Reference](reference_polyaxon_helm)
