---
title: "Builds"
sub_link: "builds"
meta_title: "Builds in Polyaxon - Core Concepts"
meta_description: "A Build is the container created to run your jobs ans experiments."
tags:
    - concepts
    - polyaxon
    - experimentation
    - jobs
    - architecture
sidebar: "concepts"
---

Builds are one of the primitive that Polyaxon creates automatically when a user creates an experiment or job.

Polyaxon provides different [backends](/integrations/containers/) for creating builds, by default the platform uses the in-cluster native builder, but the user can change that.

Polyaxon tries to abstract the creation of containers, to allow users to easily iterate on their experiments, by exposing a very simple [API](/references/polyaxonfile-yaml-specification/#build-job-sections) to create a Docker image. 
However, in certain cases, users might need to create complex Dockerfiles, in that case, 
the platform can build containers based on the Dockerfiles provided by the users instead of generating one by the platform.  
