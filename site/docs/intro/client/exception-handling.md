---
title: "Exception handling"
sub_link: "client/exception-handling"
meta_title: "Exception handling - Python Client References"
meta_description: "Polyaxon's Python library raises some of its own exceptions as well as standard Python exceptions."
visibility: public
status: published
tags:
  - specifications
  - polyaxon
  - python
sidebar: "intro"
---

## Overview

Polyaxon's Python library raises some of its own exceptions as well as standard Python exceptions.  

## Core Exceptions

Polyaxon raises several exceptions, all classes are derived from:

```bash
from polyaxon.exceptions import PolyaxonException
```

## Schema and Compiler Exceptions

During the parsing and validation of a Polyaxonfile or configurations, Polyaxon will raise:

```bash
from polyaxon.exceptions import PolyaxonSchemaError, PolyaxonfileError, PolyaxonCompilerError
```

## Client Exceptions

When performing API calls using the Python client, Polyaxon will raise:

```bash
from polyaxon.exceptions import PolyaxonClientException, PolyaxonHTTPError
```
