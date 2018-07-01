The project commands accept an optional argument `--project` or '-p'  to use a specific project.

If no project is provided, the command will default to the currently initialized project.

If no project is provided and no project is cached, the command will raise an error.


Usage:

polyaxon project [OPTIONS] COMMAND [ARGS]...

Commands for projects.

Options:

option | type | description
-------|------|------------
  -p, --project | TEXT | The project name, e.g. 'mnist' or 'adam/mnist'
  --help |  | Show this message and exit.


## create

Usage:

```
$ polyaxon project create [OPTIONS]
```

Create a new project.

Example:

```
$ polyaxon project create \
    --name=cats-vs-dogs \
    --description="Image Classification with Deep Learning"
```

Options:

option | type | description
-------|------|------------
  --name [required] | TEXT | Name of the project, must be unique for the same user
  --description | TEXT | Description of the project.
  --tags | TEXT | Tags, comma separated values, of the project.
  --private | | Set the visibility of the project to private.
  --help | | Show this message and exit.

## list

Usage:

```bash
$ polyaxon project list [OPTIONS]
```

List projects.

Options:

option | type | description
-------|------|------------
  --page | INTEGER | To paginate through the list of projects.
  --help | | Show this message and exit.

## get

Usage:

```bash
$ polyaxon project get [OPTIONS]
```

Get info for current project, by project_name, or user/project_name.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

 * To get current project:

   ```bash
   $ polyaxon project get
   ```

 * To get a project by name

    ```bash
    $ polyaxon project --project=project_name get
    ```

 * To get a project by user and name
    ```bash
    $ polyaxon project -p user/project get
    ```

## update

Usage:

```
polyaxon project update [OPTIONS]
```

Update project.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Example:

```bash
$ polyaxon update foobar --description="Image Classification with Deep Learning using TensorFlow"
```

```bash
$ polyaxon update mike1/foobar --description="Image Classification with Deep Learning using TensorFlow"
```

```bash
$ polyaxon update --tags="foo, bar"
```

Options:

option | type | descrition
-------|------|-----------
  --name | TEXT | Name of the project, must be unique for the same user,
  --description | TEXT | Description of the project.
  --tags | TEXT | Tags, comma separated values, of the project.
  --private | BOOLEAN | Set the visibility of the project to private/public.
  --help | | Show this message and exit.


## delete

Usage:

```bash
polyaxon project delete
```

Delete project.


## download

Usage:

```bash
polyaxon project download
```

Download code of the current project.


## experiments

Usage:

```bash
polyaxon project experiments [OPTIONS]
```

List experiments for this project.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

Get all experiments:

```bash
$ polyaxon project experiments
```

Get all experiments with with status {created or running}, and creation
date between 2018-01-01 and 2018-01-02, and declarations activation equal
to sigmoid and metric loss less or equal to 0.2

```bash
$ polyaxon project experiments -q "status:created|running, started_at:2018-01-01..2018-01-02, declarations.activation:sigmoid, metric.loss:<=0.2"
```

Get all experiments sorted by update date

```bash
$ polyaxon project experiments -s "-updated_at"
```

Options:

option | type | description
-------|------|------------
  -m, --metrics | | List experiments with their metrics.
  -d, --declarations | | List experiments with their declarations/params.
  -i, --independent | | To return only independent experiments.
  -g, --group| INTEGER | To filter experiments for a specific group.
  -q, --query| TEXT | To filter the experiments based on this query spec.
  -s, --sort | TEXT | To change order by of the experiments.
  --page | INTEGER | To paginate through the list of experiments.
  --help | | Show this message and exit.

## groups

Usage:

```bash
polyaxon project groups [OPTIONS]
```

List experiment groups for this project.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

Get all groups:

```bash
$ polyaxon project groups
```

Get all groups with with status {created or running}, and creation date
between 2018-01-01 and 2018-01-02, and search algorithm not in {grid or
random search}

```bash
$ polyaxon project groups -q "status:created|running, started_at:2018-01-01..2018-01-02, search_algorithm:~grid|random"
```

Get all groups sorted by update date

```bash
$ polyaxon project groups -s "-updated_at"
```

Options:

option | type | description
-------|------|------------
  -q, --query| TEXT | To filter the groups based on this query spec.
  -s, --sort | TEXT | To change order by of the groups.
  --page | INTEGER | To paginate through the list of groups.
  --help | | Show this message and exit.


## jobs

Usage:

```bash
polyaxon project jobs [OPTIONS]
```

List jobs for this project.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

Get all jobs:

```bash
$ polyaxon project jobs
```

Get all jobs with with status not in {created or running}

```bash
$ polyaxon project jobs -q "status:~created|running"
```

Get all jobs with with status failed

```bash
$ polyaxon project jobs -q "status:failed"
```

Get all jobs sorted by update date

```bash
$ polyaxon project jobs -s "-updated_at"
```

Options:

option | type | description
-------|------|------------
  -q, --query| TEXT | To filter the jobs based on this query spec.
  -s, --sort | TEXT | To change order by of the jobs.
  --page | INTEGER | To paginate through the list of jobs.
  --help | | Show this message and exit.

## builds

Usage:

```bash
polyaxon project builds [OPTIONS]
```

List build jobs for this project.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

Get all builds:

```bash
$ polyaxon project builds
```

Get all builds with with status not in {created or running}

```bash
$ polyaxon project builds -q "status:~created"
```

Get all builds with with status failed

```bash
$ polyaxon project builds -q "status:failed"
```

Get all builds sorted by update date

```bash
$ polyaxon project builds -s "-updated_at"
```

Options:

option | type | description
-------|------|------------
  -q, --query| TEXT | To filter the builds based on this query spec.
  -s, --sort | TEXT | To change order by of the builds.
  --page | INTEGER | To paginate through the list of builds.
  --help | | Show this message and exit.


## tensorboards

Usage:

```bash
polyaxon project tensorboards [OPTIONS]
```

Usage: polyaxon project tensorboards [OPTIONS]

List tensorboard jobs for this project.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Options:

option | type | description
-------|------|------------
  -q, --query| TEXT | To filter the tensorboards based on this query spec.
  -s, --sort | TEXT | To change order by of the tensorboards.
  --page | INTEGER | To paginate through the list of tensorboards.
  --help | | Show this message and exit.
