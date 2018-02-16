The project commands accept an optional argument `--project` or '-p'  to use a specific project.

If no project is provided, the command will default to the currently initialized project.

If no project is provided and no project is cached, the command will raise.


Usage:

polyaxon notebook [OPTIONS] COMMAND [ARGS]...

Options:

option | type | description
-------|------|------------
  -p, --project | TEXT |
  --help | | Show this message and exit.


## Start

Usage:

```bash
$ polyaxon tensorboard start
```

Start a notebook deployment for this project.


Uses [Caching](/polyaxon_cli/introduction#Caching)

Options:

option | type | description
-------|------|------------
  -f, --file | PATH | The polyaxon files to run.
  -u | | To upload the repo before running.
  --help | | Show this message and exit.

## Stop

Usage:

```
$ polyaxon tensorboard stop
```

Stops the tensorboard deployment for this project if it exists.

Uses [Caching](/polyaxon_cli/introduction#Caching)
