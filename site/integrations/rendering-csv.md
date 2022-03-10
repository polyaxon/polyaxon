---
title: "CSV/TSV/Dataframe Auto-Rendering"
meta_title: "CSV/TSV/Dataframe Auto-Rendering"
meta_description: "Polyaxon UI can automatically render your CSV/TSV/Dataframe files on the artifacts tab."
custom_excerpt: "Polyaxon CSV/TSV/Dataframe auto-rendering converts files automatically to tables."
image: "../../content/images/integrations/csv.png"
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

Polyaxon UI comes with an auto-rendering for CSV/TSV/Dataframe files in the artifacts tab.

> **Note**: Requires CE or Agent v1.16.0 or higher

## Go to the artifacts tab

The Artifacts tab allows users to organize files, events, logs, models, outputs, ... from their runs 
that can be natively rendered in Polyaxon UI! 

If your job or experiment generate or has a file that follows a data separate values format, you can navigate to the artifacts tab to visualize it:

![artifacts-tab](../../content/images/rendering/artifacts-tab.png)

## Visualize the file

If you click on any csv file, Polyaxon will attempt at rendering the file inside the UI:

![rendering-csv](../../content/images/rendering/csv.png)

## View raw content

You can also view the raw content which is rendered in a text editor:

![raw-csv](../../content/images/rendering/raw-csv.png)

## Polyaxon event files

Polyaxon UI will automatically render any event file as well, i.e. files with `.plx` extension: 

![plx-event](../../content/images/rendering/plx.png)
