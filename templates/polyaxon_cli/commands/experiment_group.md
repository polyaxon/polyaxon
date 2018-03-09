The experiment group commands accept 2 optional arguments:

 * Experiment Group: `--group` or `-g`  to use a specific experiment group.
 * Project: `--project` or `-p` to use a specific project.

If no project/group is provided, the command will default to the currently initialized project/last used group.

If no project/group is provided and no project/group is cached, the command will raise.

Usage:

polyaxon group [OPTIONS] COMMAND [ARGS]...

Commands for groups.

Options:

option | type | description
-------|------|------------
  -p, --project | TEXT | The project name, e.g. 'mnist' or 'adam/mnist'.
  -g, --group | INTEGER | The group sequence number.
  --help |  | Show this message and exit.


## get

Usage:

```bash
$ polyaxon group get
```

Get experiment group by uuid.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon group -g 13 get
```

## update

Usage:

```
$ polyaxon group update [OPTIONS]
```

Update experiment group.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Example:

```bash
$ polyaxon group -g 2 update --description="new description for my experiments"
```

Options:

option | type | description
-------|------|------------
  --description | TEXT | Description of the project
  --help | | Show this message and exit

## delete

Usage:

```bash
$ polyaxon group delete
```

Delete experiment group.

Uses [Caching](/polyaxon_cli/introduction#Caching)

## experiments

Usage:

```bash
$ polyaxon group experiments [OPTIONS]
```

List experiments for this experiment group

Uses [Caching](/polyaxon_cli/introduction#Caching)

option | type | description
-------|------|------------
  --page | INTEGER | To paginate through the list of experiments.
  -m, --metrics | Flag | List experiments with their metrics.
  --help | | Show this message and exit.

## stop

Stop [all | pending] experiments in the group

Usage: 

```bash
polyaxon group stop [OPTIONS]
```

Uses [Caching](/polyaxon_cli/introduction#Caching)


Examples: stop only pending experiments

```bash
$ polyaxon group stop --pending
```

Examples: stop all unfinished

```bash
$ polyaxon group stop
```

```bash
$ polyaxon group -g 2 stop
```

Options:
  --pending  To stop only pending experiments, i.e. leave currently running
             one intact.
  --help     Show this message and exit.

option | type | description
-------|------|------------
  --pending | Flag | To stop only pending experiments, i.e. leave currently running one intact.
  --help | | Show this message and exit.
