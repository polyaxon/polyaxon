---
title: "PostgreSQL HA"
sub_link: "platform/postgresql-ha"
meta_title: "High availability of postgresql database in Polyaxon - Configuration"
meta_description: "Keeping database records of your users, projects, experiments, and jobs is very important. Polyaxon offers a couple of ways to set a high available database."
tags:
  - configuration
  - polyaxon
  - postgresql
  - scaling
  - high-availability
  - kubernetes
  - docker-compose
sidebar: "setup"
---

Since keeping database records of your users, projects, experiments, and jobs is very important.
Polyaxon offers a couple of ways to set a high available database.

> **Note**: We strongly recommend that you do not deploy a production database using this chart. Although the provided database can persist data if configured, 
> you might encounter an issue in the future if we upgrade the dependency requirements or the version of the database image changes.

## Persistence

The easiest way to keep your database intact in case of node failures or restarts,
is by enabling postgresql persistence, enabling persistence will tell the database to use
a persistent volume to store data instead of using the host node.

### Dynamic persistence provisioning

Here's an example of using dynamic provisioning:

```yaml
postgresql:
  persistence:
    enabled: true
    size: 5Gi
```

Using this configuration, the volume will be provisioned dynamically,
based on default storage class defined in your cluster.

### Existing PersistentVolumeClaims

In case you want to have more control where and how the persistence claims is created,
and should not be managed by the chart,
you need to define a PVC and assign it to the `persistence.existingClaim`.

 1. Create the PersistentVolume
 2. Create the PersistentVolumeClaim
 3. Use the name of this claim in the chart

    ```yaml
    postgresql:
      persistence:
        enabled: true
        existingClaim: myClaimName
    ```

## External Postgresql

If you prefer to have the postgresql database managed and hosted outside of Kubernetes,
instead of the in-cluster one provided by Polyaxon, e.g.
[Amazon RDS for PostgreSQL](https://aws.amazon.com/rds/postgresql/),
[Azure Database for PostgreSQL](https://azure.microsoft.com/en-us/services/postgresql/),
[GCP Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres/),
or [DigitalOcean managed PostgreSQL](https://www.digitalocean.com/products/managed-databases/).
You need to disable the in-cluster database, and provide the information needed to establish a connection to the external one, e.g.:


```yaml
postgresql:
  enabled: false

externalServices:
  postgresql:
    user: polyaxon
    password: polyaxon
    database: postgres
    host: 35.262.163.88
```

Please check this [integration guide](/integrations/database/) for cloud specific instructions on how to setup a postgreSQL server instance.


## Scheduling

If you decided to deploy Polyaxon in-cluster make sure to set proper [node scheduling](/docs/setup/platform/common-reference/#node-and-deployment-manipulation)
to avoid running high load runs on the same node hosting the database.


## Connexion Max Age

`default: 60`

`connMaxAge` allows you to set the lifetime of a database connection, in seconds.
Use `0` to close database connections at the end of each request and `None` for unlimited persistent connections.

## Transaction pooling with pgbouncer

If you are running a high load Polyaxon deployment, we suggest using a connection pooler, e.g [pgbouncer](https://pgbouncer.github.io/).
