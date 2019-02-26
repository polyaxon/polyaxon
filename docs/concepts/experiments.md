---
title: "Experiments"
sub_link: "experiments"
meta_title: "Experiments in Polyaxon - Core Concepts"
meta_description: "An Experiment is the execution of your model with data and the provided parameters on the cluster."
tags:
    - concepts
    - polyaxon
    - experimentation
    - experiments
    - architecture
sidebar: "concepts"
---

Assuming that you have already a [project](/concepts/projects/) created and initialized,
and you uploaded your code consisting of a single file `train.py` that accepts 2 parameters

  * learning rate `lr`
  * batch size `batch_size`

## Updating the polyaxonfile.yml

The first thing that you need to do is to update the default `polyaxonfile.yml` that was generated.

We will start first by adding the `run` section. For example if the code requires `tensorflow` and `sklearn`,
the polyaxonfile.yml `run` section could look something like this

```yaml
...

build
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install scikit-learn

run:
  cmd: python3 train.py --batch-size={{ batch_size }} --lr={{ lr }}
```

If the code requires many python dependencies, you can install these requirements by using a `requirements.txt` file,
instead of specifying every single library in the `build_steps` part of the `run` section,
we can create a requirements file, the name must be `requirements.txt` or `polyaxon_requirements.txt` and we need to add one command in the build_steps `pip install -r polyaxon_requirements.txt`.

You can also add any other executable script, the name must be `setup.sh` or `polyaxon_setup.sh` file, and a command to execute that file `./polyaxon_setup.sh`.

Let's create a `polyaxon_requirements.txt` to demonstrate this process.

```bash
$ vi polyaxon_requirements.txt
...
```

And modify the polyaxonfile.yml to install our requirements


```yaml
---
version: 1

kind: experiment

declarations:
  lr: 0.01
  batch_size: 128

build:
  image: tensorflow/tensorflow:1.4.1-py3
  build_steps:
    - pip install -r polyaxon_requirements.txt

run:
  cmd: python3 train.py --batch-size={{ batch_size }} --lr={{ lr }}
```

> The declarations section was not completely necessary, 
we could have also just passed the value directly `--batch-size=128 --lr=0.01`
For more information please visit the [declarations section](/references/polyaxonfile-yaml-specification/declarations/) reference.


> For more details about the `run section` check the [run section reference](/references/polyaxonfile-yaml-specification/run/)


To make sure that the polyaxon file is valid, you can run the following command,

```bash
$ polyaxon check -f polyaxonfile.yml -def

Polyaxonfile valid

This file has one independent experiment.
```

This command validate the polyaxon file, and the option `-def` returns the experiment definition,
in this case we have only one independent experiment.

In some case you will need to change the directory before running a command, or you might need to run multiple commands,
the best way to do that is to create an executable file,
e.g. `run.sh` where you will put all the commands you wish to run, and then just run that file:

For example the `run.sh` could be:

```bash
cd to_some_path; echo "running my run.sh file"; python model.py
```

And your cmd in polyaxonfile:

```yaml
run:
  cmd: /bin/bash run.sh
```

## Running an experiment

To run this polyaxonfile execute

```bash
$ polyaxon run

Creating an independent experiment.

Experiment was created.
```

> For more details about this command please run `polyaxon run --help`, 
or check the [command reference](/references/polyaxon-cli/run/)

## Checking the experiments of a project

We can check that the project has now an independent experiment created.
For that we can use Polyaxon dashboard or Polyaxon CLI,

```bash
$ polyaxon project experiments

Experiments for project `admin/mnist`.


Navigation:

-----  -
count  1
-----  -

Experiments:

  id  unique_name       user    project_name    experiment_group_name    last_status    created_at         is_clone      num_jobs  finished_at    started_at
----  ----------------  ------  --------------  -----------------------  -------------  -----------------  ----------  ----------  -------------  ------------
   1  admin.mnist.1      admin   admin.mnist                              Created        a few seconds ago  False                0

```

You should notice that the column experiment group is empty,
which means that this experiment is running independently of a group.


## Running the experiment with different parameters

After running this experiment, we can imagine that you were not satisfied with the result and
that you wanted to try another learning rate `0.5`.
If you hardcoded the value and passed it directly `--lr=0.01`, you would be obliged to updated the polyaxonfile.yml.
Of course we can do that also now, but since we declared the `lr` in the declarations sections,
we can create instead another file `polyaxonfile_override.yml` to override just that section:

> "You can call your polyaxonfiles anything you want"
 By default polyaxon commands look for files called `polyaxonfile.yml`.
 If you call your files differently or want to override values, you need to use the option `-f`

```bash
$ vi polyaxonfile_override.yml
```

And past the new declarations section.

```yaml
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

You can repeat this process as much as you wish until you are satisfied with the performance of your model.
Polyaxon will create a new experiment for you each time. However, if the space of values you want to try is large,
modifying the values manually and executing `polyaxon run` is not optimal,
what you can do instead is create an [experiment group](/concepts/experiment-groups/).

## Stopping an experiment

To stop experiment 2 for example, run

```bash
$ polyaxon experiment -xp 2 stop
```

<blockquote class="warning">
There's another command <code>delete</code>, 
the difference between <code>stop</code> and <code>delete</code>,
is that delete will remove the experiment completely from your database.
</blockquote>

## Restarting an experiment

To restart experiment 2 for example, run

```bash
$ polyaxon experiment -xp 2 restart
```

It will create a new experiment based on experiment 2 last saved checked point.

## Distributed Runs

<blockquote class="warning">
    This section is oriented for users who want to run experiments with multiple jobs, the example uses Tensorflow. 
    Polyaxon supports also MXNet, Pytorch, and Horovod,
    you can find more details in the <a href=" /integrations/distributed-training/">distributed experiments</a>'s section.
</blockquote>

After modifying our `train.py` we want to run the experiment with 1 master 4 workers and 1 parameter server.
We also want to customize the resources of each node.

First let's upload the new version of the code

```bash
$ polyaxon upload
```


> You can also execute `run` with `-u` option, to upload before resuming the run the command, In that case polyaxon upload is not necessary: `$ polyaxon run -f polyaxonfile.yml -u`

In order to customize the resources of our jobs we need to introduce a new section [environment](/references/polyaxonfile-yaml-specification/environment/).

Let's create a new `polyaxonfile_resources.yml` override file that will allow us to achieve that

```yaml
version: 1

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

     default_worker:
      resources:
        cpu:
          requests: 1
          limits: 2
        memory:
          requests: 256
          limits: 1024
        gpu:
          request: 1
          limits: 1

    worker:
      - index: 2
        resources:
          cpu:
            requests: 1
            limits: 2
          memory:
            requests: 256
            limits: 1024

    ps:
      - index: 0
        resources:
          cpu:
            requests: 1
            limits: 1
          memory:
            requests: 256
            limits: 1024

build:
  image: tensorflow/tensorflow:1.4.1-gpu-py3  # Update the image to use GPU
```

This is a lot of configuration, so let's take some time to understand what is happening here.

First of all, notice that we are overriding the image, the reason is that we want to use GPUs in this experiment.

In the environment section, we are describing how we want to perform our distributed run.
In this particular case, we are requesting 4 workers and one parameter server.
By default, Polyaxon always creates a master, so you must take that into consideration.

<blockquote class="warning">
A master is always created by polyaxon, you can only specify the workers and ps nodes.
</blockquote>

Also another thing you should know, is that by default, you can create all nodes without specifying the resources,
you only need to specify the resources to have more control over the created pods.

`resources` section defines the resources for the master node, i.e.  2 CPUs with a limit 4 CPUs, 0.5GB with a limit of 2GB.

For the workers, we have two ways to define resources, the `default_worker.resources` and
`worker_resources` that takes the index of the worker to define the resources for.

Here, we defined the default resources for our 4 workers in the `default_worker.resources`,
and provided a specific resources by index for the third worker, because we don't want to run that worker with gpu.

And finally we defined the resources requirement of our single ps node.
We could have also used `default_ps.resources` instead.

Since we have multiple jobs, Polyaxon adds the cluster definition to the docker container you will be running under the name `POLYAXON_CLUSTER`.

It also exposes some framework specific environment variables to the pods, in this case `TF_CONFIG` since we are running a Tensorflow distributed experiment.

You can also use our `tracking` api in `polyaxon-client` to extract these environment variables programmatically.

> Polyaxon export your cluster definition under environment variable name `POLYAXON_CLUSTER` 
Check how you can [get the cluster definition](/references/polyaxon-tracking-api/experiments/#tracking-experiments-running-inside-polyaxon/) to use it with your distributed deep learning model.

To run this distributed experiment, run

```bash
polyaxon run -f polyaxonfile.yml -f polyaxon_resources.yml

Creating an independent experiment.

Experiment was created.
```

Polyaxon currently supports distributed runs for Tensorflow, MXNet, Pytorch, and Horovod.
Please go to the [distributed experiments](/concepts/distributed-experiments/)'s section to learn more how
to configure your experiment for the different frameworks.

## Tracking experiment logs

To view the logs of experiment 2 for example, given that it is running now, run

```bash
$ polyaxon experiment -xp 2 logs
```

This command will show the logs in real time of all the jobs running for the experiment.
If you, however, need to check view the logs of a particular job, please check [experiment job's logs](/concepts/experiments/#experiment-jobs).

> 2 is the id of the experiment in this project, you can see it when running `polyaxon project experiments` in the id column.


## Tracking experiment resources

To view the resources of experiment 3 for example, given that it is running now, run

```bash
$ polyaxon experiment -xp 3 resources
```

This command will show the resources in real time of all the jobs running for the experiment.

If the experiment is running with GPU, and you want to see GPU metrics in real time, run

```bash
$ polyaxon experiment -xp 3 resources --gpu

or

$ polyaxon experiment -xp 3 resources -g
```

## Experiment jobs

The job is the running component of an experiment.
An experiment has at least one job.
If the experiment is running in a distributed way then it will have more than one job.

For distributed experiments, it is often difficult to follow the logs/resources of that experiments,
so the user might want to look at a specific job running in that experiment.

To check that the experiment is running in a distributed way,
you can use Polyaxon dashboard or Polyaxon CLI,

```bash
$ polyaxon experiment -xp 3 jobs

Jobs for experiment `3`.


Navigation:

-----  -
count  6
-----  -

Jobs:

id   role    experiment_name         last_status    created_at         started_at    finished_at    total_run
---  ------  ----------------------  -------------  -----------------  ------------  -------------  -----------
  1  master  admin.cats-vs-dogs.1.5  Running        a few seconds ago
  2  worker  admin.cats-vs-dogs.1.5  Running        a few seconds ago
  3  worker  admin.cats-vs-dogs.1.5  Running        a few seconds ago
  4  worker  admin.cats-vs-dogs.1.5  Running        a few seconds ago
  5  worker  admin.cats-vs-dogs.1.5  Running        a few seconds ago
  6  worker  admin.cats-vs-dogs.1.5  Running        a few seconds ago
  7  ps      admin.cats-vs-dogs.1.5  Building       a few seconds ago
```


## Getting experiment job info

To view the info of a specific job, you need to have the experiment id it belongs to, and the job id.


```bash
$ polyaxon job -xp 3 -j 1 get

Job resources:

resource      limits    requests
----------  --------  ----------
cpu                2           1
memory           200         100
gpu                1           1

Job info:

---------------  --------------------
id               1
role             master
experiment_name  root.quick-start.3
last_status      Succeeded
created_at       2 hours ago
updated_at       15 minutes ago
started_at       2 hours ago
finished_at      2 hours ago
total_run        10m 40s
---------------  --------------------
```

## Tracking experiment job logs

To view the logs of a specific job, you need to have the experiment is it belongs to, and the job id within that experiment.

For example

```bash
$ polyaxon job -xp 3 -j 1 logs
```

This command will show the logs of in real time for that job.

## Tracking experiment job resources

To view the resources of a specific job, you need to have the experiment id it belongs to, and the job id within that experiment.

For example

```bash
$ polyaxon job -xp 3 -j 1 resources
```

This command will show the resources in real time for that job.

If the job is running with GPU, and you want to see GPU metrics in real time, run

```bash
$ polyaxon job -xp 3 -j 1 resources --gpu

or

$ polyaxon job -xp 3 -j 1 resources -g
```

## Experiment job statuses

To view the chronological statuses of a specific job, you need to have the experiment id it belongs to, and the job id within that experiment.

```bash
$ polyaxon job -xp 3 -j 1 statuses

Statuses for Job `1`.


Navigation:

-----  -
count  6
-----  -

Statuses:

created_at    status     message
------------  ---------  ----------------------
2 hours ago   Created
2 hours ago   Building
2 hours ago   UNKNOWN    Unknown pod conditions
2 hours ago   Building   ContainerCreating
2 hours ago   Running
2 hours ago   Succeeded  Completed
```


> For more details about this command please run `polyaxon job --help`,
or check the [command reference](/references/polyaxon-cli/experiment/)


