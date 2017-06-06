<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/subgraph.py#L17)</span>
### SubGraph

```python
polyaxon.experiments.subgraph.SubGraph(mode, name, modules, features=None)
```

The `SubGraph` is a class that represents the flow of layers.

- __Args__:
- __mode__: `str`. Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __name__: `str`. The name of this subgraph, used for creating the scope.
- __modules__: `list`.  The modules to connect inside this subgraph, e.g. layers
- __kwargs__: `list`. The list key word args to call each method with.
- __features__: `list`. The list of features keys to extract and use in this subgraph.
	If `None`, all features will be used.
