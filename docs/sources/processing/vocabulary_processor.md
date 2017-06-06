<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/text.py#L7)</span>
### VocabularyProcessor

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
