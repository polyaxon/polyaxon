---
title: "Polyaxon Versioning"
sub_link: "versioning"
meta_title: "Polyaxon Versioning - Polyaxon Semantic Versioning Mechanism"
meta_description: "Polyaxon will be following Semantic Versioning."
visibility: public
status: published
tags:
    - reference
---

> We will update this document to reflect any change in our release mechanism.

Since our initial launch, Polyaxon has been pushing releases on a weekly basis, i.e. releasing new features, bug fixes, and improvements every week. 
We believe that it was the right decision to push innovation, test features adoption, and validate hypothesis as quickly as possible. 
As of today, April 2019, Polyaxon has become one of the major Machine Learning platforms, used at many leading institutions, 
and empowering several highly talented teams at startups and Fortune 500 companies.

Our previous versioning mechanism consisted of bumping the PATCH number every week more or less. 
This versioning mechanism, although has several benefits, puts a lot of pressure on teams running Polyaxon in production mode, 
several companies running Polyaxon in production mode have devops teams maintaining several systems and clusters, and Polyaxon is only one of them, 
when they decide to upgrade Polyaxon to a newer version, which happens every month or two and sometimes more, 
they find themselves with several releases, patch notes, and automatic migrations. 
From the point of view of the Polyaxon team, two months of releases, which translate to eight releases, makes it hard to support several versions both in terms of knowledge and documentation.  

## Benefits

Today with the release of latest version Polyaxon, v0.4.4, which we marked as stable and production ready, 
we’re making the switch to [Semantic Versioning](https://semver.org/), this change has the following benefits to the Polyaxon dev team as well as to the teams and community following our product's progress:

 * We will be able to host and support several versions of semantically contained documentation resources.
 * Every time we make a new release with the PATCH change, our users should assume a completely backwards-compatible upgrade.
 * Every time we introduce new migrations (data and db) we will be increasing the MINOR version while providing automatic migration paths.
 * Every time we push a new major functionality we will be increasing the MINOR version.

## Release cycles

One major impact of this change will be the change to our release cycle, instead of just releasing every week, we will be releasing a new version:

  * Whenever a major regression, bug, or security fix is made.
  * Whenever a new improved functionality is developed and tested on different infrastructures.
  * Every 2 weeks/month depending on the scope of the features being developed. 

## Polyaxon v1.0

Although our platform is stable and running in production mode at several organizations (academic and business oriented), 
we believe that v1.0 has a major impact on several CIOs and technical leads' psychology. 
With this new versioning mechanism, Polyaxon will have the chance to reach the v1.0, 
while providing isolated and semantically contained documentation. This is also a strong message to our users, 
that Polyaxon is here for the long haul and is serious about providing the best platform and services to help companies with their ML and AI transition.  

## Other components

In addition to Polyaxon's core functionality, we develop several other aspects and components that we believe have major impact on the productivity of our users. 
These components will be marked separately with alpha/beta until they reach a stable state.
