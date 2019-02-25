---
title: "Polyaxon Optimization Engine"
sub_link: "polyaxon-optimization-engine"
meta_title: "Polyaxon Optimization Engine Specification - Polyaxon References"
meta_description: "Finding good hyperparameters involves can be very challenging,
and requires to efficiently search the space of possible hyperparameters as well as
how to manage a large set of experiments for hyperparameter tuning, Polyaxon Optimization Engine tries to simplify this by exposing a set of search algorithms."
visibility: public
status: published
tags:
    - reference
    - polyaxon
    - experimentation
    - hyperparams-optimization
sidebar: "polyaxon-optimization-engine"
---

This reference guide assumes that you have already familiarized yourself with the concept of [experiment_groups](/concepts/experiment-groups/).

## Overview 

Hyperparameters selection is crucial for creating robust models,
since they heavily influence the behavior of the learned model.
Finding good hyperparameters involves can be very challenging,
and requires to efficiently search the space of possible hyperparameters as well as
how to manage a large set of experiments for hyperparameter tuning.

The way Polyaxon performs hyperparameters tuning is by providing to the data scientists a selection of search algorithms.
Polyaxon supports both simple approaches such as `random search` and `grid search`, and provides a simple interface for
advanced approaches, such as `Hyperband` and `Bayesian Optimization`.

All these search algorithms run in an asynchronous way, and support concurrency to leverage your cluster's resources to the maximum.

Some of these approaches are also iterative and improve based on previous experiments.

## Algorithms 

In order to search a hyperparameter space, all search algorithms require a `hptuning` section,
they also share some subsections such as: `matrix` definition of hyperparameters, `early_stopping`, and `concurrency`.
Each one of this algorithms has a dedicated subsection to define the required options.

 * [Grid search](/references/polyaxon-optimization-engine/grid-search/)
 * [Random search](/references/polyaxon-optimization-engine/random-search/)
 * [Hyperband](/references/polyaxon-optimization-engine/hyperband/)
 * [Bayesian Optimization](/references/polyaxon-optimization-engine/bayesian-optimization/)
