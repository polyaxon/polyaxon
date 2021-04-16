---
title: "Netron Auto-Rendering"
meta_title: "Netron Auto-Rendering"
meta_description: "Polyaxon UI can automatically render your neural network, deep learning and machine learning models."
custom_excerpt: "Netron is viewer for neural network, deep learning and machine learning models."
image: "../../content/images/integrations/netron.png"
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

Polyaxon UI comes with a viewer and an auto-rendering service for your neural network, deep learning and machine learning models based on [Netron](https://github.com/lutzroeder/netron).

> **Note**: Requires CE or Agent v1.8.1 or higher

## Go to the artifacts tab

The Artifacts tab allows users to organize files, events, logs, models, outputs, ... from their runs 
that can be natively rendered in Polyaxon UI! 

If your job or experiment generate or has a model that has been tracked by Polyaxon, you can navigate to the artifacts tab:

![artifacts-tab](../../content/images/rendering/artifacts-tab.png)

## Visualize the model

If you click on the model, Polyaxon will render it using Netron inside the UI:

![rendering-netron](../../content/images/rendering/netron-render.png)


![rendering-netron](../../content/images/rendering/netron.png)
