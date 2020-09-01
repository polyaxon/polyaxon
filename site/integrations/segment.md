---
title: "Segment"
meta_title: "Segment"
meta_description: "Want deep analytics for your Polyaxon deployment? Polyaxon can send events to Segment using straightforward integration. Send Polyaxon events to Segment with straightforward integration and get in-depth metrics about your platform's usage."
custom_excerpt: "Segment is a single platform that collects, stores, and routes your user data to hundreds of tools with the flick of a switch."
image: "../../content/images/integrations/segment.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - analytics
featured: false
popularity: 0
visibility: public
status: EE
---

Get in-depth metrics usage of your Polyaxon deployment, number of experiments, jobs, builds, and their statuses directly to Segment for further analysis.
[Segment](https://segment.com/) is a platform for collecting and analyzing your on-premise Polyaxon deployment.

## Set up a new Segment source

When you create a new Segment account, follow the instructions to create your first data source for your Polyaxon.

## Get the tracking key

Once you've created the new source, you'll be taken to the project settings area.
From here, copy the tracking code to your clipboard.

## Add the tracking key to your Polyaxon deployment config

Once you add the tracking to your deployment, Polyaxon will start sending events to segments, so you can connect to as many
third party data services as you like and enjoy the event pipeline which Segment provides.
