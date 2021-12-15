---
title: "Scheduling operations from an external system"
sub_link: "scheduling-strategies/external-scheduling"
meta_title: "A guide on scheduling and submitting operations from external systems - scheduling strategies"
meta_description: "Automating, scheduling, and submitting operations from external systems."
visibility: public
status: published
tags:
  - concepts
  - tutorials
sidebar: "core"
---

## Overview

Users can drive submissions and automation using external systems via our API, Clients, and CLI.

There are several examples of integrating Polyaxon with some well known [orchestration and automation systems](/integrations/automation/).

## Access Token

If you are using Polyaxon Cloud or Polyaxon EE and you want to automate and submit operations using Polyaxon API, clients, or CLI via an external system, 
we suggest that you create a token specific to those systems.  

Please check the [token management section](/docs/management/organizations/user-profile/#token-management) or the [service accounts section](/docs/management/organizations/service-accounts/) for more details.

## Accessible API

If the external system is not hosted within your network, you will need to expose Polyaxon to the external world. 
If you are a user of Polyaxon Cloud, you do not need to expose your gateway, you can use `cloud.polyaxon.com`, the default host value, to submit operations.

If you use Polyaxon Cloud for submitting operations, Polyaxon will authenticate the requests using the access token used, 
and will compile and route the operation to your agent to run securely in your cluster. 

## Token expiration and revocation

If you do not intend to use a system for a long time, you can set a short expiration for the access token that you create for that system.

You can revoke the token at any time, refresh it, or extend its expiration.

Although Polyaxon will return a `request unauthorized` response if the token is not valid, 
expired or revoked, we suggest that you also cancel any external system subscription from contacting our control plane. 
