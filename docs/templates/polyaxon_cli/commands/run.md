Usage:

```bash
$ polyaxon run [OPTIONS]
```

Run polyaxonfile specification.

Example:

```
$ polyaxon run -f file -f file_override ...
```

Example upload before running

```bash
$ polyaxon run -f file -u
```

Options:

option | type | description
-------|------|------------
  -f, --file | PATH | The polyaxon files to run.
  --description [optional] | TEXT | The description to give to this run.
  -u | | To upload the repo before running.
  --help | | Show this message and exit.
