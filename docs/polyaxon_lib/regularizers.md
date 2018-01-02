<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/regularizations.py#L37)</span>
## L1RegularizerConfig

```python
polyaxon_schemas.regularizations.L1RegularizerConfig(l=0.01, name='L1Regularizer', collect=True)
```

Regularizer for L1 regularization.

- __Args__:

	- __l__: Float; regularization factor.


Polyaxonfile usage:

```yaml
Dense:
  units: 32
  kernel_regularizer: L1
```

or

```yaml
Dense:
  units: 32
  kernel_regularizer:
	L1:
	  l: 0.2
```

or

```yaml
Dense:
  units: 32
  kernel_regularizer:
	L1: {l: 0.2}
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/regularizations.py#L93)</span>
## L2RegularizerConfig

```python
polyaxon_schemas.regularizations.L2RegularizerConfig(l=0.01, name='L2Regularizer', collect=True)
```

Regularizer for L2 regularization.

- __Args__:

	- __l__: Float; regularization factor.


Polyaxonfile usage:

```yaml
Dense:
  units: 32
  kernel_regularizer: L2
```

or

```yaml
Dense:
  units: 32
  kernel_regularizer:
	L2:
	  l: 0.2
```

or

```yaml
Dense:
  units: 32
  kernel_regularizer:
	L2: {l: 0.2}
```


----

<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon_schemas/regularizations.py#L150)</span>
## L1L2RegularizerConfig

```python
polyaxon_schemas.regularizations.L1L2RegularizerConfig(l1=0.01, l2=0.01, name='L1L2Regularizer', collect=True)
```

Regularizer for L1 and L2 regularization.

- __Args__:

	- __l1__: Float; L1 regularization factor.

	- __l2__: Float; L2 regularization factor.


Polyaxonfile usage:

```yaml
Dense:
  units: 32
  kernel_regularizer: L1L2
```

or

```yaml
Dense:
  units: 32
  kernel_regularizer:
	L1L2:
	  l1: 0.2
	  l2: 0.1
```

or

```yaml
Dense:
  units: 32
  kernel_regularizer:
	L1L2: {l1: 0.2, l2: 0.1}
```
