---
title: "User"
sub_link: "polyaxon-cli/user"
meta_title: "Polyaxonfile Command Line Interface Specification - User - Polyaxon References"
meta_description: "Polyaxonfile Command Line Interface Specification - User."
visibility: public
status: published
tags:
    - cli
    - reference
    - polyaxon
    - user
sidebar: "polyaxon-cli"
---

> The commands in this sections can be used for all Polyaxon deployment types (i.e. it does not require a scheduler)

> You can always access the help menu for this command by adding `--help`

Usage:

```bash
$ polyaxon user [OPTIONS] COMMAND [ARGS]...
```

Commands for user management.

## activate

Usage:

```bash
polyaxon user activate [OPTIONS] USERNAME
```

Activate a user.

Example:

```bash
$ polyaxon user activate david
```


## delete

Usage:

```bash
polyaxon user delete [OPTIONS] USERNAME
```

Delete a user.

Example:

```bash
$ polyaxon user delete david
```
