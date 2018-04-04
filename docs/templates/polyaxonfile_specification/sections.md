## Version

Represents the polyaxon file specification version.

Example:

```yaml
version: 1
```

## project

Represents the project namespace where we want to run the polyaxonfile.
The project must be [created on Polyaxon](/experimentation/projects##create-a-project).

This section requires one attribute name, which is the name of the project.
You can specify the name of the project in 2 different ways:

 * short version: `project_name`, in this case the username is inferred automatically as the current logged in user.
 * long version: `username/project_name` in this case the project is uniquely defined.

Example:

```yaml
project:
  name: mnist
```

```yaml
project:
  name: adam/mnist
```

## settings

Settings defines `run_type`, `concurrent_experiments`, `search_method`, `n_experiments`, `early_stopping`, and `logging`.
In general the settings defines some values that must be unique for
all experiments created based on the polyaxonfile.

### run_type

Currently polyaxon supports three different run types:

 * `kubernetes` (default value): If your cluster is running on Kubernetes.
 * `minikube`: if your cluster is running on a minikube.
 * `local`: In this case the polyaxonfile is supposed to be used with `polyaxon-lib`.

### concurrent_experiments

Defines how many experiments to run concurrently when the polyaxon file use a `matrix` section.
This option will be ignored if the polyaxon file only have one independent experiment.

### search_method

Same as `concurrent_experiments`, it defines the search method to use when running hyperparameters search.
Currently, the supported methods are:

 * `sequential` (default value)
 * `random`

!!! info
    More options will be provided for this subsection, to allow the user to explore the matrix space with advanced algorithms.

### n_experiments

Defined the maximum number of experiments to run during the exploration of the matrix space.

The `n_experiments` must be less that total matrix space to explore.

You can also provide a percent, i.e. a float value between 0 and 1, e.g. 0.4 this will translate to 40% of the total matrix space.

Default value is `None` which means will translate to an exhaustive search.

Example:

Value 

```yaml
n_experiments: 10
```

Percentage 

```yaml
n_experiments: 0.3
```

### early_stopping

Defines a list of metrics and the values for these metrics to stop the search algorithm.

Example:

```yaml
early_stopping:
  - metric: loss
    value: 0.01
    optimization: minimize

  - metric: accuracy
    value: 0.97
    optimization: maximize
```

### logging

Defines the logging behavior for your execution, this subsection accepts:

 * `level`: The log level.
 * `formatter`: The log formatter regex.


Example:

```yaml
settings:
  logging:
    level: INFO
  run_type: minikube
```

```yaml
settings:
  logging:
    level: WARNING
  run_type: kubernetes
  concurrent_experiments: 5
```

## Environment

The environment section allows to alter the
resources and configuration of the runtime of your experiments.

Based on this section you can define, how many workers/ps you want to run,
the resources and configs of each job.

The values of this section are:

### resources

The resources to use for the job. In the case of distributed run, its the resources to use for the master job.
A resources definition, is optional and made of three optional fields:

 * cpu: {limits: value, requests: value}
 * memory: {limits: value, requests: value}
 * gpu: {limits: value, requests: value}
 
To enable a distributed run, the user can define one of the following framework:

### tensorflow

#### n_workers

The number of workers to use for an experiment.

#### n_ps

The number of parameter server to use for an experiment.

#### default_worker_resources

If specified, it will be the default workers resources.

#### default_ps_resources

If specified, it will be the default ps resources.

#### worker_resources

Defines a specific resources definition for a worker indicated by the index of the worker.

#### ps_resources

Defines a specific resources definition for a ps indicated by the index of the ps.


Example:

```yaml

environment:

  resources:
    cpu:
      requests: 2
      limits: 4
    memory:
      requests: 512
      limits: 2048

  tensorflow:
      n_workers: 4
      n_ps: 1
      default_worker_resources:
        cpu:
          requests: 1
          limits: 2
        memory:
          requests: 256
          limits: 1024
        gpu:
          request: 1
          limits: 1
    
      worker_resources:
        - index: 2
          cpu:
            requests: 1
            limits: 2
          memory:
            requests: 256
            limits: 1024
    
      ps_resources:
        - index: 0
          cpu:
            requests: 1
            limits: 1
          memory:
            requests: 256
            limits: 1024
```

### mxnet

#### n_workers

The number of workers to use for an experiment.

#### n_ps

The number of parameter server to use for an experiment.

#### default_worker_resources

If specified, it will be the default workers resources.

#### default_ps_resources

If specified, it will be the default ps resources.

#### worker_resources

Defines a specific resources definition for a worker indicated by the index of the worker.

#### ps_resources

Defines a specific resources definition for a ps indicated by the index of the ps.


Example:

```yaml

environment:
  mxnet:
    n_workers: 4
    n_ps: 1
```

### pytorch

#### n_workers

The number of workers to use for an experiment.

#### default_worker_resources

If specified, it will be the default workers resources.

#### worker_resources

Defines a specific resources definition for a worker indicated by the index of the worker.

Example:

```yaml

environment:
  pytorch:
    n_workers: 4
```

### horovod

#### n_workers

The number of workers to use for an experiment.

#### default_worker_resources

If specified, it will be the default workers resources.

#### worker_resources

Defines a specific resources definition for a worker indicated by the index of the worker.

Example:

```yaml

environment:
  horovod:
    n_workers: 4
```

## declarations

This section is the appropriate place to declare constants and variables
that will be used by the rest of our specification file.

To declare a simple constant value:

```yaml
declarations:
  batch_size: 128
```

Or value named with a list or nested values:

```yaml
declarations:
  layer_units: [100, 200, 10]
```

```yaml
declarations:
  convolutions:
    conv1:
       kernels: [32, 32]
       size: [2, 2]
       strides: [1, 1]
    conv2:
       kernels: [64, 64]
       size: [2, 2]
       strides: [1, 1]
```

This declaration can be used to pass values to our program:

```yaml
 ... --batch-size={{ batch-size }}
```

```yaml
--unit1="{{ layer_units[0] }}" --unit2="{{ layer_units[1] }}" --unit3="{{ layer_units[2] }}"
```


```yaml
--conv1_kernels="{{ convolutions.conv1.kernels }}" --conv1_stides="{{ convolutions.conv1.strides }}" ...
```

The double-brackets is important and indicate that we want to use our declaration.

The declaration are particularly important for descriptive models.

All your declaration will be exported under the environment variable name `POLYAXON_DECLARATIONS`.

!!! tip "Polyaxon export your declarations under environment variable name `POLYAXON_DECLARATIONS`"
    Check how you can [get the experiment declarations](/reference_polyaxon_helper) to use them with your models.


## matrix

The matrix section works the same way as travisCI matrix section,
and it basically creates multiple specifications.
The way it does that is by traversing the matrix space defined by the Cartesian Product of all your defined parameters.

The matrix also defines variables same way the `declarations` does, the only difference is
that all the values generated by the matrix contribute to the definition of an experiment group.
Each experiment in this group is defined based on a combination of the values declared in the matrix.

The matrix is defined as `{key: value}` object where the key is the name of the parameter
you are defining and the value is one of these options:

 * `values`: a list of values, e.g. `[1, 2, 3, 4]`
 * `range`: [start, stop, step] same way you would define a range in python., e.g. `[1, 10, 2]` or `{start: 1, stop: 10, step: 2}` or `'1:10:2'`
 * `linspace`: [start, stop, num] steps from start to stop spaced evenly on a `linear scale`.
 * `logspace`: [start, stop, num] steps from start to stop spaced evenly on a `log scale`
 * `geomspace`: [start, stop, num] steps from start to stop, numbers spaced evenly on a log scale (a geometric progression).

Example:

```yaml
matrix:
  lr:
    logspace: 0.01:0.1:5

  loss:
    values: [MeanSquaredError, AbsoluteDifference]
```

These values can be accessed in the following way:

```yaml
--lr={{ lr }} --loss={{ loss }}
```

You can, of course, only access one value at time,
and the value is chosen directly by the algorithm doing the search defined in the `search_method`.

For each experiment generated during the hyperparameters search, Polyaxon will also add these values
to your declarations, and will as well export them under the environment variable name `POLYAXON_DECLARATIONS`.

!!! tip "Polyaxon append the matrix value combination to your declarations and export them under the environment variable name `POLYAXON_DECLARATIONS`"
    Check how you can [get the cluster definition](/reference_polyaxon_helper) to use it with your models.

## run

This is where you define how you want to run your code, and the requirements needed to run it.
This section defines the following values/subsections:

 * image [required]: the base image polyaxon will use to build an image for you to run your code.
 * steps [optional]: steps are basically a list of ops that Polyaxon use with docker
 `RUN` to install/run further operations you define in the list.
 * envs [optional]: envs are also a list of tuples of 2 elements, that polyaxon will use to add env variables in the docker image.
 * cmd [required]: The command to run during the execution of your code.

```yaml
run:
  image: my_image
  steps:
    - pip install PILLOW
    - pip install scikit-learn
  cmd: video_prediction_train --num_masks=1
```
