The job commands accept 2 optional arguments:

 * Job: `--job` or `-j`  to use a specific job.
 * Project: `--project` or `-p`  to use a specific project.

If no project/job is provided, the command will default to the currently initialized project/last used job.

If no project/job is provided and no project/job is cached, the command will raise an error.

Usage:

polyaxon job [OPTIONS] COMMAND [ARGS]...

Commands for jobs.

Options:

option | type | description
-------|------|------------
  -p, --project | TEXT | The project name, e.g. 'mnist' or 'adam/mnist'.
  -j, --job | INTEGER | The job id.
  --help |  | Show this message and exit.


## get

Usage:

```bash
$ polyaxon job get
```

Get job.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon job --job=1 get
```

```bash
$ polyaxon job -j 1 --project=project_name get
```

## stop

Usage:

```bash
$ polyaxon job stop
```

Stop job.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon job stop
```

```bash
$ polyaxon job -j 2 stop
```

Options:

option | type | description
-------|------|------------
  -y, --yes | Flag |  Automatic yes to prompts. Assume "yes" as answer to all prompts and run non-interactively.
  --help | | Show this message and exit.


## update

Usage:

```bash
polyaxon job update [OPTIONS]
```

Update job.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Example:

```bash
$ polyaxon job -j 2 update --description="new description for my job"
```

Options:

option | type | description
-------|------|------------
--name | TEXT | Name of the job, must be unique within the project, could none.
--description | TEXT |  Description of the job.
--tags | TEXT |  Tags of the job, comma separated values.
--help | | Show this message and exit.

## delete

Usage:

```bash
$ polyaxon job delete
```

Delete job.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Example:

```bash
$ polyaxon job delete
```

```bash
$ polyaxon job -j 2 delete
```


## restart

Usage:

```bash
$ polyaxon job restart
```

Restart job.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon job --job=1 restart
```

Options:

option | type | description
-------|------|------------
  -c, --copy | | To copy the job before restarting.
  -f, --file | PATH | The polyaxon files to update with.
  -u | | To upload the repo before restarting.
  --help | | Show this message and exit.


## logs

Usage:

```bash
$ polyaxon job logs
```

Get job logs.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon job -j 2 logs
```

```bash
$ polyaxon job logs --past --follow
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
$ polyaxon job resources
```

Usage: polyaxon job resources [OPTIONS]

Get job resources.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon job -j 2 resources
```

For GPU resources

```bash
$ polyaxon job -j 2 resources --gpu
```

Options:

option | type | description
-------|------|------------
  -g, --gpu | Flag | List experiment GPU resources.
  --help | | Show this message and exit.


## statuses

Usage:

```bash
$ polyaxon job statuses
```


Get job statuses.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon job -j 2 statuses
```

Options:

option | type | description
-------|------|------------
  --page | INTEGER | To paginate through the list of statuses.
  --help | | Show this message and exit.


## outputs

Usage:

```bash
$ polyaxon job outputs [OPTIONS]
```

Download outputs for job.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon job -xp 1 outputs
```
