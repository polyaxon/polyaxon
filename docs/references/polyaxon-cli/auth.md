---
title: "Auth"
sub_link: "polyaxon-cli/auth"
meta_title: "Polyaxonfile Command Line Interface Specification - Login - Polyaxon References"
meta_description: "Polyaxonfile Command Line Interface Specification - Login."
visibility: public
status: published
tags:
    - cli
    - reference
    - polyaxon
    - login
    - logout
    - auth
sidebar: "polyaxon-cli"
---

> The commands in this sections can be used for all Polyaxon deployment types (i.e. it does not require a scheduler)

> You can always access the help menu for this command by adding `--help`

## login

Usage:

```bash
$ polyaxon login [OPTIONS]
```

### Example using username and password

```bash
$ polyaxon login --username=adam --password=secret
```

Or

```bash
$ polyaxon login -u adam -p secret
```

### Example using username and prompt

```bash
$ polyaxon login --username=adam

Please enter your password:
```

### Example using token

```bash
$ polyaxon login --token=my-token
```

Login to Polyaxon.

Options:

option | type | description
-------|------|------------
  -t --token| TEXT|     Polyaxon token
  -u --username| TEXT|  Polyaxon username
  -p --password| TEXT|  Polyaxon password
  --help| |Show this message and exit.


## logout

Usage:

```bash
$ polyaxon logout
```

Logout of Polyaxon.


## whoami

Usage:

```
$ polyaxon whoami
```

Show current logged Polyaxon user.
