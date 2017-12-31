Assuming that you have already a [project](projects) created and initialized,
and you uploaded your code consisting of a single file `train.py` that accepts 2 parameters

  * learning rate `lr`
  * batch size `batch_size`

## Updating the polyaxonfile.yml

The first that you need to do is to update the default `polyaxonfile.yml` that was generated.

We need to set the required information, for example if the code requires `tensorflow` and `sklearn`,
the polyaxonfile.yml `run` section should look something like this

```yaml
---
...

run:
  image: tensorflow/tensorflow:1.4.1-py3
  steps:
    - pip install scikit-learn
  cmd: python3 train.py --batch_size="{{ batch_size }}" --lr="{{ lr }}"
```

If the code requires many python dependencies, Polyaxon provides an elegant way to install these requirements,
instead of specifying every single library in the `steps` part of the `run` section,
we can create a requirements file with the name `polyaxon_requirements.txt` and just create one command in the steps `pip install -r polyaxon_requirements.txt`
and Polyaxon will automatically detect it and install the requirements.

Polyaxon also allows you to specify a `polyaxon_setup.sh` file, and a command to execute that file `./polyaxon_setup.sh`.

Let's create a `polyaxon_requirements.txt` to demonstrate this process.

```bash
$ vi polyaxon_requirements.txt
...
```

And let's modify the polyaxonfile.yml to install our requirements


```yaml
---
version: 1

project:
  name: mnist

declarations:
  lr: 0.01
  batch_size: 128

run:
  image: tensorflow/tensorflow:1.4.1-py3
  steps:
    - pip install -r polyaxon_requirements.txt
  cmd: python3 train.py --batch_size="{{ batch_size }}" --lr="{{ lr }}"
```

!!! Tip
    The declarations section was not completely necessary,
    we could have also just passed the value directly `--batch_size=128 --lr=0.01`

    For more information please visite the [declarations section](/polyaxonfile_specification/sections#declarations) reference.

To make sure that the polyaxon file is valid you can execute it, we can run

```bash
$ polyaxon check -f polyaxonfile.yml -m

Polyaxonfile valid

This file has one independent experiment.
```

This command validate the polyaxon file, and the option `-m` returns the matrix space,
in this case we have only independent experiment. This option is important when we want
to check a polyaxonfile with a matrix section having an [experiment group](experiment_groups)

## Running an experiment

To run this polyaxonfile execute

```bash
$ polyaxon run

Creating an independent experiment.

Experiment was created.
```

!!! info
    For more details about this command please run `polyaxon run --help`,
    or check the [command reference]()

## Checking the experiments of a project

We can check the project has now an independent experiment created.

 * Polyaxon dashboard
 * Polyaxon CLI

```bash
$ polyaxon project experiments

Experiments for project `admin/mnist`.


Navigation:

-----  -
count  1
-----  -

Experiments:

  sequence  unique_name       user    project_name    experiment_group_name    last_status    created_at         is_clone      num_jobs  finished_at    started_at
----------  ----------------  ------  --------------  -----------------------  -------------  -----------------  ----------  ----------  -------------  ------------
        1  admin.mnist.1      admin   admin.mnist                              Created        a few seconds ago  False                0

```

You should notice that the column experiment group is empty,
which means that this experiment is running independently of a group.


## Running the experiment with different parameters

After running this experiment we were not satisfied with the result and we want to try another learning rate `0.5`.
If we hardcoded the value and passed it directly `--lr=0.01` we should have updated the polyaxonfile.yml.
Of course we can do that also now, but since we declared the `lr` in the declarations sections,
we can create instead an `polyaxonfile_override.yml` to override just that section:

!!! Tip "You can call your polyaxonfiles anything you want"
    By default polyaxon commands looks for files called `polyaxonfile.yml`
    so if you call your file differently you should always use the option `-f`

```bash
$ vi polyaxonfile_override.yml
```

And past the new declarations section.

```yaml
---
version: 1

declarations:
  lr: 0.5
```

and run again

```bash
$ polyaxon run -f polyaxonfile.yml -f polyaxonfile_override.yml

Creating an independent experiment.

Experiment was created.
```

If we again were not satisfied with this learning rate, we can modify the value and run the polyaxon file again.
Polyaxon will create a new experiment for you. If the space of values you want to try is large,
modifying the value manually and executing run is not optimal,
what you can do instead is create an [experiment group](experiment_groups).

## Stopping an experiment

To stop experiment 2 for example, run

```bash
polyaxon experiment stop 2
```

!!! caution
    There's another command `delete`, the difference between `stop` and `delete`,
    is that delete will remove the experiment completely from your database.

## Distributed Runs

!!! caution
    This is section is oriented for users who want to running experiments with multiple jobs
    based on Tensorflow.

After modifying our `train.py` we want to run the experiment with 1 master 4 workers and 1 parameter server.
We also want to customize the resources of the each node.

In that case we need to introduce a new [environment section](), in order to that.

Let's create a new `polyaxonfile_resources.yml` override file that will allow us to achieve that

```yaml
---
version: 1

environment:
  n_workers: 4
  n_ps: 1
  delay_workers_by_global_step: true
  resources:
    cpu:
      requests: 2
      limits: 4
    memory:
      requests: 512
      limits: 2048

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

run:
  image: tensorflow/tensorflow:1.4.1-py3
```

This is a lot of configuration, so let's take some time to understand what is happening here.

First of all, notice that we are overriding the image, that's because we want to use GPUs in this experiment.

In the environment section, we are describing how we want to perform our distributed run.
In this particular case, we are requesting 4 workers and one parameter server.
By default Polyaxon always creates a master, so you must take that into consideration.

??? danger "Polyaxon always creates a master"
    A master is always created by polyaxon, you can only specify the workers and ps nodes.

The default resources for all nodes is what we defined in the first `resources` section, i.e.  2 CPUs with a limit 4 CPUs, 0.5GB with a limit of 2GB.

Since we do not want to run our workers with the default `resources`,
we defined again what is the default resources for our 4 workers in the `default_worker_resources`,
and provided a specific resources by index for the third worker, because we don't want to run that worker with gpu.

And finally we defined the resources requirement of our single ps node.
We could have also used `default_ps_resources` instead.

To run this distributed experiment, run

```bash
polyaxon run -f polyaxonfile.yml -f polyaxon_resources.yml

Creating an independent experiment.

Experiment was created.
```


## Experiment jobs

To check that our experiment is running in a distributed way

 * Polyaxon dashboard
 * Polyaxon CLI

```bash
$ polyaxon experiment jobs 3

Jobs for experiment `3`.


Navigation:

-----  -
count  6
-----  -

Jobs:

uuid                              role    experiment_name         last_status    created_at         started_at    finished_at    total_run
--------------------------------  ------  ----------------------  -------------  -----------------  ------------  -------------  -----------
40465c7cca4f55bca1f98abc2bf8c770  master  admin.cats-vs-dogs.1.5  Running        a few seconds ago
7660e37608274b9e98fcfeee89dc7e29  worker  admin.cats-vs-dogs.1.5  Running        a few seconds ago
024d2b1a51b750a7838132213e89f08b  worker  admin.cats-vs-dogs.1.5  Running        a few seconds ago
1652e9c51c7f45e085b16040ef2dee45  worker  admin.cats-vs-dogs.1.5  Running        a few seconds ago
de32c613b1c752948cbb92ce7a33f0b6  worker  admin.cats-vs-dogs.1.5  Running        a few seconds ago
6ca34c69e4544fdca85fb625c1a114a5  worker  admin.cats-vs-dogs.1.5  Running        a few seconds ago
027ac27d7f5754ffbaf6081e6b657e93  ps      admin.cats-vs-dogs.1.5  Building       a few seconds ago
```

For more information about jobs, please refer to [jobs](jobs)

## Tracking experiment logs

To view the logs of experiment 3 for example, given that is running now, run

!!! note
    3 is the sequence of the experiment in this project,
    you can see it when running `polyaxon project experiments` in the sequence column.


```bash
polyaxon experiment logs 2
```

This command will show the logs of the experiment in real time of all the jobs running.
In the [jobs](jobs)'s page, we will see how we can view the logs of a particular job.

## Tracking experiment resources

To view the resources of experiment 3 for example, given that is running now, run

```bash
polyaxon experiment resources 3
```

This command will show the resources of the experiment in real time of all the jobs running.
In the [jobs](jobs)'s page, we will see how we can view the resources of a particular job.


!!! info
    For more details about this command please run `polyaxon experiment --help`,
    or check the [command reference]()

If you did not see the [jobs](jobs)'s section, please go there,
to see how you can get specific information about a particular job.
