---
title: "Google Analytics"
meta_title: "Google Analytics"
meta_description: "Publish Polyaxon events publication directly to Google Analytics for in-depth on-premise usage and metrics in realtime."
custom_excerpt: "Google Analytics lets you measure your advertising ROI as well as track your Flash, video, and social networking sites and applications."
image: "../../content/images/integrations/google-analytics.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - analytics
featured: false
visibility: public
status: coming-soon
---

Get in-depth metrics usage of your Polyaxon deployment, number of experiments, jobs, builds, and theirs statuses directly to Google analytics for further analysis. 
[Google Analytics account](https://analytics.google.com) is one of the most powerful, advanced platforms collecting and analysing your on-premise Polyaxon deployment. 


## Set up a new Google Analytics  property

Set up a new [Google Analytics account](https://analytics.google.com), for your Polyaxon deployment.

If you're already using Analytics, navigate to the admin area from the cog button in the bottom left corner, 
and use the middle column button to create a property:

On the next page, you'll need to provide some information about your site to create a property and generate a 
tracking code which you'll need for the next step.

## Get the tracking code

Once you've created a new property you will be redirected to the tracking code page.

## Add the tracking key to your Polyaxon deployment config 

Once you add the tracking to your deployment, Polyaxon will start sending events to segments, 
so you can review your deployment metrics on the Google Analytics dashboard at any time!
