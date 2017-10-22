# Introduction

Polyaxon encapsulate all configurations needed to train and evaluate a model in `Experiments`.

An `Experiment` expects a training (and evaluation) data pipeline, a model, and knows how to invoke the training from the estimator.

In case of a reinforcement learning problem, the `RLExperiment` expects an environment, a model, and knows how to invoke the training from the agent.

You can train your estimator pragmatically by invoking the training the experiment directly, or by using the the utils functions provided.

An `Experiement` can be created directly by instantiating the objects needed or by creating a `ExperiemntConfig`.


## Experiment instance

```python
import polyaxon as plx
from tensorflow.python.estimator.inputs.inputs import numpy_input_fn

train_input_fn = numpy_input_fn(X['train'], y['train'], shuffle=True)
eval_input_fn = numpy_input_fn(x['eval'], y['eval'], shuffle=False)
estimator = plx.estimators.Estimator(...)
xp = plx.experiments.Experiment(estimator=estimator, 
                                train_input_fn=train_input_fn,
                                eval_input_fn=eval_input_fn)
xp.train()
```


## Experiment from config

```yaml
version: 1

project:
  name: lenet_mnsit

settings:
  logging:
    level: INFO

environment:
  run_config:
    save_summary_steps: 100
    save_checkpoints_steps: 100

model:
  classifier:
    loss:
      MeanSquaredError:
    optimizer:
      Adam:
        learning_rate: 0.007
        decay_type: exponential_decay
        decay_rate: 0.2
    metrics:
      - TruePositives
      - TrueNegatives
      - FalsePositives
      - FalseNegatives
      - Recall
      - AUC
      - Accuracy
      - Precision
    one_hot_encode: true
    n_classes: 10
    graph:
      input_layers: image
      layers:
        - Conv2D:
            filters: 32
            kernel_size: 5
            strides: 1
        - MaxPooling2D:
            pool_size: 2
        - Conv2D:
            filters: 64
            kernel_size: 5
        - MaxPooling2D:
            pool_size: 2
        - Flatten:
        - Dense:
            units: 1024
            activation: tanh
        - Dense:
           units: 10

train:
  train_steps: 100
  data_pipeline:
    TFRecordImagePipeline:
      batch_size: 64
      num_epochs: 1
      shuffle: true
      data_files: ["../data/mnist/mnist_train.tfrecord"]
      meta_data_file: "../data/mnist/meta_data.json"
      feature_processors:
        image:
          input_layers: [image]
          layers:
            - Cast:
                dtype: float32

eval:
  data_pipeline:
    TFRecordImagePipeline:
      batch_size: 32
      num_epochs: 1
      shuffle: False
      data_files: ["../data/mnist/mnist_eval.tfrecord"]
      meta_data_file: "../data/mnist/meta_data.json"
      feature_processors:
        image:
          input_layers: [image]
          layers:
            - Cast:
                dtype: float32

```


# Polyaxon Estimator

The `Estimator` is where the object responsible for training, evaluating and extracting predictions from the graph model.

An `Estiamtor` expects a function that creates a model graph.  


```python
import polyaxon as plx

def dummy_model_fn(features, labels, mode):
    pass
      
estimator = plx.estimators.Estimator(model_fn=dummy_model_fn)
```

# Polyaxon Model

A `Model` is `GraphModule` subclass where we define the computation graph.

A `Model` expects all information about how to construct the `Graph`, the `Loss`, the evaluation `Metrics`, the `Optimizer` and the summaries level.


```python
from polyaxon_schemas.losses import MeanSquaredErrorConfig
from polyaxon_schemas.optimizers import SGDConfig
import polyaxon as plx

def graph_fn(mode, inputs):
    x = plx.layers.Dense(units=128)(inputs)
    x = plx.layers.Dense(units=64)(inputs)
    return plx.layers.Dense(units=8)(inputs)

def model_fn(features, labels, mode):
    loss = MeanSquaredErrorConfig()
    optimizer = SGDConfig(learning_rate=0.001)
    model = plx.models.Regressor(
    mode=mode, 
    name='my_regressor', 
    graph_fn=graph_fn, 
    loss=loss, 
    optimizer=optimizer)
    
    return model(features=features, labels=labels)
```
