---
title: "Streamlit"
meta_title: "Serving ML models with Streamlit on Kubernetes"
meta_description: "Polyaxon integrates with Streamlit to run and publish custom ML apps on Kubernetes."
custom_excerpt: "Streamlit’s open-source app framework is the easiest way for data scientists and machine learning engineers to create beautiful, performant apps in only a few hours!  All in pure Python."
image: "../../content/images/integrations/streamlit.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - services
  - serving
  - dashboard
featured: false
popularity: 1
visibility: public
status: examples
---

Polyaxon allows you to extend it's native dashboarding capabilities and integrates with Streamlit to run and publish custom ML apps.

## Overview

Users can leverage the service abstraction to schedule ML apps created using [Streamlit](https://streamlit.io/) to showcase their results or to expose their work as dynamic apps.

In this guide, we will show how to easily schedule and expose such work on your Kubernetes cluster using Polyaxon.

For users using Polyaxon Cloud or Polyaxon EE, the app will be automatically protected with authentication and only users with enough permissions 
and who have access to the project where the app is running can interact with the service.

The code used for this example is hosted on [github](https://github.com/polyaxon/spacy-streamlit-polyaxon-demo).

This demo shows how to use [Spacy](https://spacy.io/) to analyze text provided by the end user. 

## App code

This is a sample app that was created by [Ines Montani](https://github.com/ines) and was adapted to run on Polyaxon:

```python
import spacy_streamlit
from pathlib import Path
import srsly
import importlib

MODELS = srsly.read_json(Path(__file__).parent / "models.json")
DEFAULT_MODEL = "en_core_web_sm"
DEFAULT_TEXT = "David Bowie moved to the US in 1974, initially staying in New York City before settling in Los Angeles."
DESCRIPTION = """**Explore trained [spaCy v3.0](https://nightly.spacy.io) pipelines**"""

def get_default_text(nlp):
    # Check if spaCy has built-in example texts for the language
    try:
        examples = importlib.import_module(f".lang.{nlp.lang}.examples", "spacy")
        return examples.sentences[0]
    except (ModuleNotFoundError, ImportError):
        return ""

spacy_streamlit.visualize(
    MODELS,
    default_model=DEFAULT_MODEL,
    visualizers=["parser", "ner", "similarity", "tokens"],
    show_visualizer_select=True,
    sidebar_description=DESCRIPTION,
    get_default_text=get_default_text
)
```

## Polyaxon component to schedule the app

To schedule this app on Polyaxon, we just need to run this [simple component manifest](https://github.com/polyaxon/spacy-streamlit-polyaxon-demo/blob/master/polyaxonfiles/app.yaml): 

```yaml
version: 1.1
kind: component
name: spacy-streamlit-app
tags: [spacy, streamlit]
run:
  kind: service
  ports: [8501]
  rewritePath: true
  container:
    image: polyaxon/polyaxon-examples:spacy-streamlit-demo
    command: [streamlit, run, app.py]
```

To run without cloning the repo:

```bash
polyaxon run --url=https://raw.githubusercontent.com/polyaxon/spacy-streamlit-polyaxon-demo/master/polyaxonfiles/app.yaml
```

If you cloned the repo:

```bash
polyaxon run -f polayxonfiles/app.yaml
```

> **Note**: You might need to provide the correct project with `-p PROJECT_NAME`


## Viewing the service 

Go to the UI under `service` tab:

```bash
polyaxon ops dashboard [-uid] [-p]
```

Or to get to the service directly:

```bash
polyaxon ops service [-uid] [-p]
```

Or to get the service in full-screen mode:

```bash
polyaxon ops service --external [-uid] [-p]
```

Using the light the theme:

![spacy-streamlit-light-1](../../content/images/integrations/streamlit/spacy-streamlit-light-1.png)

![spacy-streamlit-light-2](../../content/images/integrations/streamlit/spacy-streamlit-light-2.png)

Using the dark the theme:

![spacy-streamlit-dark-1](../../content/images/integrations/streamlit/spacy-streamlit-dark-1.png)

![spacy-streamlit-dark-2](../../content/images/integrations/streamlit/spacy-streamlit-dark-2.png)

## Additional information

The docker image `polyaxon/polyaxon-examples:spacy-streamlit-demo` was created using this [operation](https://github.com/polyaxon/spacy-streamlit-polyaxon-demo/blob/master/polyaxonfiles/build.yaml):

```yaml
version: 1.1
kind: operation
name: build-spacy-streamlit
params:
  destination:
    connection: CONNECTION_NAME
    value: polyaxon-examples:spacy-streamlit-demo
  context:
    value: "{{ globals.artifacts_path }}/spacy-streamlit-polyaxon-demo"
runPatch:
  init:
    - git:
        url: "https://github.com/polyaxon/spacy-streamlit-polyaxon-demo"
hubRef: kaniko
```

This operation clones the repo (https://github.com/polyaxon/spacy-streamlit-polyaxon-demo), 
and builds the container using the [Dockerfile](https://github.com/polyaxon/spacy-streamlit-polyaxon-demo/blob/master/Dockerfile) 
that is hosted inside the repo, which basically just copies the code and runs `pip3 install -r requirements.txt`.
