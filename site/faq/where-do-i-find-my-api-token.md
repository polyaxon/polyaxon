---
title: "Where do I find my API Token?"
meta_title: "Where do I find my API key? - FAQ"
meta_description: "Polyaxon provides several ways for authenticating the CLI and Client, you can login using your username/password or go to your profile page to see the list of your tokens."
featured: false
custom_excerpt: "Polyaxon provides several ways for authenticating the CLI and Client, you can login using your username/password or go to your profile page to see the list of your tokens."
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
visibility: public
status: published
tags:
  - cli
  - api
---

Polyaxon allows to authenticate the CLI and Client using:
 * username (or email) / password 
 * Using one of the tokens specific to a user
 * Using one of the tokens specific to a service account
 
### Using username / password 

In order to login using username (or email) / password, you need to have a valid password setup:

```bash
polyaxon login -u USERNAME -p PASSWORD
```

or 

```bash
polyaxon login -u USERNAME

 > Please enter your password:
```

### Using a user token

To login using one of your tokens, please go to your profile page (`https://HOST:PORT/ui/profile/token`) and select a token or create a new one.

```bash
polyaxon login -t TOKEN
``` 

### Using a service account token

To login using a service account token, you need to be an organization owner or manager. 
Please go to your organization settings page under service account (`https://HOST:PORT//ui/orgs/ORGANIZATION/settings/sa`), 
select a service account or create a new one, and then select a token or create a new one. 

```bash
polyaxon login -t TOKEN
``` 
