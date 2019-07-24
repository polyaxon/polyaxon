---
title: "SSO with Azure"
meta_title: "Azure"
meta_description: "How to use Azure to manage users authentication on Polyaxon. You can easily integrate Microsoft Azure to manage users authentication on Polyaxon."
custom_excerpt: "Azure Websites Authentication/Authorization allows you to quickly and easily restrict access to your websites running on Azure Websites by leveraging Azure Active Directory."
image: "../../content/images/integrations/azure.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - sso
featured: false
visibility: public
status: published
---

You can use Azure to manage your organization’s entire membership.

## Register a Microsoft Azure application

You need to register a [new application on Microsoft Azure](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app).

![azure-integration1](../../content/images/integrations/sso/azure.png)

You should provide a callback URL: [Domain/IP]/oauth/azure

## Update Azure configuration on the settings page

You can now use your client id and secret token to set auth with Azure. In Polyaxon's dashboard on the settings page under `Auth`, you can set the values for `Azure`.

![azure-settings](../../content/images/integrations/sso/azure-settings.png)
