---
title: "Tracking Artifacts"
sub_link: "tracking/tracking-artifacts"
meta_title: "Add artifact tracking and log metadata to the lineage table - Tracking - Experimentation"
meta_description: "Add artifact tracking and log metadata to the lineage table."
visibility: public
status: published
tags:
  - tracking
  - reference
  - polyaxon
  - client
  - sdk
sidebar: "experimentation"
---

Polyaxon provides two methods for tracking assets and artifacts that you generate in your jobs:

 * Versioned assets.
 * Reference-only lineage metadata.
 
## Overview

For each run, Polyaxon create an artifacts folder with a predefined structure to organizes your assets and outputs.
 * outputs
 * assets
 * events
 * plxlogs
 * resources

Users might also save content in other subpaths as they wish, for instance uploading data to `uploads` or `code`. 

For each run, users can get the artifacts_path and outputs_path using:

 * `tracking.get_artifacts_path()`
 * `tracking.get_outputs_path()`
 
They can also get a relative path to these root paths:

 * `tracking.get_artifacts_path("code/file.py")`
 * `tracking.get_outputs_path("model/model.h5")`

Polyaxon also exposes two types of logging methods:

 * Reference logging: these are the methods ending with `_ref`, they generally only log the lineage reference, the user has to save the artifact manually.
 * Versioned assets logging: These are the methods that save both the assets and the corresponding event file.

## Reference logging

Reference logging is useful when the user needs to:

 * have more control where the asset must be saved.
 * do not need to log multiple versions of the asset during the run, i.e. the asset is only saved once.
 
In reference logging the user is responsible for saving the artifacts, you can use a relative path to the run's root artifacts or a relative path to the run's outputs path:

 * `tracking.get_artifacts_path("code/file.py")`
 * `tracking.get_outputs_path("model/model.h5")`
 
After saving the artifact under that path, you can decide if you want to create a new entry in the lineage table:

```python
asset_path = tracking.get_artifacts_path("custom_artifacts/filename.ext")
custom_logic_to_save_the_file(asset_path)
# This is optional
tracking.log_artifact_ref(path=asset_path, ...)
```

Sometimes you will need to save an artifact on different backend and not on the artifact store, you can still use the ref to log the lineage:

```python
asset_path = "{}/file.ext".format(S3_URI)
custom_logic_to_save_in_s3(asset_path)

# Tracking lineage only
tracking.log_artifact_ref(path=asset_path, name="myfile", summary={"extra_key": "extra_value"}, ...)
```

In this case the file was not saved to the default artifacts store, but it was saved to a custom S3 bucket. And we added a new entry in the lineage table with that information.

In reference lineage tracking, you can also provide extra key/value summary to augment the lineage information.

## Versioned assets logging

Versioned assets logging is useful when the user needs to save the same asset but several times in the same run, based on timestamp values and/or steps.
For that the tracking module will automatically generate a new subpath under the `assets` sub-folder, e.g. `assets/model/dirname_STEP_NUMBER` or `assets/audio/filename_STEP_NUMBER`,
and each time a logging method is called with the same artifact name, it will create a new entry in the event file and and a new subpath with the step number.

Usually users should use the versioned logging when they need an easy way to explore a specific versioned artifact in the dashboards tab, 
the UI will create a widget with a step slider to load a new file version based on the step number.
 
> **Note**: some logging functions do not save assets, they just populate the event file with new values, for instance scalars/metrics/text tracking.
