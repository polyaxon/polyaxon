## variable


```python
variable()
```


Instantiate a new variable.

- __Args__:
	- __name__: `str`. A name for this variable.
	- __shape__: list of `int`. The variable shape (optional).
	- __dtype__: `type`. The variable data type.
	- __initializer__: `str` or `Tensor`. The variable initialization.
	- __regularizer__: `str` or `Tensor`. The variable regularizer.
	- __trainable__: `bool`. If True, this variable weights will be trained.
	- __collections__: `str`. A collection to add the new variable to (optional).
	- __device__: `str`. Device ID to store the variable. Default: '/cpu:0'.
	- __restore__: `bool`. Restore or not this variable when loading a pre-trained model.

- __Returns__:
	A Variable.
