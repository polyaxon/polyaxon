<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/getters.py#L16)</span>

## get_optimizer


```python
get_optimizer(module)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/getters.py#L26)</span>

## get_constraint


```python
get_constraint(module)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/getters.py#L36)</span>

## get_layer


```python
get_layer(module)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/getters.py#L46)</span>

## get_exploration


```python
get_exploration(module)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/getters.py#L61)</span>

## get_activation


```python
get_activation(module)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/getters.py#L73)</span>

## get_initializer


```python
get_initializer(module)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/getters.py#L84)</span>

## get_regularizer


```python
get_regularizer(module)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/getters.py#L93)</span>

## get_metric


```python
get_metric(module, y_pred, y_true)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/getters.py#L140)</span>

## get_loss


```python
get_loss(module, y_pred, y_true)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/getters.py#L178)</span>

## get_memory


```python
get_memory(module)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/getters.py#L190)</span>

## get_pipeline


```python
get_pipeline(module, mode)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/getters.py#L205)</span>

## get_environment


```python
get_environment(module, env_id)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/getters.py#L217)</span>

## get_graph_fn


```python
get_graph_fn(config, graph_class=None)
```


Creates the graph operations.

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/getters.py#L241)</span>

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

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/getters.py#L263)</span>

## get_model_fn


```python
get_model_fn(model_config, graph_fn=None, encoder_fn=None, decoder_fn=None, bridge_fn=None)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/getters.py#L303)</span>

## get_estimator


```python
get_estimator(model, run_config, module='Estimator', output_dir=None)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/getters.py#L320)</span>

## get_agent


```python
get_agent(module, model, memory, run_config, output_dir=None)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/libs/getters.py#L335)</span>

## get_hooks


```python
get_hooks(hooks_config)
```
