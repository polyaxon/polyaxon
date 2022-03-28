---
title: "Authenticate Polyaxon CLI"
sub_link: "cli/authentication"
meta_title: "A guide on how to authenticate Polyaxon CLI - Core Concepts"
meta_description: "Polyaxon login command allows to authenticate your CLI and creates a context for future interactions with the API."
visibility: public
status: published
tags:
  - cli
  - reference
  - polyaxon
  - concepts
  - tutorials
sidebar: "core"
---

<blockquote class="commercial">This is part of our commercial offering.</blockquote>

Polyaxon login command allows to authenticate your CLI and creates a context for future interactions with the API.

## Overview

Polyaxon CLI provides several options to create an auth context. Both the CLI and the Python Client, if used, will look for an auth context to perform API calls. 

When running an operation in-cluster, Polyaxon will automatically provide a scoped auth context based on the user who started the operation, so the user does not have to authenticate their runs manually.
It's also possible to disable this default behavior by setting the [auth plugin](/docs/core/specification/plugins/#auth):

```yaml
plugins:
  auth: false
```

## Auth options

Users can can login by:
 * passing a token directly: `polyaxon login -t TOKEN`
 * passing the username/password: `polyaxon login -u USER -p PASS`
 * passing the username and getting a hidden prompt to pass the password: `polyaxon login -u USER`
 * getting a prompt to pass a token: `polyaxon login`

> **Note 1**: the `--user/-u` can be the username or the email.

> **Note 2**: the `--token/-t` can be any token issued by the users under the `profile > token`

## Environment variables

Users can also authenticate the CLI by setting the environment variable `POLYAXON_AUTH_TOKEN`.
