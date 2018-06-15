The job is the running component of an experiment.
An experiment has at least one job.
If the experiment is running in a distributed way then it will have more than one job.

For distributed experiments, it is often difficult to follow the logs/resources of that experiments,
so the user might want to look at a specific job running in that experiment.

## Getting job info

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

## Tracking job logs

To view the logs of a specific job, you need to have the experiment is it belongs to, and the job id within that experiment.

For example

```bash
$ polyaxon job -xp 3 -j 1 logs
```

This command will show the logs of in real time for that job.

## Tracking job resources

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

## Job statuses

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


!!! info "More details"
    For more details about this command please run `polyaxon job --help`,
    or check the [command reference](/polyaxon_cli/commands/job)

