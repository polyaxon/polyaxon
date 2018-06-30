Usage:

```bash
$ polyaxon run [OPTIONS]
```

Run polyaxonfile specification.

Examples:

```bash
$ polyaxon run -f file -f file_override ...
```

Upload before running

```bash
$ polyaxon run -f file -u
```

Run and set description and tags for this run

```bash
$ polyaxon run -f file -u --description="Description of the current run" --tags="foo, bar, moo"
```
Run and set a unique name for this run

```bash
polyaxon run --name=foo
```

Options:

option | type | description
-------|------|------------
  -f, --file | PATH | The polyaxon files to run.
  --name [optional] | TEXT | Name to give to this run, must be unique within the project, could be none.
  --description [optional] | TEXT | The description to give to this run.
  --tags [optional] | TEXT | Tags of this run, comma separated values.
  -u [optional] | | To upload the repo before running.
  --help | | Show this message and exit.
