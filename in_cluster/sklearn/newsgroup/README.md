# News group classification

This is an example to train a classification model for scikit-learn's newsgroup dataset.

- [5\.6\.2\. The 20 newsgroups text dataset — scikit\-learn 0\.19\.2 documentation](https://scikit-learn.org/0.19/datasets/twenty_newsgroups.html)

## Initialize the polyaxon project
First of all, we create the project if you haven't created it yet.
Then, we initialize the command.

```
# Change dorectory to the project.
cd path/to/polyaxon-example/sklearn/newsgroup

# Create the project on the polyaxon environment.
polyaxon project create --name=sklearn-newsgroup --description='newsgroup classification with scikit-learn'

# Initialize the project.
polyaxon init sklearn-newsgroup
```

## Submit the code to the polyaxon environment.
First, we upload the files


```
# Upload the files to the polyaxon environment.
polyaxon upload

# Run the simple training job.
polyaxon run -f polyaxonfile.yml

# Run the hyperparameter tuning job.
polyaxon run -f polyaxon_hyperparams.ytml
```
