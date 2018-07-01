The experiment group commands accept 2 optional arguments:

 * Experiment Group: `--group` or `-g`  to use a specific experiment group.
 * Project: `--project` or `-p` to use a specific project.

If no project/group is provided, the command will default to the currently initialized project/last used group.

If no project/group is provided and no project/group is cached, the command will raise an error.

Usage:

polyaxon group [OPTIONS] COMMAND [ARGS]...

Commands for groups.

Options:

option | type | description
-------|------|------------
  -p, --project | TEXT | The project name, e.g. 'mnist' or 'adam/mnist'.
  -g, --group | INTEGER | The group id number.
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

```bash
$ polyaxon update --tags="foo, bar"
```

Options:

option | type | description
-------|------|------------
  --name [optional] | TEXT | Name of the group, must be unique within the project.
  --description [optional] | TEXT | Description of the experiment group.
  --tags [optional] | TEXT | Tags, comma separated values, of the experiment group.
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

List experiments for this experiment group. Supports sorting and querying.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Options:

option | type | description
-------|------|------------
  -m, --metrics | | List experiments with their metrics.
  -d, --declarations | | List experiments with their declarations/params.
  -q, --query| TEXT | To filter the experiments based on this query spec.
  -s, --sort | TEXT | To change order by of the experiments.
  --page | INTEGER | To paginate through the list of experiments.
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
  -y, --yes | Flag |  Automatic yes to prompts. Assume "yes" as answer to all prompts and run non-interactively.
  --help | | Show this message and exit.


## statuses

Usage:

```bash
polyaxon group statuses
```

Get experiment group statuses.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon group -g 2 statuses
```

Options:

option | type | description
-------|------|------------
  --page | INTEGER | To paginate through the list of statuses.
  --help | | Show this message and exit.
