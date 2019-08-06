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

 * Improve local run experience.
 * Improve Notebook/JupyterLab experience.

### Platform

 * Stabilise PolyFlow: events/actions workflow engine.
 * Model packaging and easy deployment options with native integration with other community projects as well as integration with cloud offerings, 
   with possibility to start test servers in-cluster.
 * Post-deployment metrics watchdogs and workflow triggers.
 * Improve datasets management and access.
 * Data insights, features storage, and processing provenance.
 * Possibility to enable automatic collections of outputs/artifacts at the end of the runs without scheduling Storage secrets access (WIP).
 * Stabilise several integrations.
 * Expose monitoring.

### UI

 * Code tab for checking code version for experiments with possibility to compare changes/diffs between experiments.
 * Better outputs and artifacts preview, e.g. use proper editors for code files.
 * Better outputs categorization.

### Documentation
 
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
