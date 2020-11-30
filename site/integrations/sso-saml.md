---
title: "SSO with SAML"
meta_title: "SAML"
meta_description: "How to use SAML to manage users authentication on Polyaxon."
custom_excerpt: "Security Assertion Markup Language is an open standard for exchanging authentication and authorization data between parties, in particular, between an identity provider and a service provider."
image: "../../content/images/integrations/saml.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags:
  - sso
featured: false
popularity: 0
visibility: public
status: EE
---

You can use SAML to manage your organization’s entire membership.

## Overview

Polyaxon supports using SAML authentication for Single Sign On, both when self-hosting and soon on the Polyaxon Cloud.

## Configure a SAML provider

Polyaxon works with various common SAML Identity Providers: [Okta](https://developer.okta.com/docs/guides/build-sso-integration/saml2/overview/) and [OneLogin](https://support.onelogin.com/hc/en-us/articles/115005181586-Configuring-SAML-for-Sentry).

You should provide a callback URL: `[Domain/IP]/sso/saml`

## Update your deployment config file

Use your information to update your deployment config file.

```yaml
externalServices:
    auth:
      saml:
        enabled: true
        options: {...}
```
