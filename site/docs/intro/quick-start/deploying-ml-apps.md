---
title: "Quick Start: Deploying ML apps"
sub_link: "quick-start/deploying-ml-apps"
meta_title: "Deploying ML apps - Polyaxon quick start tutorial - Core Concepts"
meta_description: "Deploying ML apps - Become familiar with the ecosystem of Polyaxon tools with a top-level overview and useful links to get you started."
visibility: public
status: published
tags:
    - tutorials
    - concepts
    - notebook
    - quick-start
sidebar: "intro"
---

In this section, we will learn how to train a machine learning model and deploy it as an interactive dashboard.

## Create a new project

Let's create a new project `streamlit-app`:

```bash
polyaxon project create --name=streamlit-app
``` 

## Training a machine learning model

we will train a model to classify Iris flower species from its features.

Iris features: `Sepal, Petal, lengths, and widths`

### Exploring the datasets

We will start first by exploring the iris dataset in a notebook session running on our Kubernetes cluster.

Let's start a new notebook session and wait until it reaches the running state:

```bash
polyaxon run --hub jupyterlab -w
```

Let's create a new notebook and start by examining the dataset's features:

![Explore the dataset](../../../../content/images/dashboard/runs/notebook-explore-dataset.png)

Commands executed:

```python
from sklearn.datasets import load_iris

iris= load_iris()

print(iris.feature_names)
print(iris.target_names)
print(iris.data.shape)
print(iris.target.shape)
print(iris.target)
```

### Exploring the model

There are different classes of algorithms that scikit-learn offers, in the scope of this tutorial, we will use [Nearest Neighbors algorithm](https://scikit-learn.org/stable/modules/neighbors.html).

Before we create a robust script, we will play around with a simple model in our notebook session:

![explore-models](../../../../content/images/dashboard/runs/notebook-explore-models.png)

Commands executed:

```python
from sklearn.neighbors import KNeighborsClassifier

X = iris.data
y = iris.target

classifier = KNeighborsClassifier(n_neighbors=3)
# Fit the model
classifier.fit(X, y)

# Predict new data
new_data = [[3, 2, 5.3, 2.9]]
print(classifier.predict(new_data))

# Show the results
print(iris.target_names[classifier.predict(new_data)])
```

In this case we used `n_neighbors=3` and the complete dataset for training the model.

In order to explore different variants of our model, we need to make a script for our model, and parametrize the inputs and outputs, to easily change the parameters such as `n_neighbors` we also need to establish some rigorous way of estimating the **performance of the model**.

A practical way of doing that, is by creating an evaluation procedure where we would split the dataset to **training and testing**. We train the model on the training set and evaluate it on the testing set.

scikit-learn provides methods to split a dataset:

```bash
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1012)
```

### Productionizing the model training

Now that we established some practices let's create a function that accepts parameters, trains the model, and saves the resulting score:

```python
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.datasets import load_iris
try:
    from sklearn.externals import joblib
except:
    pass

def train_and_eval(
    n_neighbors=3,
    leaf_size=30,
    metric='minkowski',
    p=2,
    weights='uniform',
    test_size=0.3,
    random_state=1012,
    model_path=None,
):
    iris = load_iris()
    X = iris.data
    y = iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    classifier = KNeighborsClassifier(n_neighbors=n_neighbors, leaf_size=leaf_size, metric=metric, p=p, weights=weights)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)
    recall = metrics.recall_score(y_test, y_pred, average='weighted')
    f1 = metrics.f1_score(y_pred, y_pred, average='weighted')
    results = {
        'accuracy': accuracy,
        'recall': recall,
        'f1': f1,
    }
    if model_path:
        joblib.dump(classifier, model_path)
    return results
```

Now we have a script that accepts parameters to evaluate the model based on different inputs, saves the model and returns the results, but this is still very manual, and for larger and more complex models this is very impractical.

### Running experiments with Polyaxon

Instead of running the model by manually changing the values in the notebook, we will create a script and run the model using Polyaxon. We will also log the resulting metrics and model using [Polyaxon's tracking module](https://polyaxon.com/docs/experimentation/tracking/).
The code for the model that we will train can be found in this [github repo](https://github.com/polyaxon/polyaxon-examples/tree/master/in_cluster/sklearn/iris).

Running the example with the default parameters:

```bash
polyaxon run --url=https://raw.githubusercontent.com/polyaxon/polyaxon-examples/master/in_cluster/sklearn/iris/polyaxonfile.yml -l
```

Running with a different parameters:

```bash
polyaxon run --url=https://raw.githubusercontent.com/polyaxon/polyaxon-examples/master/in_cluster/sklearn/iris/polyaxonfile.yml -l -P n_neighbors=50
```

### Scheduling multiple parallel experiments

Instead of manually changing the parameters, we will automate this process by exploring a space of configurations:

```bash
polyaxon run --url=https://raw.githubusercontent.com/polyaxon/polyaxon-examples/master/in_cluster/sklearn/iris/hyper-polyaxonfile.yml --eager
```

You will see the CLI creating several experiments that will run in parallel:

```bash
Starting eager mode...
Creating 15 operations
A new run `b6cdaaee8ce74e25bc057e23196b24e6` was created
...
```

### Analyzing the experiments

Sorting the experiments based on their accuracy metric

![sorting-experiments](../../../../content/images/dashboard/runs/notebook-sorting-experiments.png)

Comparing `accuracy` against `n_neighbors`

![visualizing-accuracy-n_neighbors](../../../../content/images/dashboard/runs/visualizing-accuracy-n_neighbors.png)

### Selecting and deploying the best model by accuracy as an Iris Classification App

In our script we used Polyaxon to log a model every time we run an experiment:

```python
# Logging the model
tracking.log_model(model_path, name="iris-model", framework="scikit-learn")
```

We will deploy a simple streamlit app that will load our model and display an app that makes a prediction based on the features and displays an image corresponding to the flower class.


```python
import streamlit as st
import pandas as pd
import joblib
import argparse

from PIL import Image


def load_model(model_path: str):
    model = open(model_path, "rb")
    return joblib.load(model)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--model-path',
        type=str,
    )
    args = parser.parse_args()

    setosa = Image.open("images/iris-setosa.png")
    versicolor = Image.open("images/iris-versicolor.png")
    virginica = Image.open("images/iris-virginica.png")
    classifier = load_model(args.model_path)

    st.title("Iris flower species Classification")
    st.sidebar.title("Features")
    parameter_list = [
        "Sepal length (cm)",
        "Sepal Width (cm)",
        "Petal length (cm)",
        "Petal Width (cm)"
    ]
    sliders = []
    for parameter, parameter_df in zip(parameter_list, ['5.2', '3.2', '4.2', '1.2']):
        values = st.sidebar.slider(
            label=parameter,
            key=parameter,
            value=float(parameter_df),
            min_value=0.0,
            max_value=8.0,
            step=0.1
        )
        sliders.append(values)

    input_variables = pd.DataFrame([sliders], columns=parameter_list)

    prediction = classifier.predict(input_variables)
    if prediction == 0:

    elif prediction == 1:
        st.image(versicolor)
    else:
        st.image(virginica)
```

We will use a custom component instead of using the generic Streamlit component:

```yaml
version: 1.1
kind: component
name: iris-classification
tags: ["streamlit", "app"]

inputs:
- name: uuid
  isOptional: true
  type: str

run:
  kind: service
  ports: [8501]
  rewritePath: true
  init:
  - git: {"url": "https://github.com/polyaxon/polyaxon-examples"}
  - artifacts: {"files": ["{{ uuid }}/assets/model/iris-model.joblib"]}
  container:
    image: polyaxon/polyaxon-contrib
    workingDir: "{{ globals.artifacts_path }}/polyaxon-examples/in_cluster/sklearn/iris"
    command: [streamlit, run, app.py]
    args: ["--", "--model-path={{ globals.artifacts_path }}/{{ uuid }}/assets/model/iris-model.joblib"]
```

The reason why we are creating a new component instead of use the generic component is to simplify the experience of starting a new streamlit dashboard based on a run uuid.

Let's schedule the app with Polyaxon: 

```bash
polyaxon run --url=https://raw.githubusercontent.com/polyaxon/polyaxon-examples/master/in_cluster/sklearn/iris/streamlit-polyaxonfile.yml -P uuid=86ffaea976c647fba813fca9153781ff
```

> Note that the uuid `86ffaea976c647fba813fca9153781ff` will be different in your use case.

![classification-app](../../../../content/images/dashboard/runs/classification-app.png)

