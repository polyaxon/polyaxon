---
title: "Bookmark"
sub_link: "polyaxon-cli/bookmark"
meta_title: "Polyaxonfile Command Line Interface Specification - Bookmark - Polyaxon References"
meta_description: "Polyaxonfile Command Line Interface Specification - Bookmark."
visibility: public
status: published
tags:
    - cli
    - reference
    - polyaxon
    - bookmark
sidebar: "polyaxon-cli"
---

> The commands in this sections can be used for all Polyaxon deployment types (i.e. it does not require a scheduler)

> You can always access the help menu for this command by adding `--help`

The bookmark commands accept an optional argument `--username` or `-u`  to use a specific user.

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

Uses [Caching](/references/polyaxon-cli/#caching)

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

Uses [Caching](/references/polyaxon-cli/#caching)

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

Uses [Caching](/references/polyaxon-cli/#caching)

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

Uses [Caching](/references/polyaxon-cli/#caching)

Examples:

```bash
$ polyaxon bookmark builds
```

Options:

option | type | description
-------|------|------------
  --page | INTEGER | To paginate through the list of builds.
  --help | | Show this message and exit.
