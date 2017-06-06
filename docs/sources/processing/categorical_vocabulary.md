<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/categorical.py#L7)</span>
### CategoricalVocabulary

```python
polyaxon.processing.categorical.CategoricalVocabulary(unknown_token='<UNK>', support_reverse=True)
```

Categorical variables vocabulary class.

Accumulates and provides mapping from classes to indexes.
Can be easily used for words.

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/categorical.py#L79)</span>
### CategoricalProcessor

```python
polyaxon.processing.categorical.CategoricalProcessor(min_frequency=0, share=False, vocabularies=None)
```

Maps documents to sequences of word ids.

As a common convention, Nan values are handled as unknown tokens.
Both float('nan') and np.nan are accepted.
