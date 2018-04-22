This section assumes that you have already familiarized yourself with the concept of [experiment_groups](experiment_groups).

Hyperparameters selection is crucial for creating robust models,
since they heavily influence the behavior of the learned model.
Finding good hyperparameters involves can be very challenging,
and requires to efficiently search the space of possible hyperparameters as well as h
ow to manage a large set of experiments for hyperparameter tuning.

The way Polyaxon performs hyperparameters tuning is by providing to the data scientists a selection of search algorithms,
Polyaxon supports both simple approaches such as `random search` and `grid search`, but it also provides a simple interface for
to advance approaches, such as `Hyperband` and `Bayesian Optimization`.

All these search algorithms run in an asynchronous way, and support concurrency to leverage your cluster's resources to the maximum.

Some of these approaches are also iterative and improve based on previous experiments.

In order to search a hyperparameter space, all search algorithms require a `settings` section,
they also share some subsections such as: `matrix` definition of hyperparameters, `early_stopping`, and `concurrency`.
Each one of this algorithms has a dedicated subsection to define the required options.

# Grid search

The grid search is the default algorithm used by Polyaxon in case no other algorithm is defined.
and it has support one optional parameter `n_experiments` in case the user does not want to traverse the whole space search.

The grid search does not allow the use of distribution, and requires that all matrix definition are wither values or ranges.

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

Other possible matrix options that can be used are:


 * `values`: [value1, value2, value3, ...]
 * `range`: [start, stop, step]
 * `logspace`: [start, stop, step]
 * `linspace`: [start, stop, num]
 * `geomspace`: [start, stop, num]

The previous example will define 10 experiments based on the cartesian product of `lr` and `dropout` possible values.

We can restrict the number of experiments to be created and tried by using `n_experiments`,
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

# Random search

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

### Hyperband

Hyperband is a relatively new method for tuning iterative algorithms.
It performs random sampling and attempts to gain an edge by using time spent optimizing in the best way.

In order to configure this search algorithm correctly, you need to have as one of the hyperparameters,
a resource, this could be the number of steps or epochs, and metric that you want to maximize or minimize.

Example:

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

### Bayesian Optimization

Bayesian optimization is an extremely powerful technique.
The main idea behind it is to compute a posterior distribution over the objective function based on the data,
and then select good points to try with respect to this distribution.

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
