This section assumes that you have already familiarized yourself with the concept of [experiment_groups](experiment_groups).

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

In order to search a hyperparameter space, all search algorithms require a `settings` section,
they also share some subsections such as: `matrix` definition of hyperparameters, `early_stopping`, and `concurrency`.
Each one of this algorithms has a dedicated subsection to define the required options.

## Grid search

The grid search is the default algorithm used by Polyaxon in case no other algorithm is defined.
and it accepts one optional parameter `n_experiments` in case the user does not want to traverse the whole space search.

The grid search does not allow the use of distribution, and requires that all matrix definition are values or ranges.

Here's an example of a

```yaml
---
version: 1

kind: group

project:
  name: mnist

declarations:
  batch_size: 128

settings:
    matrix:
      lr:
        logspace: 0.01:0.1:5
      dropout:
        values: [0.2, 0.5]

run:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install scikit-learn
  cmd: python3 train.py --batch-size={{ batch_size }} --lr={{ lr }} --dropout={{ dropout }}
```

Other possible matrix options that can be found [here](/polyaxonfile_specification/sections#discrete-values).

The previous example will define 10 experiments based on the cartesian product of `lr` and `dropout` possible values.

We can restrict the number of experiments torun by using `n_experiments`,
the update version:


```yaml
---
version: 1

kind: group

project:
  name: mnist

declarations:
  batch_size: 128

settings:
    grid_search:
      n_experiments: 4

    matrix:
      lr:
        logspace: 0.01:0.1:5
      dropout:
        values: [0.2, 0.5]

run:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install scikit-learn
  cmd: python3 train.py --batch-size={{ batch_size }} --lr={{ lr }} --dropout={{ dropout }}
```

This updated example will create only 4 experiments from the total number of possible experiments.

## Random search

Random search requires a parameter `n_experiments`, this is essential because Polyaxon needs to know how many experiments to sample.

Here's an example of a

```yaml
---
version: 1

kind: group

project:
  name: mnist

declarations:
  batch_size: 128

settings:
    concurrency: 2

    random_search:
      n_experiments: 40

    matrix:
      lr:
        logspace: 0.01:0.1:5
      dropout:
        values: [0.2, 0.5]
      activation:
        pvalues: [[elu, 0.1], [relu, 0.2], [sigmoid, 0.7]]
      param1:
        uniform: [0, 1]

    early_stopping:
    - metric: accuracy
      value: 0.9
      optimization: maximize
    - metric: loss
      value: 0.05
      optimization: minimize

run:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install scikit-learn
  cmd: python3 train.py --batch-size={{ batch_size }} \
                        --lr={{ lr }} \
                        --dropout={{ dropout }} \
                        --activation={{ activation }} \
                        --param1={{ param1 }}
```

## Hyperband

Hyperband is a relatively new method for tuning iterative algorithms.
It performs random sampling and attempts to gain an edge by using time spent optimizing in the best way.

In order to configure this search algorithm correctly, you need to have as one of the hyperparameters,
a resource, this could be the number of steps or epochs, and a metric that you want to maximize or minimize.
You can also indicate if the experiments should be restarted from scratch or resumed from the last check point.

The way Hyperband works is by discarding poor performing
configurations leaving more resources for more promising configurations during the successive halving.
In order to use Hyperband correctly, you must define a metric called `resource` that the algorithm
will increase iteratively. Here's an example of resource definitions:

```yaml
resource:
  name: num_steps
  type: int
```

You can also have a resource with type float.

Another important concept is the metric to optimize, for example:

```yaml
metric:
  name: loss
  optimization: minimize
```

or

```yaml
metric:
  name: accuracy
  optimization: maximize
```

A complete definition of the settings section:

```yaml
...

settings:
  concurrency: 2

  hyperband:
    max_iter: 81
    eta: 3
    resource:
      name: num_steps
      type: int
    metric:
      name: loss
      optimization: minimize
    resume: False

  matrix:
    learning_rate:
      uniform: [0, 0.9]
    dropout:
      values: [0.25, 0.3]
    activation:
      pvalues: [[relu, 0.1], [sigmoid, 0.8]]
```

You can also use early stopping with hyperband:


```yaml
...

settings:
  concurrency: 2

  hyperband:
    max_iter: 81
    eta: 3
    resource:
      name: num_steps
      type: int
    metric:
      name: loss
      optimization: minimize
    resume: False

  matrix:
    learning_rate:
      uniform: [0, 0.9]
    dropout:
      values: [0.25, 0.3]
    activation:
      pvalues: [[relu, 0.1], [sigmoid, 0.8]]

  early_stopping:
    - metric: accuracy
      value: 0.9
      optimization: maximize
    - metric: loss
      value: 0.05
      optimization: minimize
```

## Bayesian Optimization

Bayesian optimization is an extremely powerful technique.
The main idea behind it is to compute a posterior distribution over the objective function based on the data,
and then select good points to try with respect to this distribution.

The way Polyaxon performs bayesian optimization is by measuring the expected increase in the maximum objective value
seen over all experiments in the group, given the next point we pick.

Since the bayesian optimization leverages previous experiments, the algorithm requires a metric to optimize (`maximize` or `minimize`).

To use bayesian optimization the user must define a utility function. This utility defines what acquisition function and bayesian process to use.

### Acquisition functions

A couple of acquisition functions can be used: `ucb`, `ei` or `poi`.

  * `ucb`: Upper Confidence Bound,
  * `ei`: Expected Improvement
  * `poi`: Probability of Improvement

When using `ucb` as acquisition function, a tunable parameter `kappa` is also required, to balance exploitation
against exploration, increasing kappa will make the optimized hyperparameters pursuing exploration.

When using `ei` or `poi` as acquisition function, a tunable parameter `eps` is also required,
to balance exploitation against exploration, increasing epsilon will
make the optimized hyperparameters are more spread out across the whole range.

### Gaussian process

Polyaxon allows to tune the gaussian process.

 * kernel: `matern` or `rbf`.
 * length_scale: float
 * nu: float
 * n_restarts_optimizer: int


Example :


```yaml
...

settings:
  concurrency: 2
  bo:
    n_iterations: 15
    n_initial_trials: 30
    metric:
      name: loss
      optimization: minimize
    utility_function:
      acquisition_function: ucb
      kappa: 1.2
      gaussian_process:
        kernel: matern
        length_scale: 1.0
        nu: 1.9
        n_restarts_optimizer: 0

  matrix:
    learning_rate:
      uniform: [0, 0.9]
    dropout:
      values: [0.25, 0.3]
    activation:
      pvalues: [[relu, 0.1], [sigmoid, 0.8]]
```

Example with early stopping:

```yaml
...

settings:
  concurrency: 2
  bo:
    n_iterations: 15
    n_initial_trials: 30
    metric:
      name: loss
      optimization: minimize
    utility_function:
      acquisition_function: ei
      eps: 1.2
      gaussian_process:
        kernel: rbf
        length_scale: 1.0
        nu: 1.9
        n_restarts_optimizer: 0

  matrix:
    learning_rate:
      uniform: [0, 0.9]
    dropout:
      values: [0.25, 0.3]
    activation:
      pvalues: [[relu, 0.1], [sigmoid, 0.8]]

  early_stopping:
    - metric: accuracy
      value: 0.9
      optimization: maximize
    - metric: loss
      value: 0.05
      optimization: minimize
```
