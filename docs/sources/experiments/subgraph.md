<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/subgraph.py#L9)</span>
### SubGraph

```python
polyaxon.experiments.subgraph.SubGraph(mode, name, modules, kwargs)
```

The `SubGraph` is a class that represents the flow of layers.

- __Args__:
- __mode__: `str`. Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __name__: `str`. The name of this subgraph, used for creating the scope.
- __modules__: `list`.  The modules to connect inside this subgraph, e.g. layers
- __kwargs__: `list`. the list key word args to call each method with.
