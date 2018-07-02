# Introduction

Welcome to Polyaxon, a platform for building, training and monitoring large scale deep learning applications.

Polyaxon deploys into any data center, cloud provider,
or can be hosted and managed by Polyaxon,
and it supports all the major deep learning frameworks such as Tensorflow, MXNet, Caffe, Torch, etc.

Polyaxon makes it faster, easier, and more efficient to develop deep learning applications
by managing workloads with smart container and node management.
It also turns GPU servers into shared, self-service resources for your team or organization.

Here  you will find a comprehensive guide for setting up Polyaxon on your cluster,
and information for training and monitoring your deep learning applications.

We do our best to make this documentation clear and user friendly,
if you see anything that is incorrect or have any questions,
feel free to reach out at the
[issues page](https://github.com/polyaxon/polyaxon/issues),
[forum](https://join.slack.com/t/polyaxon/shared_invite/enQtMzQ0ODc2MDg1ODc0LWY2ZTdkMTNmZjBlZmRmNjQxYmYwMTBiMDZiMWJhODI2ZTk0MDU4Mjg5YzA5M2NhYzc5ZjhiMjczMDllYmQ2MDg)
or [contact us](mailto:contact@polyaxon.com).


## Get Started

This documentation start with quick start example,
and then walks through the steps required to install and configure a complete Polyaxon deployment either in
the cloud or on your own infrastructure.

Kubernetes and the Polyaxon Helm chart provide sensible defaults for an initial deployment.

To get started, go to [quick start with Polyaxon](quick_start) to start your first experiments.

To setup a Polyaxon deployment, go to [installation requirements and setup](installation/introduction).

Once you have a Polyaxon deployment, you can check polyaxon architecture and learn how to organize your [experimentation workflow](experimentation/concepts).


## Management

 * [Admins management](management/superusers)
 * [Users management](management/users)

## Customization

 * [Extending Polyaxon deployment](customization/extend_deployments)
 * [Customizing run environment](customization/customize_run_environment)
 * [Customize Node Scheduling](customization/customize_node_scheduling)
 * [Customize Data and Outputs](customization/customize_outputs_and_data)
 * [Single Sign On (SSO)](customization/single_sign_on)


## References

 * [CLI Reference](polyaxon_cli/introduction)
 * [Specification Reference](polyaxonfile_specification/introduction)
 * [Helm Chart Reference](reference_polyaxon_helm)
 * [Client Reference](reference_polyaxon_client)
 * [Helper Reference](reference_polyaxon_helper)
 * [Query Syntax Reference](reference_query_syntax)
