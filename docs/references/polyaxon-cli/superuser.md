---
title: "Superuser"
sub_link: "polyaxon-cli/superuser"
meta_title: "Polyaxonfile Command Line Interface Specification - Superuser - Polyaxon References"
meta_description: "Polyaxonfile Command Line Interface Specification - Superuser."
visibility: public
status: published
tags:
    - cli
    - reference
    - polyaxon
    - superuser
sidebar: "polyaxon-cli"
---

> The commands in this sections can be used for all Polyaxon deployment types (i.e. it does not require a scheduler)

> You can always access the help menu for this command by adding `--help`

Usage:

```bash
$ polyaxon superuser [OPTIONS] COMMAND [ARGS]...
```

Commands for superuser role management.

## grant

Usage:

```bash
polyaxon superuser grant [OPTIONS] USERNAME
```

Grant superuser role to a user.

Example:

```bash
$ polyaxon superuser grant david
```


## revoke

Usage:

```bash
polyaxon superuser revoke [OPTIONS] USERNAME
```

Revoke superuser role to a user.

Example:

```bash
$ polyaxon superuser revoke david
```
