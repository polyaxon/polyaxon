## get_optimizer


```python
get_optimizer(module)
```


----

## get_constraint


```python
get_constraint(module)
```


----

## get_layer


```python
get_layer(module)
```


----

## get_exploration


```python
get_exploration(module)
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
get_metric(module, y_pred, y_true)
```


----

## get_loss


```python
get_loss(module, y_pred, y_true)
```


----

## get_memory


```python
get_memory(module)
```


----

## get_pipeline


```python
get_pipeline(module, mode)
```


----

## get_environment


```python
get_environment(module, env_id)
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
get_estimator(model, run_config, module='Estimator', output_dir=None)
```


----

## get_agent


```python
get_agent(module, model, memory, run_config, output_dir=None)
```


----

## get_hooks


```python
get_hooks(hooks_config)
```
