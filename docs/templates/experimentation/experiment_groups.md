Assuming that you have already a [project](projects) created and initialized,
and you uploaded your code consisting of a single file `train.py` that accepts 2 parameters

  * learning rate `lr`
  * batch size `batch_size`

If you want to run this code with different learning rate  `lr` values,
you can use the [matrix section](/polyaxonfile_specification/sections#matrix) to declare the values you want to run.

## Updating the polyaxonfile.yml with a matrix

The first thing you need to do is to update the default `polyaxonfile.yml` that was generated.

You need set the required information, for example if the code requires `tensorflow` and `sklearn`,
the polyaxonfile.yml `run` section could look something like this

```yaml
---
...

run:
  image: tensorflow/tensorflow:1.4.1-py3
  steps:
    - pip install scikit-learn
  cmd: python3 train.py --batch-size={{ batch_size }} --lr={{ lr }}
```

This declares a section to run our `train.py` file by passing two values, the `learning rate` and the `batch_size`.

!!! info "More details"
    For more details about the `run section` check the [run section reference](/polyaxonfile_specification/sections#run)

Now you need to declare this values, and for that you will add 2 more sections to the polyaxonfile.yml

 * A [declarations section](/polyaxonfile_specification/sections#declarations), to declare a constant value for `batch_size`
 * A [matrix section](/polyaxonfile_specification/sections#matrix), to declare the values for `lr`

The new `polyaxonfile.yml` after the update

```yaml
---
version: 1

project:
  name: mnist

declarations:
  batch_size: 128

matrix:
  lr:
    logspace: 0.01:0.1:5

run:
  image: tensorflow/tensorflow:1.4.1-py3
  steps:
    - pip install scikit-learn
  cmd: python3 train.py --batch-size={{ batch_size }} --lr={{ lr }}
```

!!! Tip
    The declarations section was not completely necessary,
    we could have also just passed the value directly `--batch-size=128`

So what we did is we declared a constant value for `batch_size`, and a value for `lr` going from `0.01` to `0.1` with `5` steps spaced evenly on a `log scale`.

There are other options that we could have used such as

 * `values`: [value1, value2, value3]
 * `range`: [start, stop, step]
 * `linspace`: [start, stop, num]
 * `geomspace`: [start, stop, num]

You can check all the options available on the [matrix section reference](/polyaxonfile_specification/sections#matrix).

To make sure that the polyaxon file is valid, and creates multiple values for `lr`, we can run the following

```bash
$ polyaxon check -f polyaxonfile.yml -m

Polyaxonfile valid

The matrix definition is:
{'lr': 1.0232929922807541}
{'lr': 1.0777052536943219}
{'lr': 1.1350108156723151}
{'lr': 1.1953635256737185}
{'lr': 1.2589254117941673}
```

This command validate the polyaxon file, and the option `-m` returns the matrix space.

!!! info "More details"
    For more details about this command please run `polyaxon check --help`,
    or check the [command reference](/polyaxon_cli/commands/check)

!!! tip "Polyaxon merges the combination values from matrix for a single experiment with the values from declarations and export under the environment variable name `POLYAXON_DECLARATIONS`"
    Check how you can [get the experiment declarations](/reference_polyaxon_helper) to use them with your models.

## Running a group of experiments

To run this polyaxonfile execute

```bash
$ polyaxon run

Creating an experiment group with 5 experiments.

Experiment group was created
```

!!! info "More details"
    For more details about this command please run `polyaxon run --help`,
    or check the [command reference](/polyaxon_cli/commands/run)

Now one thing we did not discuss is how many experiments we want to run in parallel,
and how we want to perform the hyperparameters search. Be default, Polyaxon
will schedule your experiments sequentially and also go through the matrix space sequentially.

We could have checked that with the check command before

```bash
polyaxon check -f polyaxonfile.yml -x

The matrix-space has 5 experiments, with sequential runs
```


## Running concurrent experiments

Now imagine we have enough resources on our cluster to run experiments in parallel.
And we want to run 2 experiments concurrently, and explore the space randomly instead of sequentially.

For this purpose we need a new [settings section](/polyaxonfile_specification/sections#settings).

Although we can modify the `polyaxonfile.yml` to include this new section,
we will do something different this time and override this value with a new file, same way you would do with `docker/docker-compose`.

Create a new file, let's call polyaxonfile_override.yml

!!! Tip "You can call your polyaxonfiles anything you want"
    By default polyaxon commands look for files called `polyaxonfile.yml`.
    If you call your files differently or want to override values, you need to use the option `-f`

```bash
$ vi polyaxonfile_override.yml
```

And past the following settings section.

```yaml

---
version: 1

settings:
  concurrent_experiments: 2
  search_method: random
```

If we run again the `check` command with `-x` or `--experiments` option, we will get

```bash
polyaxon check -f polyaxonfile.yml -f polyaxonfile_override.yml -x

Polyaxonfile valid

The matrix-space has 5 experiments, with 2 concurrent runs, and a random search
```

Let's run our new version

```bash
$  polyaxon run -f polyaxonfile.yml -f polyaxonfile_override.yml

Creating an experiment group with 5 experiments.

Experiment group was created
```

## Maximum number of experiments

Sometimes you don't wish to explore the matrix space exhaustively. 
In that case, you can define a maximum number of experiments to explore form the matrix space.
The value must be of course less than the total number of experiments in the matrix space, 
or a float value between 0 and 1 defining a percentage of the total number of experiments.

In order to activate this option, you must update your polyaxonfile's `settings` section with `n_experiments`


```yaml

---
version: 1

settings:
  concurrent_experiments: 2
  search_method: random
  n_experiments: 4
```

This will start a maximum of 4 experiments in this group independently of how big is the total number of experiments in matrix space.

Or, alternatively you can provide a percentage:

```yaml

---
version: 1

settings:
  concurrent_experiments: 2
  search_method: random
  n_experiments: 0.4
```

This will start 40% of total number of experiments.


## Early stopping

Another way to stop the exhaustive search is to provide a condition for early stopping.
Obviously in this case early stopping is only responsible for the number of experiments to run.
For an early stopping related to the number of steps or epochs, you should be able to provide such logic in your code.

In order to activate this option, you must update your polyaxonfile's `settings` section with `early_stopping`

```yaml

---
version: 1

settings:
  concurrent_experiments: 2
  search_method: random
  n_experiments: 4
  early_stopping:
    - metric: accuracy
      value: 0.9
      optimization: maximize
    - metric: loss
      value: 0.05
      optimization: minimize
```

In this case, the scheduler will not start any more experiment, if one of the experiments in the group validate the following condition:
 
 * An accuracy >= 0.9
 * Or a loss <= 0.05

## Checking the status of your experiments

First, we can double check that our groups was created.

For that you can use the Polyaxon dashboard or Polyaxon CLI.

```bash
$ polyaxon project groups

Experiment groups for project `admin/mnist`.


Navigation:

-----  -
count  2
-----  -

Experiment groups:

  sequence  unique_name    project_name    created_at           concurrency    num_experiments    num_pending_experiments    num_running_experiments
----------  -------------  --------------  -----------------  -------------  -----------------  -------------------------  -------------------------
         1  admin.mnist.1  admin.mnist     a few seconds ago              1                  5                          4                          1
         2  admin.mnist.2  admin.mnist     a few seconds ago              2                  5                          3                          2
```

We can see that we created 2 groups, the first one with sequential runs, and the second one with 2 concurrent runs.

We can also see the how many experiments are running/pending now.

We can have a look at the the two experiment running concurrently in the second group

Again you can go to the Polyaxon dashboard or use the Polyaxon CLI.

```bash
polyaxon group -g 2 experiments

Experiments for experiment group `2`.


Navigation:

-----  -
count  5
-----  -

Experiments:

  sequence  unique_name       user    last_status    created_at         is_clone      num_jobs  finished_at    started_at
----------  ----------------  ------  -------------  -----------------  ----------  ----------  -------------  -----------------
         6  admin.mnist.2.6   admin   Created        a few seconds ago  False                0
         7  admin.mnist.2.7   admin   Created        a few seconds ago  False                0
         8  admin.mnist.2.8   admin   Starting       a few seconds ago  False                0                 a few seconds ago
         9  admin.mnist.2.9   admin   Created        a few seconds ago  False                0
        10  admin.mnist.2.10  admin   Building       a few seconds ago  False                0                 a few seconds ago
```

!!! info "More details"
    For more details about this command please run `polyaxon group --help`,
    or check the [command reference](/polyaxon_cli/commands/experiment_group)


To check the logs, resources, jobs, and statuses of a specific experiment, please go to [experiments](experiments).
The section also covers how to customize the resources of an experiment, the configuration,
the log level and many important information.

All the information that you will learn in that section applies to experiment groups,
because groups are only a collection of experiments.

In the experiments section, you will also see how you can execute a single experiment without concurrency.
