<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/pipelines.py#L18)</span>
### Pipeline

```python
polyaxon.processing.pipelines.Pipeline(mode, name, modules=None, shuffle=True, num_epochs=None)
```

Abstract InputPipeline class. All input pipelines must inherit from this.
An InputPipeline defines how data is read, parsed, and separated into
features and labels.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __name__: `str`, name to give for this pipeline.
- __modules__: `list`, list of modules to call in order to create this pipeline.
- __shuffle__: If true, shuffle the data.
- __num_epochs__: Number of times to iterate through the dataset. If None, iterate forever.

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/pipelines.py#L63)</span>
### TFRecordImagePipeline

```python
polyaxon.processing.pipelines.TFRecordImagePipeline(mode, name, modules=None, shuffle=True, num_epochs=None, data_files=None, meta_data_file=None)
```

Abstract InputPipeline class. All input pipelines must inherit from this.
An InputPipeline defines how data is read, parsed, and separated into
features and labels.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __name__: `str`, name to give for this pipeline.
- __modules__: `list`, list of modules to call in order to create this pipeline.
- __shuffle__: If true, shuffle the data.
- __num_epochs__: Number of times to iterate through the dataset. If None, iterate forever.

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/pipelines.py#L138)</span>
### ParallelTextPipeline

```python
polyaxon.processing.pipelines.ParallelTextPipeline(mode, name, modules=None, shuffle=True, num_epochs=None, source_files=None, target_files=None, source_delimiter='', target_delimiter='')
```

An input pipeline that reads two parallel (line-by-line aligned) text files.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __name__: `str`, name to give for this pipeline.
- __modules__: `list`, list of modules to call in order to create this pipeline.
- __shuffle__: If true, shuffle the data.
- __num_epochs__: Number of times to iterate through the dataset. If None, iterate forever.
- __source_files__: An array of file names for the source data.
- __target_files__: An array of file names for the target data. These must
  be aligned to the `source_files`.
- __source_delimiter__: A character to split the source text on. Defaults
  to  " " (space). For character-level training this can be set to the
  empty string.
- __target_delimiter__: Same as `source_delimiter` but for the target text.

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/pipelines.py#L215)</span>
### TFRecordSourceSequencePipeline

```python
polyaxon.processing.pipelines.TFRecordSourceSequencePipeline(mode, name, modules=None, shuffle=True, num_epochs=None, files=None, source_field='source', target_field='target', source_delimiter='', target_delimiter='')
```

An input pipeline that reads a TFRecords containing both source and target sequences.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __name__: `str`, name to give for this pipeline.
- __modules__: `list`, list of modules to call in order to create this pipeline.
- __shuffle__: If true, shuffle the data.
- __num_epochs__: Number of times to iterate through the dataset. If None, iterate forever.
- __files__: An array of file names to read from.
- __source_field__: The TFRecord feature field containing the source text.
- __target_field__: The TFRecord feature field containing the target text.
- __source_delimiter__: A character to split the source text on. Defaults
  to  " " (space). For character-level training this can be set to the
  empty string.
- __target_delimiter__: Same as `source_delimiter` but for the target text.

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/pipelines.py#L303)</span>
### ImageCaptioningPipeline

```python
polyaxon.processing.pipelines.ImageCaptioningPipeline(mode, name, modules=None, shuffle=True, num_epochs=None, files=None, image_field='image/data', image_format='jpg', caption_ids_field='image/caption_ids', caption_tokens_field='image/caption')
```

An input pipeline that reads a TFRecords containing both source and target sequences.

- __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __name__: `str`, name to give for this pipeline.
- __modules__: `list`, list of modules to call in order to create this pipeline.
- __shuffle__: If true, shuffle the data.
- __num_epochs__: Number of times to iterate through the dataset. If None, iterate forever.
- __files__: An array of file names to read from.
- __image_field__: The TFRecord feature field containing the source images.
- __image_format__: The images extensions.
- __caption_ids_field__: The caption ids field.
- __caption_tokens_field__: the caption tokends field.
