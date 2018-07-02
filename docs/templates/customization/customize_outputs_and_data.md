Polyaxon allows to mount multiple data volumes and outputs,
this could be very useful for large teams who need to either to scale or
to have different teams to have access to different volumes.

This section tries to explain how Polyaxon mounts these volumes for experiments and jobs.

## Chart Definition

The [helm reference](/reference_polyaxon_helm) describes briefly the data and outputs persistence definitions,
and how you can mount volumes, both persistent claims and host paths, here's the example coming from the ref:

```yaml
persistence:
  data:
    data1:
      mountPath: "/data/1"
      hostPath: "/path/to/data"
      readOnly: true
    data2:
      mountPath: "/data/2"
      existingClaim: "data-2-pvc"
    data-foo:
      mountPath: "/data/foo"
      existingClaim: "data-foo-pvc"
  outputs:
    outputs1:
      mountPath: "/outputs/1"
      hostPath: "/path/to/outputs"
      readOnly: true
    outputs2:
      mountPath: "/outputs/2"
      existingClaim: "outputs-2-pvc"
    outputs-foo:
      mountPath: "/outputs/foo"
      existingClaim: "outputs-foo-pvc"
```

## Scheduling

When you define a multi data outputs volumes, Polyaxon has default behavior on how to mount
these volumes for your jobs and experiments, unless you override this default behavior in your polyaxonfiles.

### For data

If the polyaxonfile for running an experiment or a job does not define the data volume or volumes that it needs access to,
Polyaxon will, by default mount all these volumes when it schedules the experiment or the job.

These data volumes will be accessible to you as a dictionary {volume_name: path_to_data},
exported as an env variable `POLYAXON_DATA_PATH`.

You can use as well our `helper` library `polyaxon-helper` to extract this value for you automatically.

If on the other hand, if you wish to only mount a one volume or a subset of the volumes,
you then need to provide this information in the polyaxonfile, e.g.

```yaml
environment:
  persistence:
    data: ['data1', 'data-foo']
```

By providing this persistence subsection,
Polyaxon will only mount these volumes by looking up there names from the defined volumes.


### For outputs

This is also optional and you can only define one volume to use for the outputs for a particular experiment or a job.

If the polyaxonfile for running an experiment or a job does not define the outputs volume,
Polyaxon will, by default mount one volume, either the first one or a random one from the list of the defined volumes.

The outputs volume will be accessible to you as a string `path_to_outputs_for_experiment`,
exported as an env variable `POLYAXON_OUTPUTS_PATH`.

You can use as well our `helper` library `polyaxon-helper` to extract this value for you automatically.

If on the other hand, you wish to mount a particular volume,
you then need to provide this information in the polyaxonfile, e.g.

```yaml
environment:
  persistence:
    outputs: 'outputs-foo'
```

By providing this persistence subsection,
Polyaxon will mount the volume by looking up the name from the defined volumes.
