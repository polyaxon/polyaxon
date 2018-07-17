The bookmark commands accept an optional argument `--username` or '-u'  to use a specific user.

If no user is provided, the command will default to the currently authenticated user.


Usage:

polyaxon bookmark [OPTIONS] COMMAND [ARGS]...

Commands for bookmark.

Options:

option | type | description
-------|------|------------
  -u, --username | TEXT | The username.
  --help |  | Show this message and exit.


## experiments

Usage:

```bash
polyaxon bookmark experiments [OPTIONS]
```

List bookmarked experiments for user.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon bookmark experiments
```

Options:

option | type | description
-------|------|------------
  --page | INTEGER | To paginate through the list of experiments.
  --help | | Show this message and exit.

## groups

Usage:

```bash
polyaxon bookmark groups [OPTIONS]
```

List bookmarked experiment groups for user.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon bookmark groups
```

Options:

option | type | description
-------|------|------------
  --page | INTEGER | To paginate through the list of groups.
  --help | | Show this message and exit.


## jobs

Usage:

```bash
polyaxon bookmark jobs [OPTIONS]
```

List bookmarked jobs for user.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon bookmark jobs
```

Options:

option | type | description
-------|------|------------
  --page | INTEGER | To paginate through the list of jobs.
  --help | | Show this message and exit.

## builds

Usage:

```bash
polyaxon bookmark builds [OPTIONS]
```

List bookmarked build jobs for user.

Uses [Caching](/polyaxon_cli/introduction#Caching)

Examples:

```bash
$ polyaxon bookmark builds
```

Options:

option | type | description
-------|------|------------
  --page | INTEGER | To paginate through the list of builds.
  --help | | Show this message and exit.
