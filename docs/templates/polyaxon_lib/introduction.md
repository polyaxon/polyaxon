Polyaxon Lib is deep learning and reinforcement library that powers Polyaxon descriptive models.

## Polyaxon descriptive models

Polyaxon provides a way to build models without the need to code.

The model in general consist on the following information:

 * A model type
 * An optimizer
 * A loss function
 * A list of metrics
 * A graph consisting of connected layers
 * Inputs and outputs

Polyaxon then parses and build the model based on its specification, and start the training and/or evaluation.

The object behind this library is to provide a simple for train deep learning models, based on best practices.

``` caution
    Polyaxon Lib is currently still under heavy developement, and it's based on tensorflow.
    Future version, will include
        * benshmarking
        * models tuned to specific application
        * support for other deep learning frameworks
