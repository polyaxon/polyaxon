---
title: "Elastic Stack"
meta_title: "Elastic Stack"
meta_description: "Polyaxon allows users to use Elastic Stack to reliably and securely take data from any source, in any format, and search, analyze, and visualize it in real-time."
custom_excerpt: "Elastic Stack lets you reliably and securely take data from any source, in any format, and search, analyze, and visualize it in real-time."
image: "../../content/images/integrations/elastic-stack.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - setup
  - logging
featured: false
popularity: 0
visibility: public
status: published
---

You can use the Elastic Stack to centralize your logging with Polyaxon.

## Overview

You can set up EFK ([elasticsearch](https://www.elastic.co/products/elasticsearch), [fluentd/fluentbit](https://www.fluentd.org/), [kibana](https://www.elastic.co/products/kibana)) as a stack to gather logs from Polyaxon core components or experiment and job runs.

If you are running Polyaxon in the cloud, then you can consider a managed service from your cloud provider.

## Setup Helm

You need [Helm](https://helm.sh/docs/intro/install/) to deploy Polyaxon as well as Elastic stack.

## Install ElasticSearch

```bash
helm install elasticsearch elasticsearch --version 7.1.1 --namespace=logging  -f elastic-config.yaml --repo https://helm.elastic.co
```

You can read more about how to customize your ElasticSearch instance and provide `elastic-config.yaml` to override the default values.

## Install Fluentd

```bash
helm install fluentd fluentd --namespace=logging -f fluentd-config.yaml --repo https://kiwigrid.github.io
```

You can read more about how to customize your Fluentd instance and provide `fluentd-config.yaml` to override the default values.

For instance if you want to log all pods managed by Polyaxon (core and runs), you might want to add:

```
# Filter to only records with label kubernetes.io/managed-by=polyaxon
<filter kubernetes.**>
@type grep
<regexp>
key $["kubernetes"]["labels"]["app.kubernetes.io/managed-by"]
pattern polyaxon
</regexp>
</filter>
```

If you want to only monitor the core components:

```
# Filter to only records with label type=polyaxon-core
<filter kubernetes.**>
@type grep
<regexp>
key $["kubernetes"]["labels"]["type"]
pattern polyaxon-core
</regexp>
</filter>
```

This filter should be added to your `fluentd-config.yaml` under `extraConfigMaps`, e.g:

```yaml
elasticsearch:
  host: 'elasticsearch-master'

configMaps:
  useDefaults:
    containersInputConf: false
    systemInputConf: false

extraConfigMaps:
  containers.input.conf: |-
    <match fluent.**>
    # Ignore fluentd' log
    @type null
    </match>
    # Docker's containers logs
    <source>
    @type tail
    path /var/log/containers/*.log
    pos_file /var/log/fluentd-containers.log.pos
    tag kubernetes.*
    read_from_head true
    <parse>
    @type json
    time_format %Y-%m-%dT%H:%M:%S.%NZ
    </parse>
    </source>
    # Kubernetes metadata
    <filter kubernetes.**>
    @type kubernetes_metadata
    </filter>
    <match kubernetes.var.log.containers.**kube-system**.log>
    @type null
    </match>
    # Exceptions in logs
    <match raw.kubernetes.**>
    @id raw.kubernetes
    @type detect_exceptions
    remove_tag_prefix raw
    message log
    stream stream
    multiline_flush_interval 5
    max_bytes 50000
    max_lines 1000
    </match>
    # Exclude kube-system
    <match kubernetes.var.log.containers.**kube-system**.log>
    @type null
    </match>
    # Filter to only records with label kubernetes.io/managed-by=polyaxon
    <filter kubernetes.**>
    @type grep
    <regexp>
    key $["kubernetes"]["labels"]["app.kubernetes.io/managed-by"]
    pattern polyaxon
    </regexp>
    </filter>
    # Filter to only records with label kubernetes.io/managed-by=polyaxon
    <filter kubernetes.**>
    @type grep
    <regexp>
    key $["kubernetes"]["labels"]["type"]
    pattern polyaxon-core
    </regexp>
    </filter>
```

## Install Kibana

```bash
helm install kibana --version 7.1.1 --name=kibana --namespace=logging -f kibana-config.yaml  --repo https://helm.elastic.co
```

You can read more about how to customize your ElasticSearch instance and provide `kibana-config.yaml` to override the default values.


## Check the logs on the Kibana UI

You can inspect the logs on the Kibana UI, by port-forwarding for example.

 1. When Kibana appears click Explore on my own.
     From the top-left or from the Visualize and Explore Data panel select the Discover item.
     In the form field Index pattern enter `logstash-*` It should read “Success!” and Click the > Next step button.

 2. In the next form select timestamp from the dropdown labeled Time Filter field name.

 3. From the bottom-right of the form select Create index pattern. In a moment a list of fields will appear.

 4. From the top-left of the home screen’s Visualize and Explore Data panel, select the Discover item. The logs list will appear.


## Notes

Polyaxon will persist by default all runs' logs to a persistent volume or a cloud bucket provided by the user.
Please check the [Logs storage configuration](/docs/setup/connections/artifacts/) for more details.
