---
title: "Migration to v0.5.x"
sub_link: "migration"
meta_title: "Migration to Polyaxon v0.5.x - Polyaxon Releases"
meta_description: "Polyaxon Migration to Polyaxon v0.5.x."
visibility: public
status: published
tags:
    - reference
---

v0.5 includes a few major product and configuration changes that you should be aware of if you are upgrading an existing Polyaxon deployment.

## Before you upgrade

Before upgrading to Polyaxon v0.5, please make sure you are running the latest version v0.4.4. Also please make sure you have a backup of your database.

## How to upgrade

The latest Polyaxon's Helm chart has up-to-date dependency requirements,  
some of these dependencies cannot be upgraded automatically and require a shutdown.

N.B.1 the Postgres dependency is still the same, we also suggest that you always pin the db version, 
Polyaxon's built-in dependency points to `imageTag: 9.6.1`.
 
N.B.2 Polyaxon supports any version of postfresql from 9.6 and it's recommended that you have this value in your deployment config.

N.B.3 If you are using an external Postgres instance, the chart has been updated to consolidate all external services in one section. 

### Teardown Polyaxon deployment

In order to upgrade to the latest Polyaxon version, please make sure to teardown your deployment, 
this will leave your data intact, i.e. database, outputs, logs, and they will be reused upon the upgrade.


### Delete entities not deleted by Helm

Often times after a Helm teardown, some service accounts or secrets might be left undeleted, 
please make sure to delete them before proceeding.

### Migrate your configuration YAML/Json file

In order to upgrade to the new version while reusing your previous data, 
you need to make sure that your deployment config file is valid, you can use the CLI to validate your new config file. 

Make sure to keep a backup of your config file to set the configuration using the web UI.

Several options have been migrated to a web UI settings page, please section [Dynamic configuration](/resources/migration/#dynamic-configuration).

### Dependencies

You need to decide which built-in dependencies to use from the chart. 
Polyaxon v0.5 comes with built-in dependencies for `rabbitmq-ha`, `redis`, `postgresql`, and `docker-registry`. 
That being said, in this version, you can disable all dependencies 
and bring your own (either managed by a cloud provider, or hosted on the same cluster but managed by a different chart). 

To disable one or several components:

```yaml
postgresql:
  enabled: false
 
redis:
  enabled: false

rabbitmq-ha:
  enabled: false
  
docker-registry:
  enabled: false
```

To provide an external connexion for one or several of these dependencies:

```yaml
externalServices:
  postgresql:
    ...
  redis:
    ...
  rabbitmq:
    ...
```

For the docker registry, since it's not required for starting the core components, 
you can use the web UI to set a connexion or several depending on your distribution.

For more details about the HA for each one of these components, please check:

 * [Postgresql HA](/configuration/postgresql-ha/)
 * [Redis HA](/configuration/redis-ha/)
 * [Rabbitmq HA](/configuration/rabbitmq-ha/)
 * [Docker registry HA](/configuration/postgresql-ha/)


Finally, in the v0.5, Polyaxon allows to use Redis as a broker as well, 
which means that you can turn-off rabbitmq completely and rely on redis. 
Please see [this for more details](/configuration/broker/).

## Dynamic configuration

Several configuration options are now stored in the database, not in a config.yaml file.

Editing the options is now only possible through the web UI. Some configuration are still managed by the config.yaml file, 
e.g. data, logs, outputs, and will be migrated slowly to the web UI in the following versions.

### Config options that were moved to the web UI settings page

```
integrations:
  slack:	
  hipchat:	
  mattermost:	
  discord:	
  pagerduty:	
  webhooks:	

auth:
 github:
 gitlab:
 bitbucket:
 azure:
 
notebookBackend:
notebookDockerImage:
tensorboardDockerImage:

kaniko:
  image:
  imageTag:
  imagePullPolicy:

dockerizer:
  imagePullPolicy
  
nodeSelectors:
  experiments:
  jobs:
  builds:
  tensorboards:
tolerations:
  resourcesDaemon:
  experiments:
  jobs:
  builds:
  tensorboards:
affinity:
  experiments:
  jobs:
  builds:
  tensorboards:

secretRefs:
configmapRefs:

privateRegistries:
reposAccessToken:
``` 

## Platform ports

Starting from v0.5, Polyaxon will use one single port for handling API requests, 
the platform is moving to internal plugins for handling logs, metadata, and other plugins.
This will reduce the complexity of securing the platform, and expose more flexibility to extend and create custom plugins.

This change will affect several components:

 * In the helm chart there will be only one port exposed from the service.
 
The CLI will accept only one argument for ports: `--port=`

If you have a custom configuration please have a look at the service.yaml file and ing.yaml file.

## Component scheduling

Since most of the configurations are now UI based, the scheduling exposed in the Helm chart is fairly standard, 
and only applies to the components being deployed, i.e. API, scheduler, events, ...:

```yaml
nodeSelector:
tolerations:
affinity:
```

Additionally, any dependency enabled can be customized in a similar way, e.g.

```yaml
postgresql:
  nodeSelector:
  tolerations:
  affinity:
```

For jobs, experiments, builds, notebooks, and tensorboards, 
a web UI has all information about default values, and an easy way to change them.

After deploying the platform, you can update the default [node scheduling](/configuration/custom-node-scheduling/). for each primitive through the web UI, 
and using Polyaxonfiles.

N.B. This change only applies to CE versions, since EE had dynamic configurations.

## Private registries

In order to pull/push to private docker registries, 
the platform will be using standard credential configuration instead of the previous way of passing user and password. 
You can still authorize access to private registries by providing user/password, but it should be through a secret with a credential helper.

The credential config can be set in a kubernetes secret and will be attached during the build process to allow pulling and pushing images. 

## Schemas

### Declarations
 
`declarations` is now deprecated, and `params` is used instead. 
However the platform will still accept any polyaxonfile containing `declarations`.
 
Polyaxon v0.5 introduces also new way to declare values in your polyaxonfiles; `inputs` and `outputs`. 
These 2 new sections will allow to define types declarations of your polyaxonfiles, and can have default values.

Additionally a user can override or provide a value for an input or output using params with an override file or directly with the CLI:

`polyaxon run -f polyaxonfile.yaml -P param1=value1 -P param2=value2` 

### Persistence

`persistence` is now deprecated, and `data_refs` under `environment` is used instead. 
The platform will still accept any polyaxonfile containing `persistence`.

### configmaps_refs

`configmaps_refs` has been renamed to `config_maps_refs`, The platform will still accept any polyaxonfile containing `configmaps_refs`.

## Specification

The specficiation requires an extra step: `parse()`

## CLI 

### deploy

`polyaxon deploy` is now moved to `polyaxon admin deploy`, `polyaxon admin upgrade`, and `polyaxon admin teardown`.

### \-\-declarations / -d

`declarations` is deprecated in favor of `params`, this flag is also changed to `--params / -p` 


## Search

### declarations is now params

`declarations` is deprecated in favor of `params`

`declarations.param1: value1 | value2` is now `params.param1: value1 | value2`. The api will still accept requests with `declarations`

### metric is now metrics

To make the search consistent, `metric` is deprecated in favor of `metrics`.

`metric.loss: <= 0.1` is now `metrics.loss: <= 0.1`. The api will still accept requests with `metric`.


## Environment variables exposed in the runs

`POLYAXON_DECLARATIONS` is now `POLYAXON_PARAMS`, if you are using polyaxon-client, your program should work without changes. 

## Tracking

`log_output` and `log_outputs` are now`log_artifact` and `log_artifacts`. 
