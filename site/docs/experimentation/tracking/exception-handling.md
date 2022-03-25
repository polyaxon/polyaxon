---
title: "Exception handling"
sub_link: "tracking/exception-handling"
meta_title: "Exception handling - Tracking - Experimentation"
meta_description: "Polyaxon's tracking module raises some of its own exceptions as well as standard Python exceptions."
visibility: public
status: published
tags:
  - client
  - api
  - polyaxon
  - python
  - tracking
  - reference
  - sdk
sidebar: "experimentation"
---

## Overview

The tracking module is based on the [Python library](/docs/core/python-library/exception-handling/) and so it raises similar exceptions in addition to standard Python exceptions and exception coming from other modules, 
for example when logging an image or a dataframe, an exception can be raised from `matplotlib` or `pandas`.  

## Core Exceptions

Polyaxon raises several exceptions, all classes are derived from:

```python
from polyaxon.exceptions import PolyaxonException
```

## Data validation

When logging a metadata or an artifacts, the tracking can raise the following exceptions:

```python
TypeError
ValueError
OSError
```

## Client Exceptions

When performing API calls using the Python client, Polyaxon will raise:

```python
from polyaxon.exceptions import PolyaxonClientException, PolyaxonHTTPError
```
