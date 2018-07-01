The experiment commands accept 2 optional arguments:

 * Experiment: `--experiment` or `-xp`  to use a specific experiment.
 * Project: `--project` or `-p`  to use a specific project.

If no project/experiment is provided, the command will default to the currently initialized project/last used experiment.

If no project/experiment is provided and no project/experiment is cached, the command will raise an error.

Usage:

polyaxon experiment [OPTIONS] COMMAND [ARGS]...

Commands for experiments.

Options:

option | type | description
-------|------|------------
  -p, --project | TEXT | The project name, e.g. 'mnist' or 'adam/mnist'.
  -xp, --experiment | INTEGER | The experiment id number.
  --help |  | Show this message and exit.

## get

Usage:

```bash
$ polyaxon experiment get
```

Get experiment or an experiment job.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples for getting an experiment:

```bash
$ polyaxon experiment get  # if experiment is cached
```

```bash
$ polyaxon experiment --experiment=1 get
```

```bash
$ polyaxon experiment -xp 1 --project=cats-vs-dogs get
```

```bash
$ polyaxon experiment -xp 1 -p alain/cats-vs-dogs get
```

Examples for getting an experiment job:

```bash
$ polyaxon experiment get -j 1  # if experiment is cached
```

```bash
$ polyaxon experiment --experiment=1 get --job=10
```

```bash
$ polyaxon experiment -xp 1 --project=cats-vs-dogs get -j 2
```

```bash
$ polyaxon experiment -xp 1 -p alain/cats-vs-dogs get -j 2
```

Options:

option | type | description
-------|------|------------
  -j, --job | INTEGER |  The job id.
  --help | | Show this message and exit.


## stop

Usage:

```bash
$ polyaxon experiment stop
```

Stop experiment.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon experiment stop
```

```bash
$ polyaxon experiment -xp 2 stop
```

Options:

option | type | description
-------|------|------------
  -y, --yes | Flag |  Automatic yes to prompts. Assume "yes" as answer to all prompts and run non-interactively.
  --help | | Show this message and exit.


## update

Usage:

```bash
$ polyaxon experiment update
```

Update experiment.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon experiment -xp 2 update --description="new description for my experiments"
```

```bash
$ polyaxon experiment -xp 2 update --tags="foo, bar" --name="unique-name"
```

Options:

option | type | description
-------|------|------------
  --name [optional] | TEXT | Name of the experiment, must be unique within the project.
  --description [optional] | TEXT | Description of the experiment.
  --tags [optional] | TEXT | Tags, comma separated values, of the experiment.
  --help | | Show this message and exit

## delete

Usage:

```bash
$ polyaxon experiment delete
```

Delete experiment.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Example:

```bash
$ polyaxon experiment delete
```

## restart

Usage:

```bash
$ polyaxon experiment restart
```

Restart experiment.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon experiment --experiment=1 restart
```

Options:

option | type | description
-------|------|------------
  -c, --copy | | To copy the experiment before restarting.
  -f, --file | PATH | The polyaxon files to update with.
  -u | | To upload the repo before restarting.
  --help | | Show this message and exit.

## resume

Usage:

```bash
$ polyaxon experiment resume
```

Resume experiment.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon experiment --experiment=1 resume
```

Options:

Options:
  -f, --file | PATH |  The polyaxon files to update with.
  -u | | To upload the repo before resuming.
  --help | | Show this message and exit.

## jobs

Usage:

```bash
$ polyaxon experiment jobs [OPTIONS]
```

List jobs for experiment.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon experiment --experiment=1 jobs
```

Options:

option | type | description
-------|------|------------
  --page | INTEGER | To paginate through the list of jobs.
  --help | | Show this message and exit.

## logs

Usage:

```bash
$ polyaxon experiment logs
```

Get experiment or experiment job logs.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples for getting experiment logs:

```bash
$ polyaxon experiment logs
```

```bash
$ polyaxon experiment logs --past --follow
```

```bash
$ polyaxon experiment -xp 10 -p mnist logs
```

Examples for getting experiment job logs:

```bash
$ polyaxon experiment -xp 1 -j 1 logs
```

Options:

option | type | description
-------|------|------------
  -j, --job | INTEGER | The job id.
  --past | |  Show the past logs.
  --follow | | Stream logs after showing past logs.
  --help | | Show this message and exit.

## resources

Usage:

```bash
$ polyaxon experiment resources
```

Get experiment or experiment job resources.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples for getting experiment resources:

```bash
$ polyaxon experiment -xp 19 resources
```

For GPU resources

```bash
$ polyaxon experiment -xp 19 resources --gpu
```

Examples for getting experiment job resources:

```bash
$ polyaxon experiment -xp 19 resources -j 1
```

For GPU resources

```bash
$ polyaxon experiment -xp 19 resources -j 1 --gpu
```

Options:

option | type | description
-------|------|------------
  -j, --job | INTEGER | The job id.
  -g, --gpu | Flag | List experiment GPU resources.
  --help | | Show this message and exit.


## statuses

Usage:

```bash
$ polyaxon experiment statuses [OPTIONS]
```

Get experiment or experiment job statuses.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples getting experiment statuses:

```bash
$ polyaxon experiment statuses
```

```bash
$ polyaxon experiment -xp 1 statuses
```

Examples getting experiment job statuses:

```bash
$ polyaxon experiment statuses -j 3
```

```bash
$ polyaxon experiment -xp 1 statuses --job 1
```


Options:

option | type | description
-------|------|------------
  -j, --job | INTEGER | The job id.
  --page | INTEGER | To paginate through the list of statuses.
  --help | | Show this message and exit.

## outputs

Usage:

```bash
$ polyaxon experiment outputs [OPTIONS]
```

Download outputs for experiment.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon experiment -xp 1 outputs
```
