# A test Polyaxon project on CIFAR10

## How to create project


### Create project on the cluster
To create a project visible on the dashboard, run (anywhere)
```
polyaxon login
polyaxon project create --name=cifar10 --description='Train and evaluate models on CIFAR-10'
```
and check it out on the dashboard:
```
polyaxon dashboard -y
```

### Initialize project locally

From the folder with the source code of the project
```
polyaxon init cifar10
```
This will create 2 files and a folder:
- polyaxonfile.yml
- .polyaxonignore
- .polyaxon


### Run the first experiment

```
polyaxon run -u -f polyaxonfile_first.yml
```

### Run the second experiment

```
polyaxon run -u -f polyaxonfile_second.yml
```
