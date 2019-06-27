---
title: "Polyaxon Roadmap"
sub_link: "roadmap"
meta_title: "Polyaxon Roadmap - Polyaxon Product Roadmap and Highlights"
meta_description: "Please note that the roadmap is intended to provide high-level visibility into the short-term direction of the product. This can change at any time."
visibility: public
status: published
tags:
    - reference
---

> Please note that the roadmap is intended to provide high-level visibility into the short-term direction of the product. This can change at any time. Several of these aspects are either in alpha phase, private beta, beta, or under heavy development.

## Product Roadmap

This roadmap features several aspects of Polyaxon, every aspect has it's own subsection. 
The main and most important aspect of our roadmap is the platform stability.

We welcome our users to give feedback and suggest updates and additions.

### Schema and parsing

 * Better schema for params with optional typing.
 * Rename declarations section to params.
 * Support k8s resources specification in addition to the current resources section (beta).
 * Add possibility to create manual groups: often time users running hyperparams tuning, 
   find themselves in a situation where the built-in AutoML algorithms provided by the platform do not allow to search a specific hyperparams space. 
   Polyaxon will provide the possibility to declare new type of algorithms, `manual` and `api`.
   
   * The `manual` section, similar to grid search, but instead of using the cartesian product to create suggestions, 
   the user can provide a list of dictionaries of the suggestions she wants to use for every experiment.
   * The `api` section, will enable Polyaxon to call a Service that the user will provide access to, to request suggestions, 
   this allow users to not only integrate Polyaxon with several external services, but also it will allow them to develop their own search models.
 * Make the build primitive first class, with the possibility to build arbitrary images, and the possibility to reference and reuse these images in other experiments/runs. 


### Runtime

 * Local run: Allow to run experiments (non-distributed) locally either by invoking a python with a conda/pip env or by generating a dockerfile, 
   with out-of-the box tracking if `POLYAXON_NO_OP` is not set to true (alpha).
 * Better Notebook/Lab/Colab experience.

### Deployment

 * Open sourcing "Cluster Level Dynamic Configuration", move it from EE to CE, the EE version uses forms to configure access, storages and integrations on Cluster/Project/Team/User levels, 
   we believe that by open sourcing the cluster level configuration we will allow several users to reconfigure their cluster without the need to upgrade the deployment, 
   hence avoiding downtime. 
   Our EE users will still enjoy several additional benefits with much better and fine grained configurable Polyaxon deployments.
 * Provide an easy way to use HA managed and external core dependencies: redis, registry, rabbitmq.
 * Polyaxon tracking and Polyaxon tracking & scheduling one click deployment on AWS MarketPlace, GCP MarketPlace, Azure MarketPlace.
 * Possibility to plugin a tsdb for high performance metrics insights and time series management.

### Platform

 * Open sourcing PolŷHat: Model packaging and easy deployment options with native integration with other community projects as well as integration with cloud offerings, 
   with possibility to start test servers in-cluster.
 * Post-deployment metrics watchdogs and workflow triggers.
 * Open sourcing PolyFlow, our internal events/actions and pipelining engine.
 * Better datasets management and access.
 * Data insights, features storage, and processing provenance.
 * Open sourcing PolyaxonAgent used in our PaaS, our solution to manage clusters remotely.
 * Possibility to enable automatic collections of outputs/artifacts at the end of the runs without scheduling Storage secrets access (WIP).
 * Stabilise PolyaxonCI, our CI engine solution to automate experimentation workflows, with additional enterprise extensions (private beta).
 * Stabilise several integrations.
 * Autoscaling of Polyaxon's core components.

### UI

 * Code tab for checking code version for experiments with possibility to compare changes/diffs between experiments.
 * Better outputs and artifacts preview, e.g. use proper editors for code files.
 * Better outputs categorization.
 * Enable running from template with Possibility to easily update default values (beta).

### Security

 * Introduce optional and configurable user UID and group GID for all Polyaxon services and scheduled runs (alpha, some backends like Horovod require privileged access).
 * Mount all volumes with the proper security context (alpha).

### Documentation
 
 * Documentation for setting templates for highly productive iterations: Polyaxon CLI allows to parse several configurations files, 
   this open the doors for setting several override templates, e.g. updating params, updating the node scheduling, updating resources.
 * Documentation for the development setup.
 * Documentation for the pure-docker cluster deployment.
   * Single machine docker deployment.
   * Multi-machines docker deployment, the goal is to allow deploy Polyaxon on any container management platform, e.g. Titus, Mesos, ...)
 * Documentation for easily setting up a production ready Polyaxon deployment on the major cloud providers.
 * Documentation for setting Polyaxon tracking on docker-compose (this is already in alpha, and can be started with one single CLI command)
 * Documentation for setting Polyaxon tracking on Heroku.
 
### Testing

 * More automation and deployment testing.
 * Abstract the e2e testing to reuse it with all git repos and examples.
