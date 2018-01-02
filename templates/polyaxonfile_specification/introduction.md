In order to use Polyaxon, users need to create YAML polyaxonfiles.
These files use a specification to describe how experiments should run on Polyaxon.

The Polyaxon specification is based on a list of sections, in this guide, we describe the required and optional sections.

!!! note
    Polyaxon specification can parse both YAML and Json format.


## Sections

 * [version](sections#version): defines the version of the file to be parsed and validated.
 * [project](sections#project): defines the project name this specification belongs to (must be unique).
 * [settings](sections#settings): defines the logging, run type and concurrent runs.
 * [environment](sections#environment): defines the run environment for experiment.
 * [matrix](sections#matrix): hyper parameters matrix definition.
 * [declarations](sections#declarations): variables/modules that can be reused.
 * [run](sections#run): defines the run step where the user can set a docker image to execute


## Model specific Sections

 * [model](model_sections#model): defines the model to use based on the declarative API.
 * [train](model_sections#train)sec: defines how to train a model and how to read the data.
 * [eval](model_sections#train): defines how to evaluate a modela how to read the data
