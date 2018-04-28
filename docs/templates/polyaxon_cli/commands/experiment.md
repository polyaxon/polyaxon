The experiment commands accept 2 optional arguments:

 * Experiment: `--experiment` or `-xp`  to use a specific experiment.
 * Project: `--project` or `-p`  to use a specific project.

If no project/experiment is provided, the command will default to the currently initialized project/last used experiment.

If no project/experiment is provided and no project/experiment is cached, the command will raise.

Usage:

polyaxon experiment [OPTIONS] COMMAND [ARGS]...

Commands for experiments.

Options:

option | type | description
-------|------|------------
  -p, --project | TEXT | The project name, e.g. 'mnist' or 'adam/mnist'.
  -xp, --experiment | INTEGER | The experiment sequence number.
  --help |  | Show this message and exit.

## get

Usage:

```bash
$ polyaxon experiment get
```

Get experiment.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

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

option | type | description
-------|------|------------
  -y, --yes | Flag |  Automatic yes to prompts. Assume "yes" as answer to all prompts and run non-interactively.
  --help | | Show this message and exit.


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

Get experiment logs.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon experiment logs
```

```bash
$ polyaxon experiment logs --past --follow
```

```bash
$ polyaxon experiment -xp 10 -p mnist logs
```

Options:

option | type | description
-------|------|------------
  --past | |  Show the past logs.
  --follow | | Stream logs after showing past logs.
  --help | | Show this message and exit.

## resources

Usage:

```bash
$ polyaxon experiment resources
```

Get experiment resources.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Example:

```bash
$ polyaxon experiment -xp 19 resources
```

For GPU resources

```bash
$ polyaxon experiment -xp 19 resources --gpu
```

Options:

option | type | description
-------|------|------------
  -g, --gpu | Flag | List experiment GPU resources.
  --help | | Show this message and exit.


## statuses

Usage:

```bash
$ polyaxon experiment statuses [OPTIONS]
```

Get experiment status.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Example:

```bash
$ polyaxon experiment statuses 3
```

```bash
$ polyaxon experiment -xp 1 statuses
```

Options:

option | type | description
-------|------|------------
  --page | INTEGER | To paginate through the list of statuses.
  --help | | Show this message and exit.

## outputs
