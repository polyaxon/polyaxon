<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/data_providers.py#L15)</span>
### Dataset

```python
polyaxon.processing.data_providers.Dataset(data_sources, reader, decoder, num_samples=None, items_to_descriptions=None, meta_data=None)
```

Represents a Dataset specification.
----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/data_providers.py#L43)</span>
### DataProvider

```python
polyaxon.processing.data_providers.DataProvider(items_to_tensors, num_samples)
```

Maps a list of requested data items to tensors from a data source.
(A mirror to tf.slim.data DataProvider)

All data providers must inherit from DataProvider and implement the Get
method which returns arbitrary types of data. No assumption is made about the
source of the data nor the mechanism for providing it.

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/data_providers.py#L118)</span>
### DatasetDataProvider

```python
polyaxon.processing.data_providers.DatasetDataProvider(dataset, num_readers=1, reader_kwargs=None, shuffle=True, num_epochs=None, common_queue_capacity=256, common_queue_min=128, record_key='__record_key__', seed=None, scope=None)
```

----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/processing/data_providers.py#L164)</span>
### ParallelDatasetProvider

```python
polyaxon.processing.data_providers.ParallelDatasetProvider(dataset_source, dataset_target, shuffle=True, num_epochs=None, common_queue_capacity=4096, common_queue_min=1024, seed=None)
```

Creates a ParallelDatasetProvider. This data provider reads two datasets
in parallel, keeping them aligned.

- __Args__:
	- __dataset_source__: The first dataset. An instance of the Dataset class.
	- __dataset_target__: The second dataset. An instance of the Dataset class.
	Can be None. If None, only `dataset1` is read.
	- __shuffle__: Whether to shuffle the data sources and common queue when
	  reading.
	- __num_epochs__: The number of times each data source is read. If left as None,
	  the data will be cycled through indefinitely.
	- __common_queue_capacity__: The capacity of the common queue.
	- __common_queue_min__: The minimum number of elements in the common queue after a dequeue.
	- __seed__: The seed to use if shuffling.
  