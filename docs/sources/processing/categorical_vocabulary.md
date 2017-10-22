<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/categorical.py#L7)</span>
## CategoricalVocabulary

```python
tensorflow.contrib.learn.python.learn.preprocessing.categorical_vocabulary.CategoricalVocabulary(unknown_token='<UNK>', support_reverse=True)
```

Categorical variables vocabulary class.

Accumulates and provides mapping from classes to indexes.
Can be easily used for words.


----

### freeze


```python
freeze(self, freeze=True)
```


Freezes the vocabulary, after which new words return unknown token id.

- __Args__:
  - __freeze__: True to freeze, False to unfreeze.


----

### get


```python
get(self, category)
```


Returns word's id in the vocabulary.

If category is new, creates a new id for it.

- __Args__:
  - __category__: string or integer to lookup in vocabulary.

- __Returns__:
  interger, id in the vocabulary.


----

### add


```python
add(self, category, count=1)
```


Adds count of the category to the frequency table.

- __Args__:
  - __category__: string or integer, category to add frequency to.
  - __count__: optional integer, how many to add.


----

### trim


```python
trim(self, min_frequency, max_frequency=-1)
```


Trims vocabulary for minimum frequency.

Remaps ids from 1..n in sort frequency order.
where n - number of elements left.

- __Args__:
  - __min_frequency__: minimum frequency to keep.
  - __max_frequency__: optional, maximum frequency to keep.
Useful to remove very frequent categories (like stop words).


----

### reverse


```python
reverse(self, class_id)
```


Given class id reverse to original class name.

- __Args__:
  - __class_id__: Id of the class.

- __Returns__:
  Class name.

- __Raises__:
  - __ValueError__: if this vocabulary wasn't initialized with support_reverse.
