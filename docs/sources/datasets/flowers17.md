### filenames_by_classes


```python
filenames_by_classes(dataset_dir, num_images, folds)
```

----

### convert_images


```python
convert_images(session, writer, converter, filesnames_by_classes)
```

----

### prepare_dataset


```python
prepare_dataset(converter, dataset_dir, num_images, folds)
```

----

### prepare


```python
prepare(dataset_dir)
```


Runs download and conversion operation.

- __Args__:
- __dataset_dir__: The dataset directory where the dataset is stored.

----

### create_input_fn


```python
create_input_fn(dataset_dir)
```
