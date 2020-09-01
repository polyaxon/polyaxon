---
title: "SSO with Google"
meta_title: "SSO with Google"
meta_description: "How to use Google to manage users authentication on Polyaxon. You can easily integrate google to manage users authentication on Polyaxon."
custom_excerpt: "Google launched OAuth2 support following the definition at OAuth2 draft. It works in a similar way to plain OAuth mechanism, but developers must register an application and apply for a set of keys. Check Google OAuth2 document for details."
image: "../../content/images/integrations/google.png"
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

You can use Google to manage your organization’s entire membership.

## Register a Google application

You need to set up [OAuth application](https://console.developers.google.com/) via Google Developers Console.

![google-integration1](../../content/images/integrations/sso/google.png)

You should provide a callback URL: `[Domain/IP]/sso/google`

## Update your deployment config file

Use your client id and secret token to update your deployment config file.

```yaml
externalServices:
    auth:
      google:
        enabled: true
        options: {client_id: "#####", client_secret: "#####"}
```
