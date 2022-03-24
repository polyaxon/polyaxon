---
title: "Exception handling"
sub_link: "python-library/exception-handling"
meta_title: "Exception handling - Python Client References"
meta_description: "Polyaxon's Python library raises some of its own exceptions as well as standard Python exceptions."
visibility: public
status: published
tags:
  - client
  - api
  - polyaxon
  - python
sidebar: "core"
---

## Overview

Polyaxon's Python library raises some of its own exceptions as well as standard Python exceptions.  

## Core Exceptions

Polyaxon raises several exceptions, all classes are derived from:

```python
from polyaxon.exceptions import PolyaxonException
```

## Schema and Compiler Exceptions

During the parsing and validation of a Polyaxonfile or configurations, Polyaxon will raise:

```python
from polyaxon.exceptions import PolyaxonSchemaError, PolyaxonfileError, PolyaxonCompilerError
```

## Client Exceptions

When performing API calls using the Python client, Polyaxon will raise:

```python
from polyaxon.exceptions import PolyaxonClientException, PolyaxonHTTPError
```
