<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/summarizer.py#L14)</span>
### SummaryOptions

```python
polyaxon.experiments.summarizer.SummaryOptions()
```

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/summarizer.py#L41)</span>
### SummaryTypes

```python
polyaxon.experiments.summarizer.SummaryTypes()
```

----

### add_learning_rate_summaries


```python
add_learning_rate_summaries()
```

----

### add_loss_summaries


```python
add_loss_summaries(total_loss, loss)
```


Adds loss scalar summaries.

- __Args__:
- __total_loss__: `Tensor`. The total loss (Regression loss + regularization losses).
- __loss__: `Tensor`. Regression loss.

- __Returns__:
The list of created loss summaries.

----

### add_activations_summary


```python
add_activations_summary(activation_ops)
```


Adds histogram and scalar summary for given activations.

- __Args__:
- __activation_ops__: A list of `Tensor`. The activations to summarize.

- __Returns__:
The list of created activation summaries.

----

### add_gradients_summary


```python
add_gradients_summary(grads)
```


Add histogram summary for given gradients and scalar summary for clipped gradients.

- __Args__:
- __grads__: A list of `Tensor`. The gradients to summarize.

- __Returns__:
The list of created gradient summaries.


----

### add_trainable_vars_summary


```python
add_trainable_vars_summary(variables)
```


Adds histogram summary for given variables weights.

- __Args__:
- __variables__: A list of `Variable`. The variables to summarize.

- __Returns__:
The list of created weights summaries.

