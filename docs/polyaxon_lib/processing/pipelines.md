<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/processing/pipelines.py#L106)</span>
## TFRecordImagePipelineConfig

```python
polyaxon_schemas.processing.pipelines.TFRecordImagePipelineConfig(data_files, meta_data_file, name='TFRecordImagePipeline')
```

A Pipeline to convert TF-Records to images.

- __Args__:

	- __name__: `str`, name to give for this pipeline.

	- __feature_processors__: `dict`, list of modules to call for each feature to be processed.

	- __shuffle__: `bool`, If true, shuffle the data.

	- __num_epochs__: `int`, Number of times to iterate through the dataset. If None, iterate forever.

	- __batch_size__: The new batch size pulled from the queue (all queues will have the same size).

		If a list is passed in then each bucket will have a different batch_size.
		(python int, int32 scalar or iterable of integers of length num_buckets).
	- __bucket_boundaries__: `list` of `int` or `None`, increasing non-negative numbers.

		The edges of the buckets to use when bucketing tensors.
		Two extra buckets are created, one for input_length < bucket_boundaries[0]
		and one for input_length >= bucket_boundaries[-1].
	- __allow_smaller_final_batch__: `bool`, whether to allow a last small batch.

	- __dynamic_pad__: `bool`, Allow variable dimensions in input shapes.

		The given dimensions are padded upon dequeue so that tensors
		within a batch have the same shapes.
	- __min_after_dequeue__: `int`.

	- __num_threads__: `int`. The number of threads enqueuing tensors.

	- __capacity__: `int`, The maximum number of minibatches in the top queue,

		and also the maximum number of elements within each bucket.
	- __data_files__: `list` of `str`. List of the filenames for data.

	- __meta_data_file__: `str`. Metadata filename


Polyaxonfile usage:

```yaml
TFRecordImagePipeline:
  batch_size: 64
  num_epochs: 1
  shuffle: true
  dynamic_pad: false
  data_files: ["../data/mnist/mnist_train.tfrecord"]
  meta_data_file: "../data/mnist/meta_data.json"
  feature_processors:
	image:
	  input_layers: [image]
	  layers:
		- Cast:
			dtype: float32
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/processing/pipelines.py#L175)</span>
## TFRecordSequencePipelineConfig

```python
polyaxon_schemas.processing.pipelines.TFRecordSequencePipelineConfig(data_files, meta_data_file, name='TFRecordSequencePipeline')
```

A Pipeline to convert TF-Records to sequences.

At least one sequence must be `source_token`.

- __Args__:

	- __name__: `str`, name to give for this pipeline.

	- __feature_processors__: `dict`, list of modules to call for each feature to be processed.

	- __shuffle__: `bool`, If true, shuffle the data.

	- __num_epochs__: `int`, Number of times to iterate through the dataset. If None, iterate forever.

	- __batch_size__: The new batch size pulled from the queue (all queues will have the same size).

		If a list is passed in then each bucket will have a different batch_size.
		(python int, int32 scalar or iterable of integers of length num_buckets).
	- __bucket_boundaries__: `list` of `int` or `None`, increasing non-negative numbers.

		The edges of the buckets to use when bucketing tensors.
		Two extra buckets are created, one for input_length < bucket_boundaries[0]
		and one for input_length >= bucket_boundaries[-1].
	- __allow_smaller_final_batch__: `bool`, whether to allow a last small batch.

	- __dynamic_pad__: `bool`, Allow variable dimensions in input shapes.

		The given dimensions are padded upon dequeue so that tensors
		within a batch have the same shapes.
	- __min_after_dequeue__: `int`.

	- __num_threads__: `int`. The number of threads enqueuing tensors.

	- __capacity__: `int`, The maximum number of minibatches in the top queue,

		and also the maximum number of elements within each bucket.
	- __data_files__: `list` of `str`. List of the filenames for data.

	- __meta_data_file__: `str`. Metadata filename


Polyaxonfile usage:

```yaml
TFRecordSequencePipeline:
  batch_size: 64
  num_epochs: 1
  shuffle: true
  dynamic_pad: false
  data_files: ["data.tfrecord"]
  meta_data_file: "meta_data.json"
  feature_processors:
	image:
	  input_layers: [sequence]
	  layers:
		- Cast:
			dtype: float32
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/processing/pipelines.py#L248)</span>
## ParallelTextPipelineConfig

```python
polyaxon_schemas.processing.pipelines.ParallelTextPipelineConfig(source_files=None, target_files=None, source_delimiter='', target_delimiter='', name='ParallelTextPipeline')
```

An input pipeline that reads two parallel (line-by-line aligned) text files.

- __Args__:

	- __name__: `str`, name to give for this pipeline.

	- __feature_processors__: `dict`, list of modules to call for each feature to be processed.

	- __shuffle__: `bool`, If true, shuffle the data.

	- __num_epochs__: `int`, Number of times to iterate through the dataset. If None, iterate forever.

	- __batch_size__: The new batch size pulled from the queue (all queues will have the same size).

		If a list is passed in then each bucket will have a different batch_size.
		(python int, int32 scalar or iterable of integers of length num_buckets).
	- __bucket_boundaries__: `list` of `int` or `None`, increasing non-negative numbers.

		The edges of the buckets to use when bucketing tensors.
		Two extra buckets are created, one for input_length < bucket_boundaries[0]
		and one for input_length >= bucket_boundaries[-1].
	- __allow_smaller_final_batch__: `bool`, whether to allow a last small batch.

	- __dynamic_pad__: `bool`, Allow variable dimensions in input shapes.

		The given dimensions are padded upon dequeue so that tensors
		within a batch have the same shapes.
	- __min_after_dequeue__: `int`.

	- __num_threads__: `int`. The number of threads enqueuing tensors.

	- __capacity__: `int`, The maximum number of minibatches in the top queue,

		and also the maximum number of elements within each bucket.
	- __source_files__: An array of file names for the source data.

	- __target_files__: An array of file names for the target data. These must

	  be aligned to the `source_files`.
	- __source_delimiter__: A character to split the source text on. Defaults

	  to  " " (space). For character-level training this can be set to the
	  empty string.
	- __target_delimiter__: Same as `source_delimiter` but for the target text.



----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/processing/pipelines.py#L315)</span>
## TFRecordSourceSequencePipelineConfig

```python
polyaxon_schemas.processing.pipelines.TFRecordSourceSequencePipelineConfig(files=None, source_field='source', target_field='target', source_delimiter='', target_delimiter='', name='TFRecordSourceSequencePipeline')
```

An input pipeline that reads a TFRecords containing both source and target sequences.

- __Args__:

	- __name__: `str`, name to give for this pipeline.

	- __feature_processors__: `dict`, list of modules to call for each feature to be processed.

	- __shuffle__: `bool`, If true, shuffle the data.

	- __num_epochs__: `int`, Number of times to iterate through the dataset. If None, iterate forever.

	- __batch_size__: The new batch size pulled from the queue (all queues will have the same size).

		If a list is passed in then each bucket will have a different batch_size.
		(python int, int32 scalar or iterable of integers of length num_buckets).
	- __bucket_boundaries__: `list` of `int` or `None`, increasing non-negative numbers.

		The edges of the buckets to use when bucketing tensors.
		Two extra buckets are created, one for input_length < bucket_boundaries[0]
		and one for input_length >= bucket_boundaries[-1].
	- __allow_smaller_final_batch__: `bool`, whether to allow a last small batch.

	- __dynamic_pad__: `bool`, Allow variable dimensions in input shapes.

		The given dimensions are padded upon dequeue so that tensors
		within a batch have the same shapes.
	- __min_after_dequeue__: `int`.

	- __num_threads__: `int`. The number of threads enqueuing tensors.

	- __capacity__: `int`, The maximum number of minibatches in the top queue,

		and also the maximum number of elements within each bucket.
	- __source_field__: The TFRecord feature field containing the source text.

	- __target_field__: The TFRecord feature field containing the target text.

	- __source_delimiter__: A character to split the source text on. Defaults

	  to  " " (space). For character-level training this can be set to the
	  empty string.
	- __target_delimiter__: Same as `source_delimiter` but for the target text.



----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/processing/pipelines.py#L383)</span>
## ImageCaptioningPipelineConfig

```python
polyaxon_schemas.processing.pipelines.ImageCaptioningPipelineConfig(files=None, image_field='image/data', image_format='jpg', caption_ids_field='image/caption_ids', caption_tokens_field='image/caption', name='ImageCaptioningPipeline')
```

An input pipeline that reads a TFRecords containing both source and target sequences.

- __Args__:

	- __name__: `str`, name to give for this pipeline.

	- __feature_processors__: `dict`, list of modules to call for each feature to be processed.

	- __shuffle__: `bool`, If true, shuffle the data.

	- __num_epochs__: `int`, Number of times to iterate through the dataset. If None, iterate forever.

	- __batch_size__: The new batch size pulled from the queue (all queues will have the same size).

		If a list is passed in then each bucket will have a different batch_size.
		(python int, int32 scalar or iterable of integers of length num_buckets).
	- __bucket_boundaries__: `list` of `int` or `None`, increasing non-negative numbers.

		The edges of the buckets to use when bucketing tensors.
		Two extra buckets are created, one for input_length < bucket_boundaries[0]
		and one for input_length >= bucket_boundaries[-1].
	- __allow_smaller_final_batch__: `bool`, whether to allow a last small batch.

	- __dynamic_pad__: `bool`, Allow variable dimensions in input shapes.

		The given dimensions are padded upon dequeue so that tensors
		within a batch have the same shapes.
	- __min_after_dequeue__: `int`.

	- __num_threads__: `int`. The number of threads enqueuing tensors.

	- __capacity__: `int`, The maximum number of minibatches in the top queue,

		and also the maximum number of elements within each bucket.
	- __files__: An array of file names to read from.

	- __image_field__: The TFRecord feature field containing the source images.

	- __image_format__: The images extensions.

	- __caption_ids_field__: The caption ids field.

	- __caption_tokens_field__: the caption tokends field.

