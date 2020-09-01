---
title: "Postgres HA on Azure"
meta_title: "Azure Database for postgres"
meta_description: "Using Azure Database for postgres for a high available Polyaxon sql storage of your experiments and jobs' records."
custom_excerpt: "Azure Database for PostgreSQL provides fully managed, enterprise-ready community PostgreSQL database as a service. The PostgreSQL Community edition helps you easily lift and shift to the cloud, using languages and frameworks of your choice."
image: "../../content/images/integrations/azure-postgresql.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - setup
  - database
  - azure
featured: false
popularity: 0
visibility: public
status: published
---

This integration is about using Azure Database for PostgreSQL server to provide a High Available database for Polyaxon.

> This integration can be used with all Polyaxon deployment types


## Pre-requisites

A valid Azure Subscription (click here for a free trial).


## One-click deploy ARM Template

All resources mentioned in this guide can be deployed using the one-click button below.

[![Deploy to Azure Button](https://azuredeploy.net/deploybutton.png)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fpolyaxon%2Fpolyaxon-azure%2Fmaster%2Fprovision-pg%2Ftemplate.json)

(The button opens Azure Portal, you might want to do a Ctrl+Click, to get it on a new tab)

![azure-one-click-deployment](../../content/images/integrations/azure/custom-deployment.png)

Once all entries are filled, you can click the Purchase button.

You can now use this PostgreSQL server with your Polyaxon deployment:

```yaml
postgresql:
  enabled: false

externalServices:
  postgresql:
    user: <server_admin_login_name>
    password: <password>
    database: <database>
    host: <server_name>
```

You need to replace the user, password, database, and host, based on the information you filled in the form, you can always find this information on the entity overview of Azure dashboard.

## CLI instructions

In case you want to use [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) to create the database resource.

### CLI Login

```bash
az login
```

### Create a new Resource Group

If you don't have a resource group yet, you need to create one:

```bash
az group create --name <resource> --location eastus
```

### Provision a PostgreSQL database

You need a resource group to create PostgreSQL server instance:

```bash
az postgres server create --resource-group <resource> \
   --name "<server_name>" \
   --location eastus \
   --admin-user "<user>" \
   --admin-password "<admin_password>" \
   --sku-name GP_Gen5_2 \
   --version 10
```

### Allow access to Azure Services

Create a firewall rule allowing acess from Azure internal services:

```bash
az postgres server firewall-rule create --resource-group <resource_group> \
   --server-name "<server_name>" \
   --name "allow-azure-internal" \
   --start-ip-address 0.0.0.0 \
   --end-ip-address 0.0.0.0
```

### Update polyaxon deployment

```yaml
postgresql:
  enabled: false

externalServices:
  postgresql:
    user: <server_admin_login_name>
    password: <password>
    database: <database>
    host: <server_name>
```
