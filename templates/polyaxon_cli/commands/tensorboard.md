The project commands accept an optional argument `--project` or '-p'  to use a specific project.

If no project is provided, the command will default to the currently initialized project.

If no project is provided and no project is cached, the command will raise.


Usage:

polyaxon tensorboard [OPTIONS] COMMAND [ARGS]...

Options:

option | type | description
-------|------|------------
  -p, --project | TEXT |
  --help | | Show this message and exit.


## start

Usage:

```bash
$ polyaxon tensorboard start
```

Example with custom image and resources

```bash
$ polyaxon tensorboard start -f file -f file_override ...
```

Start a tensorboard deployment for this project. It will show all experiments under the project.


Uses [Caching](/polyaxon_cli/introduction#Caching)


## stop

Usage:

```
$ polyaxon tensorboard stop
```

Stops the tensorboard deployment for this project if it exists.

Uses [Caching](/polyaxon_cli/introduction#Caching)


option | type | description
-------|------|------------
  -y, --yes | Flag |  Automatic yes to prompts. Assume "yes" as answer to all prompts and run non-interactively.
  --help | | Show this message and exit.


## url

Prints the tensorboard url for this project.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Example:

```
$ polyaxon tensorboard url
```
