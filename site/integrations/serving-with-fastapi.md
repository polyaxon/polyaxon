---
title: "FastAPI"
meta_title: "Serving ML models REST APIs with FastAPI on Kubernetes"
meta_description: "Serve internal API and test your models before moving them to production."
custom_excerpt: "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints."
image: "../../content/images/integrations/fastapi.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - services
  - serving
featured: false
popularity: 0
class_name: instruction
visibility: public
status: examples
---

Polyaxon users can use the service abstraction to move from trained ML models to internal production-grade prediction APIs or to test their APIs before moving to a production framework. 

This guide demonstrates how to create a simple [FastAPI](https://fastapi.tiangolo.com/) service and schedule it with Polyaxon.

## Install the libraries

Your container needs to have the FastAPI dependencies:

```bash
pip install fastapi uvicorn[standard]
```  

## Creating a simple API

The following code is a simple FastAPI program:

```python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

## Polyaxon service

By default, Polyaxon exposes services with a base url following this pattern: `/services/v1/namespace/owner/project/runs/uuid`.
In order to leverage the service kind in Polyaxon with FastAPI, the easiest to avoid handling base urls is by enabling the `rewritePath: true` flag to rewrite the path and remove that part.  

## Polyaxon component

This is a simple API component, the component can be more complex if it requires to initialize code, artifacts, or if it defines inputs.

```yaml
version: 1.1
kind: component
name: fastapi-service
tags: ["fastapi", "api"]
run:
  kind: service
  ports: [8000]
  rewritePath: true
  container:
    image: polyaxon/polyaxon-examples:ml-serving
    command: ["sh", "-c"]
    args: ["uvicorn app:app --host 0.0.0.0 --port 8000"]
```

### Example as an executable component

> This inline example is intended to make it easy to execute this component without download or cloning any repo, this not intended as production pattern.

```yaml
version: 1.1
kind: component
name: fastapi-service
tags: ["fastapi", "api"]
run:
  kind: service
  ports: [8000]
  rewritePath: true
  init:
    - file:
        filename: app.py
        content: |
          from typing import Optional

          from fastapi import FastAPI
          
          app = FastAPI()
          
          
          @app.get("/")
          def read_root():
              return {"Hello": "World"}
          
          
          @app.get("/items/{item_id}")
          def read_item(item_id: int, q: Optional[str] = None):
              return {"item_id": item_id, "q": q}
  container:
    image: polyaxon/polyaxon-examples:ml-serving
    workingDir: "{{ globals.artifacts_path }}"
    command: ["sh", "-c"]
    args: ["uvicorn app:app --host 0.0.0.0 --port 8000"]
```

## Scheduling the example

To schedule this component you can copy/past it to the UI and use the default values.

You can also schedule it with CLI:

```bash
polyaxon run -f api.yaml
```

## Interacting with the API

The API can be tested directly from the UI, you also can get the url by clicking fullscreen or you can execute this CLI command to get the external service url:

```bash
polyaxon ops service --external --url
``` 

To test the endpoint using a browser the index returns a Json value, you can also append `items/5?q=somequery` to get a different response.

To test the endpoint using curl:

```bash
curl HOST:PORT/rewrite-services/v1/NAMESPACE/ORG/PROJECT/runs/UUID/items/5?q=somequery --request GET \
    --header "Content-Type: application/json"

{"item_id":5,"q":"somequery"}
```

## Authentication

For users on Polyaxon EE or Polyaxon Cloud, you will need to use:

 * A browser session with an authenticated user.
 * Add the auth header with a [valid auth token](/docs/management/organizations/user-profile/#token-management): `--header "Authorization: token AUTH_TOKEN"`.  

## Complete example

For a complete example from training to serving, please check [the serving tutorial](/docs/intro/serving/serving-fastapi-rest-apis/)
