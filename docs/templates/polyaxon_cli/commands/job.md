The experiment commands accept 2 optional arguments:

 * Job: `--job` or `-j`  to use a specific job.
 * Experiment: `--experiment` or `-xp`  to use a specific experiment.
 * Project: `--project` or `-p`  to use a specific project.

If no project/experiment/job is provided, the command will default to the currently initialized project/last used experiment/last used job.

If no project/experiment/job is provided and no project/experiment/job is cached, the command will raise.

Usage:

polyaxon job [OPTIONS] COMMAND [ARGS]...

Commands for jobs.

Options:

option | type | description
-------|------|------------
  -p, --project | TEXT | The project name, e.g. 'mnist' or 'adam/mnist'.
  -xp, --experiment | INTEGER | The id number of the experiment.
  -j, --job | INTEGER | The job id.
  --help |  | Show this message and exit.


## get

Usage:

```bash
$ polyaxon job get
```

Get job.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon job --job=1 --experiment=1 get
```

```bash
$ polyaxon job --job=1 --project=project_name get
```

## logs

Usage:

```bash
$ polyaxon job logs
```

Get job logs.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon job -xp 3 -j 2 logs
```

```bash
$ polyaxon job logs
```


## resources

Usage:

```bash
$ polyaxon job resources [OPTIONS]
```

Get job resources.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon job -j 2 resources
```

For GPU resources

\b
```bash
$ polyaxon job -j 2 resources --gpu
```


Options:

option | type | description
-------|------|------------
  -g, --gpu | Flag | List job GPU resources.
  --help | | Show this message and exit.


## statuses

Usage:

```bash
$ polyaxon job statuses [OPTIONS]
```

Get job status.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon job -xp 1 -j 2 statuses
```
