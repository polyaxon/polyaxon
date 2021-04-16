---
title: "Notebook Auto-Rendering"
meta_title: "Notebook Auto-Rendering"
meta_description: "Polyaxon UI can automatically render your notebooks on the artifacts tab."
custom_excerpt: "Polyaxon notebook auto-rendering service converts notebooks to static web pages."
image: "../../content/images/integrations/jupyter-notebook.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - tracking
  - experimentation
featured: false
popularity: 0
visibility: public
status: published
---

Polyaxon UI comes with an auto-rendering service for Jupyter Notebooks in the artifacts tab.

> **Note**: Requires CE or Agent v1.8.1 or higher

## Go to the artifacts tab

The Artifacts tab allows users to organize files, events, logs, models, outputs, ... from their runs 
that can be natively rendered in Polyaxon UI! 

If your job or experiment generate or has a notebook that has been tracked by Polyaxon, you can navigate to the artifacts tab:

![artifacts-tab](../../content/images/rendering/artifacts-tab.png)

## Visualize notebooks

If you click on any notebook, Polyaxon will attempt at rendering the notebook inside the UI:

![rendering-notebooks](../../content/images/rendering/notebooks.png)

## View raw content

You can also view the raw content which is rendered in a text editor:

![rendering-notebooks](../../content/images/rendering/raw-notebooks.png)
