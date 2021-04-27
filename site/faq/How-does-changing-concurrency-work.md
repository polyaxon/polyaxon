---
title: "How does changing concurrency work?"
meta_title: "How does changing concurrency work? - FAQ"
meta_description: "Polyaxon will try meet the new concurrency limit by applying a draining effect if the concurrency is reduced, or schedule more operations if increased."
featured: false
custom_excerpt: "Polyaxon will try meet the new concurrency limit by applying a draining effect if the concurrency is reduced, or schedule more operations if increased."
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
visibility: public
status: published
tags:
  - scheduling
---

When you reduce a pipeline or a queue concurrency, Polyaxon does not kill or cancel active or scheduled runs to meet the new value.
Polyaxon will apply a "draining" effect, where it will allow those active or scheduled runs to finish first without scheduling more operations under that pipeline or on that queue.

If the concurrency is increased, Polyaxon will try to reach this new value by scheduling new operations while respecting other higher level limitations. 
For example increasing the concurrency of a pipeline to a higher value than the concurrency of the queue used or the organization's quota will result 
in a pass-through mechanism and the agent manager will only consider the queue or the organization to manage the concurrency, in other terms it has the same effect as not setting any concurrency limit.  
