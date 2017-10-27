<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/summarizer.py#L14)</span>
## SummaryOptions

```python
polyaxon.models.summarizer.SummaryOptions()
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/summarizer.py#L49)</span>
## SummaryTypes

```python
polyaxon.models.summarizer.SummaryTypes()
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/summarizer.py#L73)</span>

## add_learning_rate_summaries


```python
add_learning_rate_summaries()
```


Adds learning rate summaries. Only works when decaying learning rate is chosen.

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/summarizer.py#L109)</span>

## add_loss_summaries


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

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/summarizer.py#L131)</span>

## add_activations_summary


```python
add_activations_summary(activation_ops)
```


Adds histogram and scalar summary for given activations.

- __Args__:
	- __activation_ops__: A list of `Tensor`. The activations to summarize.

- __Returns__:
	The list of created activation summaries.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/summarizer.py#L152)</span>

## add_gradients_summary


```python
add_gradients_summary(grads)
```


Add histogram summary for given gradients and scalar summary for clipped gradients.

- __Args__:
	- __grads__: A list of `Tensor`. The gradients to summarize.

- __Returns__:
	The list of created gradient summaries.



----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/models/summarizer.py#L184)</span>

## add_trainable_vars_summary


```python
add_trainable_vars_summary(variables)
```


Adds histogram summary for given variables weights.

- __Args__:
	- __variables__: A list of `Variable`. The variables to summarize.

- __Returns__:
	The list of created weights summaries.

