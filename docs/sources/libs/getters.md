### get_optimizer


```python
get_optimizer(optimizer)
```

----

### get_activation


```python
get_activation(activation)
```

----

### get_initializer


```python
get_initializer(initializer)
```

----

### get_regularizer


```python
get_regularizer(regularizer)
```

----

### get_metric


```python
get_metric(metric, incoming, outputs)
```

----

### get_eval_metric


```python
get_eval_metric(metric, y_pred, y_true)
```

----

### get_loss


```python
get_loss(loss, y_pred, y_true)
```

----

### get_pipeline


```python
get_pipeline(name, mode, shuffle, num_epochs, subgraph_configs_by_features=None)
```

----

### get_graph_fn


```python
get_graph_fn(config)
```


Creates the graph operations.
----

### get_model_fn


```python
get_model_fn(model_config, graph_fn=None)
```

----

### get_estimator


```python
get_estimator(estimator_config, model_config, run_config)
```

----

### get_hooks


```python
get_hooks(hooks_config)
```
