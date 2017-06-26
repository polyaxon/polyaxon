# Introduction

Polyaxon encapsulate all configurations needed to train and evaluate a model in `Experiments`.

An `Experiment` expects a training (and evaluation) data pipeline, a model, and knows how to invoke the training from the estimator.

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

```python
import polyaxon as plx
output_dir = ''
config = {
    'name': 'lenet_mnsit',
    'output_dir': output_dir,
    'eval_every_n_steps': 10,
    'train_steps_per_iteration': 100,
    'run_config': {'save_checkpoints_steps': 100},
    'train_input_data_config': {
        'input_type': plx.configs.InputDataConfig.NUMPY,
        'pipeline_config': {'name': 'train', 'batch_size': 64, 'num_epochs': None,
                            'shuffle': True},
        'x': X_train,
        'y': Y_train
    },
    'eval_input_data_config': {
        'input_type': plx.configs.InputDataConfig.NUMPY,
        'pipeline_config': {'name': 'eval', 'batch_size': 32, 'num_epochs': None,
                            'shuffle': False},
        'x': X_test,
        'y': Y_test
    },
    'estimator_config': {'output_dir': output_dir},
    'model_config': {
        'summaries': 'all',
        'module': 'Classifier',
        'loss_config': {'module': 'softmax_cross_entropy'},
        'eval_metrics_config': [{'module': 'streaming_accuracy'},
                                {'module': 'streaming_precision'}],
        'optimizer_config': {'module': 'adam', 'learning_rate': 0.002,
                             'decay_type': 'exponential_decay', 'decay_rate': 0.2},
        'graph_config': {
            'name': 'lenet',
            'definition': [
                (plx.layers.Conv2d, {'num_filter': 32, 'filter_size': 5, 'strides': 1,
                                     'regularizer': 'l2_regularizer'}),
                (plx.layers.MaxPool2d, {'kernel_size': 2}),
                (plx.layers.Conv2d, {'num_filter': 64, 'filter_size': 5,
                                     'regularizer': 'l2_regularizer'}),
                (plx.layers.MaxPool2d, {'kernel_size': 2}),
                (plx.layers.FullyConnected, {'n_units': 1024, 'activation': 'tanh'}),
                (plx.layers.FullyConnected, {'n_units': 10}),
            ]
        }
    }
}
xp_config = plx.configs.ExperimentConfig.read_configs(config)
xp = plx.experiments.create_experiment(xp_config)
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
import polyaxon as plx

def graph_fn(mode, inputs):
    x = plx.layers.FullyConnected(mode, n_units=128)(inputs)
    x = plx.layers.FullyConnected(mode, n_units=64)(inputs)
    return plx.layers.FullyConnected(mode, n_units=8)(inputs)

def model_fn(features, labels, mode):
    loss = plx.configs.LossConfig(module='mean_squared_error')
    optimizer = plx.configs.OptimizerConfig(module='SGD')
    model = plx.models.Regressor(
    mode=mode, name='my_regressor', graph_fn=graph_fn, 
    loss_config=loss, optimizer_config=optimizer)
    
    return model(features=features, labels=labels)
```
