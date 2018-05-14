In order to use Polyaxon, users need to create YAML polyaxonfiles.
These files use a specification to describe how experiments, experiment groups, jobs, plugins should run on Polyaxon.

The Polyaxon specification is based on a list of sections, in this guide, we describe the required and optional sections.

!!! note
    Polyaxon specification can parse both YAML and Json format.


## Experiment Sections

 * [version](sections#version) `required`: defines the version of the file to be parsed and validated.
 * [kind](sections#kind) `required`: defines the kind of operation to run: experiment.
 * [project](sections#project) `required`: defines the project name (must be unique).
 * [settings](sections#settings): defines the logging, early stopping.
 * [environment](sections#environment): defines the run environment, resources, and node selectors.
 * [declarations](sections#declarations): defines variables/modules that can be reused.
 * [run](sections#run) `required`: defines the how the user can set a docker image and a command to execute.


## Experiment Group Sections

 * [version](sections#version) `required`: defines the version of the file to be parsed and validated.
 * [kind](sections#kind) `required`: defines the kind of operation to run: group.
 * [project](sections#project) `required`: defines the project name (must be unique).
 * [settings](sections#settings) `required`: defines the logging, seed, concurrent runs, search algorithm, early stopping, matrix hyper parameters.
 * [environment](sections#environment): defines the run environment, resources, node selectors, and distributed jobs definition.
 * [declarations](sections#declarations): defines variables/modules that can be reused.
 * [run](sections#run) `required`: defines the how the user can set a docker image and a command to execute.


## Plugins sections

 * [version](sections#version) `required`: defines the version of the file to be parsed and validated.
 * [kind](sections#kind) `required`: defines the kind of operation to run: plugin.
 * [project](sections#project) `required`: defines the project name (must be unique).
 * [environment](sections#environment): defines the run environment, resources, and node selectors.
 * [run](sections#run): defines the run step where the user can set a docker image and a command to execute.


## Model specific sections

 * [model](model_sections#model): defines the model to use based on the declarative API.
 * [train](model_sections#train): defines how to train a model and how to read the data.
 * [eval](model_sections#train): defines how to evaluate a modela how to read the data
