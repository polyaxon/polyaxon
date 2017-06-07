<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/text.py#L7)</span>
## VocabularyProcessor

```python
polyaxon.processing.text.VocabularyProcessor(max_document_length, min_frequency=0, vocabulary=None, tokenizer_fn=None)
```

A mirror to tf.contrib.learn VocabularyProcessor.

Maps documents to sequences of word ids.

- __Args__:
	- __max_document_length__: Maximum length of documents.
		if documents are longer, they will be trimmed, if shorter - padded.
	- __min_frequency__: Minimum frequency of words in the vocabulary.
	- __vocabulary__: CategoricalVocabulary object.

- __Attributes__:
	- __vocabulary__: CategoricalVocabulary object.


----

### fit


```python
fit(self, raw_documents, unused_y=None)
```


fit.

Learn a vocabulary dictionary of all tokens in the raw documents.

- __Args__:
	- __raw_documents__: An iterable which yield either str or unicode.
	- __unused_y__: to match fit format signature of estimators.

- __Returns__:
	self


----

### transform


```python
transform(self, raw_documents)
```


transform.

Transform documents to word-id matrix.

Convert words to ids with vocabulary fitted with fit or the one
provided in the constructor.

- __Args__:
	- __raw_documents__: An iterable which yield either str or unicode.

- __Yields__:
	- __X__: iterable, [n_samples, max_document_length] Word-id matrix.


----

### fit_transform


```python
fit_transform(self, raw_documents, unused_y=None)
```


fit_transform.

Learn the vocabulary dictionary and return indexies of words.

- __Args__:
	- __raw_documents__: An iterable which yield either str or unicode.
	- __unused_y__: to match fit_transform signature of estimators.

- __Returns__:
	- __X__: iterable, [n_samples, max_document_length] Word-id matrix.


----

### reverse


```python
reverse(self, documents)
```


reverse.

Reverses output of vocabulary mapping to words.

- __Args__:
	- __documents__: iterable, list of class ids.

- __Returns__:
	Iterator over mapped in words documents.


----

### save


```python
save(self, filename)
```


save.

Saves vocabulary processor into given file.

- __Args__:
	- __filename__: Path to output file.


----

### restore


```python
restore(cls, filename)
```


restore.

Restores vocabulary processor from given file.

- __Args__:
	- __filename__: Path to file to load from.

- __Returns__:
	VocabularyProcessor object.
