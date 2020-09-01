---
title: "Jenkins"
meta_title: "Jenkins"
meta_description: "Polyaxon can be integrated with Jenkins to create an end to end machine learning pipeline."
custom_excerpt: "Jenkins is an open-source automation server, Jenkins provides hundreds of plugins to support building, deploying and automating workflows."
image: "../../content/images/integrations/jenkins.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - pipelines
  - scheduling
  - dags
  - automation
featured: false
popularity: 0
visibility: public
status: published
---

You can easily use Polyaxon in your Jenkins pipelines.

Starting with Jenkins Pipeline versions 2.5 and higher, Jenkins Pipeline has built-in support for interacting with Docker from within a Jenkinsfile.

## Polyaxon as a Jenkins Pipeline stage


```json
pipeline {
    agent {
        docker { image 'polyaxon:polyaxon-cli:1.x.x' }
    }
    stages {
        stage('Submit') {
            steps {
                sh 'polyaxon run -f path/to/polyaxonfile'
            }
        }
    }
}
```

> **Tip**: Polyaxon provides a native [DAG](/docs/automation/) runtime for managing your operations dependencies in a simple and efficient way.
