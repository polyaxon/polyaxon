---
title: "Postgres HA on GCP"
meta_title: "Google CLOUD SQL for postgres"
meta_description: "Using Google CLOUD SQL for postgres for a high available Polyaxon sql storage of your experiments and jobs' records."
custom_excerpt: "Cloud SQL is a fully-managed database service that makes it easy to set up, maintain, manage, and administer your relational PostgreSQL and MySQL databases in the cloud. Cloud SQL offers high performance, scalability, and convenience. Hosted on Google Cloud Platform, Cloud SQL provides a database infrastructure for applications running anywhere."
image: "../../content/images/integrations/gcp-sql.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - setup
  - database
  - gcp
featured: false
popularity: 0
visibility: public
status: published
---

This integration is about using Google CLOUD SQL for postgres server to provide a High Available database for Polyaxon.

> This integration can be used with all Polyaxon deployment types

## Create a Google Cloud Project

If you don't have a Google Cloud Project you have to create one:

```bash
gcloud projects create <project>
```

## Create a Google Cloud SQL Postgres instance

```bash
gcloud sql instances create <databse_name> --database-version POSTGRES_9_6 \
       --cpu 1 --memory 3840MiB --region eastus --project <project>
```

Once the instance is created, set a password for the default postgres user. Make sure you substitute `<password>` with a strong password.

```bash
gcloud sql users set-password postgres --instance <databse_name> \
       --password <password> --project <project>
```

## Setup a private IP address

In order to connect to the Cloud SQL instance, you need to setup a private address to connect from Polyaxon to the database instance.
Please check this [guide](https://cloud.google.com/sql/docs/postgres/connect-kubernetes-engine)


## Update polyaxon deployment

```yaml
postgresql:
  enabled: false

externalServices:
  postgresql:
    user: <username>
    password: <password>
    database: <database>
    host: <server_ip>
```

