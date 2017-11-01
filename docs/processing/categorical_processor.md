<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/categorical.py#L16)</span>
## CategoricalProcessor

```python
polyaxon.processing.categorical.CategoricalProcessor(min_frequency=0, share=False, vocabularies=None)
```

Maps documents to sequences of word ids.

As a common convention, Nan values are handled as unknown tokens.
Both float('nan') and np.nan are accepted.


----

### freeze


```python
freeze(self, freeze=True)
```


Freeze or unfreeze all vocabularies.

- __Args__:

  - __freeze__: Boolean, indicate if vocabularies should be frozen.



----

### fit


```python
fit(self, x, unused_y=None)
```


Learn a vocabulary dictionary of all categories in `x`.

- __Args__:

  - __x__: numpy matrix or iterable of lists/numpy arrays.

  - __unused_y__: to match fit format signature of estimators.


- __Returns__:

  self


----

### transform


```python
transform(self, x)
```


Transform documents to category-id matrix.

Converts categories to ids give fitted vocabulary from `fit` or
one provided in the constructor.

- __Args__:

  - __x__: numpy matrix or iterable of lists/numpy arrays.


- __Yields__:

  - __x__: iterable, [n_samples]. Category-id matrix.



----

### fit_transform


```python
fit_transform(self, x, unused_y=None)
```


Learn the vocabulary dictionary and return indexies of categories.

- __Args__:

  - __x__: numpy matrix or iterable of lists/numpy arrays.

  - __unused_y__: to match fit_transform signature of estimators.


- __Returns__:

  - __x__: iterable, [n_samples]. Category-id matrix.

