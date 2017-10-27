<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/datasets/flowers17.py#L46)</span>

## filenames_by_classes


```python
filenames_by_classes(dataset_dir, num_images, folds)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/datasets/flowers17.py#L70)</span>

## convert_images


```python
convert_images(session, writer, converter, filesnames_by_classes)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/datasets/flowers17.py#L92)</span>

## prepare_dataset


```python
prepare_dataset(converter, dataset_dir, num_images, folds)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/datasets/flowers17.py#L128)</span>

## prepare


```python
prepare(dataset_dir)
```


Runs download and conversion operation.

- __Args__:
	- __dataset_dir__: The dataset directory where the dataset is stored.


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/datasets/flowers17.py#L161)</span>

## create_input_fn


```python
create_input_fn(dataset_dir)
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/datasets/flowers17.py#L166)</span>

## create_predict_input_fn


```python
create_predict_input_fn(dataset_dir)
```
