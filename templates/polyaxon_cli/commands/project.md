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
  --description | TEXT | Description of the project,
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
$ polyaxon project get [OPTIONS] [PROJECT]
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
    $ polyaxon project get project
    ```

 * To get a project by user and name
    ```bash
    $ polyaxon project get user/project
    ```

## update

Usage:

```
$ polyaxon project update [OPTIONS] [PROJECT]
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

Options:

option | type | descrition
-------|------|-----------
  --name | TEXT | Name of the project, must be unique for the same user,
  --description | TEXT | Description of the project,
  --private | BOOLEAN | Set the visibility of the project to private/public.
  --help | | Show this message and exit.

## delete

Usage:
```bash
$ polyaxon project delete [OPTIONS] PROJECT
```

Delete project.

Uses [Caching](/polyaxon_cli/introduction#Caching)


## experiments

Usage:
```bash
$ polyaxon project experiments [OPTIONS] [PROJECT]
```

List experiments for this project.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Options:

option | type | description
-------|------|------------
  --page | INTEGER | To paginate through the list of experiments.
  --help | | Show this message and exit.

## groups

Usage:

```bash
$ polyaxon project groups [OPTIONS] [PROJECT]
```

List experiment groups for this project.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Options:

option | type | description
-------|------|------------
  --page | INTEGER | To paginate through the list of groups.
  --help | | Show this message and exit.
