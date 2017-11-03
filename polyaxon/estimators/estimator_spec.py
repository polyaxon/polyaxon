# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import collections
import six

from tensorflow.python.estimator.model_fn import EstimatorSpec as _EstimatorSpec
from tensorflow.python.framework import ops


class EstimatorSpec(
    collections.namedtuple('EstimatorSpec', [
        'predictions', 'loss', 'train_op', 'eval_metric_ops', 'extra_ops',
        'export_outputs', 'training_chief_hooks', 'training_hooks',
        'scaffold', 'evaluation_hooks']), _EstimatorSpec):
    """Ops and objects returned from a `model_fn` and passed to `Estimator`.

    This extends the Tensorflow `EstimatorSpec` with `extra_ops`

    `EstimatorSpec` fully defines the model to be run by `Estimator`.

    Creates a validated `EstimatorSpec` instance.

    Depending on the value of `mode`, different arguments are required. Namely
    * For `mode == ModeKeys.TRAIN`: required fields are `loss` and `train_op`.
    * For `mode == ModeKeys.EVAL`: required field is`loss`.
    * For `mode == ModeKeys.PREDICT`: required fields are `predictions`.

    model_fn can populate all arguments independent of mode. In this case, some
    arguments will be ignored by `Estimator`. E.g. `train_op` will be ignored
    in eval and infer modes. Example:

    ```python
    >>> def my_model_fn(mode, features, labels):
    >>>     predictions = ...
    >>>     loss = ...
    >>>     train_op = ...
    >>>     return tf.estimator.EstimatorSpec(
    ...         mode=mode, predictions=predictions, loss=loss, train_op=train_op)
    ```

    Alternatively, model_fn can just populate the arguments appropriate to the
    given mode. Example:

    ```python
    >>> def my_model_fn(mode, features, labels):
    >>>     if (mode == tf.estimator.ModeKeys.TRAIN or mode == tf.estimator.ModeKeys.EVAL):
    >>>         loss = ...
    >>>     else:
    >>>         loss = None
    >>>     if mode == tf.estimator.ModeKeys.TRAIN:
    >>>         train_op = ...
    >>>     else:
    >>>         train_op = None
    >>>     if mode == tf.estimator.ModeKeys.PREDICT:
    >>>         predictions = ...
    >>>     else:
    >>>         predictions = None

    >>>     return tf.estimator.EstimatorSpec(
    ...         mode=mode, predictions=predictions, loss=loss, train_op=train_op)
    ```

    Args:
        mode: A `ModeKeys`. Specifies if this is training, evaluation or prediction.
        predictions: Predictions `Tensor` or dict of `Tensor`.
        loss: Training loss `Tensor`. Must be either scalar, or with shape `[1]`.
        train_op: Op for the training step.
        eval_metric_ops: Dict of metric results keyed by name. The values of the
            dict are the results of calling a metric function, namely a
            `(metric_tensor, update_op)` tuple.
        export_outputs: Describes the output signatures to be exported to
            `SavedModel` and used during serving.
            A dict `{name: output}` where:
            * name: An arbitrary name for this output.
            * output: an `ExportOutput` object such as `ClassificationOutput`,
                `RegressionOutput`, or `PredictOutput`.
            Single-headed models only need to specify one entry in this dictionary.
            Multi-headed models should specify one entry for each head, one of
            which must be named using
            signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY.
        training_chief_hooks: A list of `tf.train.SessionRunHook` objects to
            run on the chief worker during training.
        training_hooks: A list of `tf.train.SessionRunHook` objects that to run on
            all workers during training.
        scaffold: A `tf.train.Scaffold` object that can be used to set
            initialization, saver, and more to be used in training.

    Returns:
        A validated `EstimatorSpec` object.

    Raises:
        ValueError: If validation fails.
        TypeError: If any of the arguments is not the expected type.
    """

    def __new__(cls, mode,
                predictions=None,
                loss=None,
                train_op=None,
                eval_metric_ops=None,
                extra_ops=None,
                export_outputs=None,
                training_chief_hooks=None,
                training_hooks=None,
                scaffold=None,
                evaluation_hooks=None):
        try:
            spec = _EstimatorSpec(
                mode=mode,
                predictions=predictions,
                loss=loss,
                train_op=train_op,
                eval_metric_ops=eval_metric_ops,
                export_outputs=export_outputs,
                training_chief_hooks=training_chief_hooks,
                training_hooks=training_hooks,
                scaffold=scaffold,
                evaluation_hooks=evaluation_hooks)
        except TypeError:
            spec = _EstimatorSpec(
                mode=mode,
                predictions=predictions,
                loss=loss,
                train_op=train_op,
                eval_metric_ops=eval_metric_ops,
                export_outputs=export_outputs,
                training_chief_hooks=training_chief_hooks,
                training_hooks=training_hooks,
                scaffold=scaffold)
            spec.evaluation_hooks = evaluation_hooks
        if extra_ops is None:
            extra_ops = {}
        else:
            if isinstance(extra_ops, dict):
                for k, v in six.iteritems(extra_ops):
                    _check_is_tensor_or_operation(v, 'extra_ops[{}]'.format(k))
            else:
                _check_is_tensor_or_operation(extra_ops, 'extra_ops')

        return super(EstimatorSpec, cls).__new__(
            cls,
            predictions=spec.predictions,
            loss=spec.loss,
            train_op=spec.train_op,
            eval_metric_ops=spec.eval_metric_ops,
            extra_ops=extra_ops,
            export_outputs=spec.export_outputs,
            training_chief_hooks=spec.training_chief_hooks,
            training_hooks=spec.training_hooks,
            scaffold=spec.scaffold,
            evaluation_hooks=spec.evaluation_hooks)


def _check_is_tensor_or_operation(x, name):
    if not isinstance(x, (ops.Operation, ops.Tensor)):
        raise TypeError('{} must be Operation or Tensor, given: {}'.format(name, x))
