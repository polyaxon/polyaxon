The job is the running component of an experiment.
An experiment has at least one job.
If the experiment is running in a distributed way then it will have more than one job.

For distributed experiments, it is often difficult to follow the logs/resources of that experiments,
so the user might want to look at a specific job running in that experiment.

## Tracking job logs

To view the logs of a specific job, you need to have the experiment sequence it belongs to, and the job sequence within that experiment.

For example

```bash
polyaxon job -xp 3 -j 1 logs
```

This command will show the logs of in real time for that job.

## Tracking job resources

To view the resources of a specific job, you need to have the experiment sequence it belongs to, and the job sequence within that experiment.

For example

```bash
polyaxon job -xp 3 -j 1 resources
```

This command will show the resources in real time for that job.

## Information and statuses

You can also get the information about the job and its statuses chronologically.

!!! info "More details"
    For more details about this command please run `polyaxon job --help`,
    or check the [command reference](/polyaxon_cli/commands/job)

