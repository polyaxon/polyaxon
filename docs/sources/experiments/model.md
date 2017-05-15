<span style="float:right;">[[source]](https://github.com/polyaxon/polyaxon/blob/master/polyaxon/experiments/models.py#L18)</span>
### BaseModel

```python
polyaxon.experiments.models.BaseModel(mode, config, model_type, summaries, name, params)
```

Abstract base class for models.

  - __Args__:
- __mode__: `str`, Specifies if this training, evaluation or prediction. See `ModeKeys`.
- __config__: An instance of `ModelConfig`.
- __params__: `dic`. A dictionary of hyperparameter values.
