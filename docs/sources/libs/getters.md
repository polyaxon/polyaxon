## get_optimizer


```python
get_optimizer(module)
```


----

## get_activation


```python
get_activation(module)
```


----

## get_initializer


```python
get_initializer(module)
```


----

## get_regularizer


```python
get_regularizer(module)
```


----

## get_metric


```python
get_metric(module, incoming, outputs)
```


----

## get_eval_metric


```python
get_eval_metric(module, y_pred, y_true)
```


----

## get_loss


```python
get_loss(module, y_pred, y_true)
```


----

## get_pipeline


```python
get_pipeline(module, mode, shuffle, num_epochs, subgraph_configs_by_features=None)
```


----

## get_graph_fn


```python
get_graph_fn(config, graph_class=None)
```


Creates the graph operations.

----

## get_bridge_fn


```python
get_bridge_fn(config)
```


Creates a bridge function. Defaults to `NoOpBridge`

- __Args__:
	- __config__: `BridgeConfig` instance.

- __Returns__:
	`function`.


----

## get_model_fn


```python
get_model_fn(model_config, graph_fn=None, encoder_fn=None, decoder_fn=None, bridge_fn=None)
```


----

## get_estimator


```python
get_estimator(estimator_config, model_config, run_config)
```


----

## get_hooks


```python
get_hooks(hooks_config)
```
