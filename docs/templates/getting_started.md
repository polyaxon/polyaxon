# Polyaxon with an introductory example

```python
import polyaxon as plx

def graph_fn(mode, inputs):
    inference = plx.layers.FullyConnected(mode=mode, n_units=64, activation='tanh')(inputs)
    return plx.layers.FullyConnected(mode=mode, n_units=10)(inference)

results1 = graph_fn(plx.Modes.TRAIN, dataset1)
results2 = graph_fn(plx.Modes.EVAL, dataset2)
```

Same thing can be achieved using `Subgraph`

```python
import polyaxon as plx

graph = plx.experiments.Subgraph(mode=plx.Modes.TRAIN, name='graph',
    methods=[plx.layers.FullyConnected, plx.layers.FullyConnected],
    kwargs=[{'n_units': 64, 'activation': 'tanh'}, {'n_units': 10}])

results1 = graph(dataset1)
results2 = graph(dataset2)
```

The difference between the first approach and second is that the second creates a scope for the subgraph and only builds and connects the layers.


# Important concepts

### GraphModule

Polyaxon make use of tensorflow `tf.make_template` to easily share variables, and all of Polyaxon module inherits from [GraphModule](/experiments/models).
Each Polyaxon module is python object that represent a part of the computation graph.


### Input data

Reading data from a file, set of files, a directory or numpy/pandas objects should be easy and reproducible.

```python
# an example of NUMPY data input configuration
train_data = 'train_input_data_config': {
    'input_type': plx.configs.InputDataConfig.NUMPY,
    'pipeline_config': {'name': 'train', 'batch_size': 64, 'num_epochs': 5,
                        'shuffle': True},
    'x': X_train,
    'y': Y_train
}
```


### Visualization

Visualizing the graph is fully customizable and can be defined by providing the level and types of visualization:

The visualization levels: `activations`, `loss`, `gradients`, `variables`, and `learning_rate`.

The visualization types currently supported: `scalar`, `histogram`, and `image`.
