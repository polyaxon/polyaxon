Assuming that you have already a [project](projects) created and initialized,
and you uploaded your code consisting of a single file `train.py` that accepts 2 parameters

  * learning rate `lr`
  * batch size `batch_size`

If you want to run this code with learning rate `lr` with different values,
you can use the [matrix](/polyaxonfile_specification/sections#matrix) to declare the values you want to run.

## Updating the polyaxonfile.yml with a matrix

The first thing you need to do is to update the default `polyaxonfile.yml` that was generated.

You need set the required information, for example if the code requires `tensorflow` and `sklearn`,
the polyaxonfile.yml `run` section should look something like this

```yaml
---
...

run:
  image: tensorflow/tensorflow:1.4.1-py3
  install:
    - pip install scikit-learn
  cmd: python3 train.py --batch_size="{{ batch_size }}" --lr="{{ lr }}"
```

This declares a section to run our `train.py` file by passing two values, the `learning rate` and the `batch_size`.

!!! info
    For more details about the `run` check the [run section reference](/polyaxonfile_specification/sections#run)

Now you need to declare this values, and for that you will add 2 more sections to the polyaxonfile.yml

 * [declarations section](/polyaxonfile_specification/sections#declarations), to declare a constant value for `batch_size`
 * [matrix](/polyaxonfile_specification/sections#matrix) section, to declare the values for `lr`

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
  install:
    - pip install scikit-learn
  cmd: python3 train.py --batch_size="{{ batch_size }}" --lr="{{ lr }}"
```

!!! Tip
    The declarations section was not completely necessary,
    we could have also just passed the value directly `--batch_size=128`

So what we did is, we declared a constant value for `batch_size`, and a value for `lr` going from `0.01` to `0.1` with `5` steps spaced evenly on a `log scale`.

In fact there's other options that we could have used such as

 * `values`: [value1, value2, value3]
 * `range`: [start, stop, step]
 * `linspace`: [start, stop, num]
 * `GeomSpace`: [start, stop, num]

You can check all the options available on the [matrix](/polyaxonfile_specification/sections#matrix)

To make sure that the polyaxon file is valid you can execute, and creates a multiple values for `lr`, we can run

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

## Running a group of experiments

To run this polyaxonfile execute

```bash
$ polyaxon run

Creating an experiment group with 5 experiments.

Experiment group was created
```

!!! info
    For more details about this command please run `polyaxon run --help`,
    or check the [command reference]()

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

For this purpose we need a new [section settings](/polyaxonfile_specification/sections#settings).

Although we can modify the `polyaxonfile.yml` to include this new section,
we will do something different this time and override this value with a new file, same way you would do with `docker/docker-compose`.

Create a new file, let's call polyaxonfile_override.yml

!!! Tip "You can call your polyaxonfiles anything you want"
    By default polyaxon commands looks for files called `polyaxonfile.yml`
    so if you call your file differently you should always use the option `-f`

```bash
$ vi polyaxon_override.yml
```

And past this settings section.

```yaml
---
version: 1

settings:
  concurrent_experiments: 2
  search_method: random
```

If we run again the `check` command with `-x` or `--experiments` option, we will get

```yaml
polyaxon check -f polyaxonfile.yml -f polyaxon_override.yml -x

Polyaxonfile valid

The matrix-space has 5 experiments, with 2 concurrent runs, and random search
```

Let's run our new version

```bash
$  polyaxon run -f polyaxonfile.yml -f polyaxon_override.yml

Creating an experiment group with 5 experiments.

Experiment group was created
```

## Checking the status of your experiments

First of we can double check that our groups were created.

 * Polyaxon dashboard
 * Polyaxon CLI

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

We can have a look at the the two experiment running concurrently in the second group


 * Polyaxon dashboard
 * Polyaxon CLI

```bash
polyaxon group experiments 2

Experiments for experiment group `2`.


Navigation:

-----  -
count  5
-----  -

Experiments:

  sequence  unique_name       user    experiment_group_name    last_status    created_at         is_clone      num_jobs  finished_at    started_at
----------  ----------------  ------  -----------------------  -------------  -----------------  ----------  ----------  -------------  -----------------
         6  admin.mnist.2.6   admin   admin.mnist.2            Created        a few seconds ago  False                0
         7  admin.mnist.2.7   admin   admin.mnist.2            Created        a few seconds ago  False                0
         8  admin.mnist.2.8   admin   admin.mnist.2            Starting       a few seconds ago  False                0                 a few seconds ago
         9  admin.mnist.2.9   admin   admin.mnist.2            Created        a few seconds ago  False                0
        10  admin.mnist.2.10  admin   admin.mnist.2            Building       a few seconds ago  False                0                 a few seconds ago
```

!!! info
    For more details about this command please run `polyaxon group --help`,
    or check the [command reference]()


To check the logs, resources, jobs, and statuses of a specific experiment, please go to [experiments](experiments).

In the experiments section, you will also see how you can execute a single experiment without concurrency.
The section also covers how to customize the resources of an experiment, the configuration,
the log level and other many more important information.
All the information that you will learn in that section applies to experiment groups,
because groups are only a collection of experiments.
