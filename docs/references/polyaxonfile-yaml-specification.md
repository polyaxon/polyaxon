---
title: "Polyaxonfile YAML Specification"
sub_link: "polyaxonfile-yaml-specification"
meta_title: "Polyaxonfile YAML Specification - Polyaxon References"
meta_description: "In order to use Polyaxon, users need to create YAML/Json polyaxonfiles. These files use a specification to describe how experiments, experiment groups, jobs, plugins should run on Polyaxon."
visibility: public
status: published
tags:
    - specifications
    - polyaxon
    - yaml
sidebar: "polyaxon-yaml-specification"
---

In order to use Polyaxon, users need to create YAML polyaxonfiles.
These files use a specification to describe how experiments, experiment groups, jobs, plugins should run on Polyaxon.

The Polyaxon specification is based on a list of sections, in this guide, we describe the required and optional sections.

!!! note
    Polyaxon specification can parse both YAML and Json format.


## Experiment Sections

 * [version](/references/polyaxonfile-yaml-specification/version/) `required`: defines the version of the file to be parsed and validated.
 * [kind](/references/polyaxonfile-yaml-specification/kind/) `required`: defines the kind of operation to run: experiment.
 * [logging](/references/polyaxonfile-yaml-specification/logging/): defines the logging.
 * [project](/references/polyaxonfile-yaml-specification/project/) `required`: defines the project name (must be unique).
 * [environment](/references/polyaxonfile-yaml-specification/environment/): defines the run environment, resources, persistence, and node selectors.
 * [declarations](/references/polyaxonfile-yaml-specification/declarations/): defines variables/modules that can be reused.
 * [build](/references/polyaxonfile-yaml-specification/polyaxonfile-yaml-specification/build/) `required`: defines the how the user can set a docker image.
 * [run](/references/polyaxonfile-yaml-specification/run/) `required`: defines the how the user can set a command to execute.


## Experiment Group Sections

 * [version](/references/polyaxonfile-yaml-specification/version/) `required`: defines the version of the file to be parsed and validated.
 * [kind](/references/polyaxonfile-yaml-specification/kind/) `required`: defines the kind of operation to run: group.
 * [logging](/references/polyaxonfile-yaml-specification/logging/): defines the logging.
 * [project](/references/polyaxonfile-yaml-specification/project/) `required`: defines the project name (must be unique).
 * [hptuning](/references/polyaxonfile-yaml-specification/hptuning/) `required`: defines the seed, concurrent runs, search algorithm, early stopping, matrix hyper parameters.
 * [environment](/references/polyaxonfile-yaml-specification/environment/): defines the run environment, resources, node selectors, and distributed jobs definition.
 * [declarations](/references/polyaxonfile-yaml-specification/declarations/): defines variables/modules that can be reused.
 * [build](/references/polyaxonfile-yaml-specification/build/) `required`: defines the how the user can set a docker image.
 * [run](/references/polyaxonfile-yaml-specification/run/) `required`: defines the how the user can set a command to execute.


## Build Job sections

 * [version](/references/polyaxonfile-yaml-specification/version/) `required`: defines the version of the file to be parsed and validated.
 * [kind](/references/polyaxonfile-yaml-specification/kind/) `required`: defines the kind of operation to run: build.
 * [project](/references/polyaxonfile-yaml-specification/project/) `required`: defines the project name (must be unique).
 * [environment](/references/polyaxonfile-yaml-specification/environment/): defines the run environment, resources, persistence, and node selectors.
 * [build](/references/polyaxonfile-yaml-specification/build/) `required`: defines the how the user can set a docker image.


## Generic Job sections

 * [version](/references/polyaxonfile-yaml-specification/version/) `required`: defines the version of the file to be parsed and validated.
 * [kind](/references/polyaxonfile-yaml-specification/kind/) `required`: defines the kind of operation to run: job.
 * [project](/references/polyaxonfile-yaml-specification/project/) `required`: defines the project name (must be unique).
 * [environment](/references/polyaxonfile-yaml-specification/environment/): defines the run environment, resources, persistence, and node selectors.
 * [build](/references/polyaxonfile-yaml-specification/build/) `required`: defines the how the user can set a docker image.
 * [run](/references/polyaxonfile-yaml-specification/run/) `required`: defines the how the user can set a command to execute.

## Tensorboard sections

 * [version](/references/polyaxonfile-yaml-specification/version/) `required`: defines the version of the file to be parsed and validated.
 * [kind](/references/polyaxonfile-yaml-specification/kind/) `required`: defines the kind of operation to run: plugin.
 * [project](/references/polyaxonfile-yaml-specification/project/) `required`: defines the project name (must be tensorboard).
 * [environment](/references/polyaxonfile-yaml-specification/environment/): defines the run environment, resources, persistence, and node selectors.
 * [build](/references/polyaxonfile-yaml-specification/build/) `required`: defines the how the user can set a docker image.


## Notebook sections

 * [version](/references/polyaxonfile-yaml-specification/version/) `required`: defines the version of the file to be parsed and validated.
 * [kind](/references/polyaxonfile-yaml-specification/kind/) `required`: defines the kind of operation to run: notebook.
 * [project](/references/polyaxonfile-yaml-specification/project/) `required`: defines the project name (must be unique).
 * [environment](/references/polyaxonfile-yaml-specification/environment/): defines the run environment, resources, persistence, and node selectors.
 * [build](/references/polyaxonfile-yaml-specification/build/) `required`: defines the how the user can set a docker image.
