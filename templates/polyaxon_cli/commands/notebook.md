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
$ polyaxon notebook start
```

Start a notebook deployment for this project.


Uses [Caching](/polyaxon_cli/introduction#Caching)


Example:

Example specifying the polyaxonfile

```bash
$ polyaxon notebook start -f file -f file_override ...
```

Example upload before running

```bash
$ polyaxon -p user12/mnist notebook start -f file -u
```

Options:

option | type | description
-------|------|------------
  -f, --file | PATH | The polyaxon files to run.
  -u | | To upload the repo before running.
  --help | | Show this message and exit.

## Stop

Usage:

```
$ polyaxon notebook stop
```

Stops the notebook deployment for this project if it exists.

Uses [Caching](/polyaxon_cli/introduction#Caching)


option | type | description
-------|------|------------
  -y, --yes | Flag |  Automatic yes to prompts. Assume "yes" as answer to all prompts and run non-interactively.
  --help | | Show this message and exit.


## Url

Prints the notebook url for this project.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Example:

```bash
$ polyaxon notebook url
```
