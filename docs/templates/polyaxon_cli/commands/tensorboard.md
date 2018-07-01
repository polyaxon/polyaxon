The tensorboard commands accept 3 optional arguments:

 * Experiment: `--experiment` or `-xp`  to use a specific experiment.
 * Experiment Group: `--group` or `-g`  to use a specific experiment group.
 * Project: `--project` or `-p`  to use a specific project.

If no project is provided, the command will default to the currently initialized project.

If no project is provided and no project is cached, the command will raise an error.


Usage:

polyaxon tensorboard [OPTIONS] COMMAND [ARGS]...

Options:

option | type | description
-------|------|------------
  -p, --project | TEXT |
  -g, --group | INTEGER | The group id number.
  -xp, --experiment | INTEGER | The experiment id number.
  --help | | Show this message and exit.


## start

Usage:

```bash
$ polyaxon tensorboard start
```

Start a tensorboard deployment for project/experiment/experiment group.

Project tensorboard will aggregate all experiments under the project.

Experiment group tensorboard will aggregate all experiments under the
group.

Experiment tensorboard will show all metrics for an experiment.

Uses [Caching](/polyaxon_cli/introduction#Caching)


Example: using the default tensorflow image 1.4.1.

```bash
$ polyaxon tensorboard start
```

Example: with custom image and resources

```bash
$ polyaxon tensorboard start -f file -f file_override ...
```

Example: starting a tensorboard for an experiment group

```bash
$ polyaxon tensorboard -g 1 start -f file
```

Example: starting a tensorboard for an experiment

```bash
$ polyaxon tensorboard -xp 112 start -f file
```

Options:

option | type | description
-------|------|------------
  -f, --file | PATH | The polyaxon files to run.
  --help | | Show this message and exit.


## stop

Usage:

```
$ polyaxon tensorboard stop
```

Stops the tensorboard deployment for project/experiment/experiment group if it exists.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples: stopping project tensorboard

```bash
$ polyaxon tensorboard stop
```

Examples: stopping experiment group tensorboard

```bash
$ polyaxon tensorboard -g 1 stop
```

Examples: stopping experiment tensorboard

```bash
$ polyaxon tensorboard -xp 112 stop
```

option | type | description
-------|------|------------
  -y, --yes | Flag |  Automatic yes to prompts. Assume "yes" as answer to all prompts and run non-interactively.
  --help | | Show this message and exit.


## url

Prints the tensorboard url for project/experiment/experiment group.

Uses [Caching](/polyaxon_cli/introduction#Caching)

 Examples for project tensorboards:

```bash
$ polyaxon tensorboard url
```

```bash
$ polyaxon tensorboard -p mnist url
```

Examples for experiment tensorboards:

```bash
$ polyaxon tensorboard -xp 1 url
```

Examples for experiment group tensorboards:

```bash
$ polyaxon tensorboard -g 1 url
```
