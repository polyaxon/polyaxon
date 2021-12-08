---
title: "Flask"
meta_title: "Serving ML models REST APIs with Flask on Kubernetes"
meta_description: "Serve internal API and test your models before moving them to production."
custom_excerpt: "Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions."
image: "../../content/images/integrations/flask.png"
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

This guide demonstrates how to create a simple [Flask](https://flask.palletsprojects.com/) service and schedule it with Polyaxon.

## Install the libraries

Your container needs to have the Flask dependencies:

```bash
pip install flask gunicorn
```  

## Creating a simple API

The following code is a simple Flask program:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'
```

## Polyaxon service

By default, Polyaxon exposes services with a base url following this pattern: `/services/v1/namespace/owner/project/runs/uuid`.
In order to leverage the service kind in Polyaxon with Flask, the easiest to avoid handling base urls is by enabling the `rewritePath: true` flag to rewrite the path and remove that part.  

## Polyaxon component

This is a simple API component, the component can be more complex if it requires to initialize code, artifacts, or if it defines inputs.

```yaml
version: 1.1
kind: component
name: flask-service
tags: ["flask", "api"]
run:
  kind: service
  ports: [5000]
  rewritePath: true
  container:
    image: polyaxon/polyaxon-examples:ml-serving
    command: ["sh", "-c"]
    args: ["flask run --host=0.0.0.0"]
```

If you need to schedule a more robust API with a production wsgi you can use gunicorn:

```yaml
version: 1.1
kind: component
name: flask-service
tags: ["flask", "api"]
run:
  kind: service
  ports: [8000]
  rewritePath: true
  container:
    image: polyaxon/polyaxon-examples:ml-serving
    command: ["sh", "-c"]
    args: ["gunicorn --preload -t 60 --bind 0.0.0.0:8000 app:app"]
```

### Example as an executable component

> This inline example is intended to make it easy to execute this component without download or cloning any repo, this not intended as production pattern.

```yaml
version: 1.1
kind: component
name: flask-service
tags: ["flask", "api"]
run:
  kind: service
  ports: [8000]
  rewritePath: true
  init:
    - file:
        filename: app.py
        content: |
          from flask import Flask

          app = Flask(__name__)
          
          @app.route('/')
          def index():
              return 'Index Page'
          
          @app.route('/hello')
          def hello():
              return 'Hello, World'
  container:
    image: polyaxon/polyaxon-examples:ml-serving
    workingDir: "{{ globals.artifacts_path }}"
    command: ["sh", "-c"]
    args: ["gunicorn --preload -t 60 --bind 0.0.0.0:8000 app:app"]
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

To test the endpoint using a browser the index returns a `Index Page`, you can also append `/hello` to get a different response `Hello, World`.

To test the endpoint using curl:

```bash
curl HOST:PORT/rewrite-services/v1/NAMESPACE/ORG/PROJECT/runs/UUID/hello --request GET \
    --header "Content-Type: application/json"

Hello, World
```

## Authentication

For users on Polyaxon EE or Polyaxon Cloud, you will need to use:

 * A browser session with an authenticated user.
 * Add the auth header with a [valid auth token](/docs/management/organizations/user-profile/#token-management): `--header "Authorization: token AUTH_TOKEN"`.

## Complete example

For a complete example from training to serving, please check [the serving tutorial](/docs/intro/serving/serving-flask-rest-apis/)
