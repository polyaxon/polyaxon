---
title: "Postgres HA on AWS"
meta_title: "AWS Postgres"
meta_description: "Using AWS Postgres for a high available Polyaxon sql storage of your experiments and jobs' records."
custom_excerpt: "Amazon offers a fully managed relational database service, Amazon RDS for PostgreSQL. Amazon Relational Database Service (RDS) makes it easy to set up, operate, and scale PostgreSQL deployments in the cloud. With Amazon RDS, you can deploy internet-scale PostgreSQL deployments in minutes, with cost-efficient and resizable hardware capacity."
image: "../../content/images/integrations/redshift.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - setup
  - database
  - aws
featured: false
popularity: 0
visibility: public
status: published
---

This integration is about using AWS RDS for postgres server to provide a High Available database for Polyaxon.

> This integration can be used with all Polyaxon deployment types

## Create an RDS instance

Log into your [AWS Console](https://console.aws.amazon.com/console/home), click the EC2 link to go to the [RDS Console](https://console.aws.amazon.com/rds/home),
and click the blue “Create Database” button:

![create-db](../../content/images/integrations/aws/create-db.png)

Make sure to choose the “PostgreSQL” engine when creating an instance:

![create-postgresql](../../content/images/integrations/aws/create-pgsql.png)

Click “Next” and choose “Production” or “Dev/Test” based on your use-case.

## Choose an instance for the RDS database

![create-postgresql](../../content/images/integrations/aws/db-resource.png)

Scroll down and setup the credentials. Keep note of the credentials (master username and password, database name etc.), which will be required later.

## VPC and security group

Choose a VPC and security group, If you are going to deploy Polyaxon on AWS, then make sure the VPC used here is the same as the VPC used with your EC2/ECS instances.

> N.B: If you are planning to deploy Polyaxon outside AWS (e.g. On-prem, Polyaxon tracking on Heroku), then you have to make this DB instance publicly accessible.

> N.B: Make sure, the security group you choose has appropriate rules for inbound connections from wherever you deploy the Polyaxon.


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
