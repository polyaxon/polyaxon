The experiment group commands accept 2 optional arguments
 * Experiment: `--group` or '-g'  to use a specific experiment group.
 * Project: `--project` or '-p'  to use a specific project.

If no project/group is provided, the command will default to the currently initialized project/last used group.

If no project/group is provided and no project/group is initialized, the command will raise.

Usage:

polyaxon group [OPTIONS] COMMAND [ARGS]...

Commands for groups.

Options:

option | type | description
-------|------|------------
  -p, --project | TEXT | The project name, e.g. 'mnist' or 'adam/mnist'
  -g, --group | INTEGER | The sequence number of the group
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
  --help | | Show this message and exit.
