The build commands accept 2 optional arguments:

 * Build: `--build` or `-b` to use a specific build.
 * Project: `--project` or `-p`  to use a specific project.

If no project/build is provided, the command will default to the currently initialized project/last used build.

If no project/build is provided and no project/build is cached, the command will raise an error.

Usage:

polyaxon build [OPTIONS] COMMAND [ARGS]...

Commands for build jobs.

Options:

option | type | description
-------|------|------------
  -p, --project | TEXT | The project name, e.g. 'mnist' or 'adam/mnist'.
  -b, --build | INTEGER | The build job id.
  --help |  | Show this message and exit.


## get

Usage:

```bash
$ polyaxon build get
```

Get build job.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon build -b 1 get
```

```bash
$  polyaxon build --build=1 --project=project_name get
```

## stop

Usage:

```bash
$ polyaxon build stop
```

Stop build job.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon build stop
```

```bash
$ polyaxon build -b 2 stop
```

Options:

option | type | description
-------|------|------------
  -y, --yes | Flag |  Automatic yes to prompts. Assume "yes" as answer to all prompts and run non-interactively.
  --help | | Show this message and exit.


## update

Usage:

```bash
polyaxon build update [OPTIONS]
```

Update build job.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Example:

```bash
$ polyaxon build -b 2 update --description="new description for my build"
```

Options:

option | type | description
-------|------|------------
--name | TEXT | Name of the build, must be unique within the project, could none.
--description | TEXT |  Description of the build.
--tags | TEXT |  Tags of the build, comma separated values.
--help | | Show this message and exit.

## delete

Usage:

```bash
$ polyaxon build delete
```

Delete build job.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Example:

```bash
$ polyaxon build delete
```

```bash
$ polyaxon build -b 2 delete
```


## logs

Usage:

```bash
$ polyaxon build logs
```

Get build logs.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon build -b 2 logs
```

```bash
$ polyaxon build logs
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
$ polyaxon build resources
```

Usage: polyaxon build resources [OPTIONS]

Get build job resources.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon build -b 2 resources
```

For GPU resources

```bash
$ polyaxon build -b 2 resources --gpu
```

Options:

option | type | description
-------|------|------------
  -g, --gpu | Flag | List experiment GPU resources.
  --help | | Show this message and exit.


## statuses

Usage:

```bash
$ polyaxon build statuses
```


Get build job statuses.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon build -b 2 statuses
```

Options:

option | type | description
-------|------|------------
  --page | INTEGER | To paginate through the list of statuses.
  --help | | Show this message and exit.
