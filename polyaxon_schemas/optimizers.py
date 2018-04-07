# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load

from polyaxon_schemas.base import BaseConfig, BaseMultiSchema


class BaseOptimizerSchema(Schema):
    learning_rate = fields.Float(allow_none=True)
    decay_type = fields.Str(allow_none=True)
    decay_rate = fields.Float(allow_none=True)
    decay_steps = fields.Int(allow_none=True)
    start_decay_at = fields.Int(allow_none=True)
    stop_decay_at = fields.Int(allow_none=True)
    min_learning_rate = fields.Float(allow_none=True)
    staircase = fields.Bool(allow_none=True)
    global_step = fields.Str(allow_none=True)
    use_locking = fields.Bool(allow_none=True)
    name = fields.Str(allow_none=True)


class BaseOptimizerConfig(BaseConfig):
    REDUCED_ATTRIBUTES = ['name']

    def __init__(self,
                 learning_rate=0.001,
                 decay_type="",
                 decay_rate=0.,
                 decay_steps=100,
                 start_decay_at=0,
                 stop_decay_at=1e10,
                 min_learning_rate=1e-12,
                 staircase=False,
                 global_step=None,
                 use_locking=False,
                 name='optimizer'):
        self.learning_rate = learning_rate
        self.decay_type = decay_type
        self.decay_rate = decay_rate
        self.decay_steps = decay_steps
        self.start_decay_at = start_decay_at
        self.stop_decay_at = stop_decay_at
        self.min_learning_rate = min_learning_rate
        self.staircase = staircase
        self.global_step = global_step
        self.use_locking = use_locking
        self.name = name


class SGDSchema(BaseOptimizerSchema):
    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return SGDConfig(**data)

    @post_dump
    def unmake(self, data):
        return SGDConfig.remove_reduced_attrs(data)


class SGDConfig(BaseOptimizerConfig):
    """Optimizer that implements the gradient descent algorithm.

    Args:
        learning_rate: A Tensor or a floating point value. The learning rate to use.
        decay_type: A decay function name defined in `tf.train`
        decay_rate: `float`. The learning rate decay to apply.
        decay_steps: `int`. Apply decay every provided steps.
        start_decay_at: `int`. Don't decay before this step.
        stop_decay_at: `int`. Don't decay after this step.
        min_learning_rate: `float`. Don't decay below this number.
        staircase: `bool`. It `True` decay learning rate at discrete intervals.
        global_step: Scalar int `Tensor`, step counter for each update.
        use_locking: If True use locks for update operations.
        name: Optional name prefix for the operations created when applying gradients.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      optimizer: SGD
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      optimizer:
        SGD:
          learning_rate: 0.21
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      optimizer:
        SGD: {learning_rate: 0.21}
      # other model properties
    ```
    """
    IDENTIFIER = 'SGD'
    SCHEMA = SGDSchema

    def __init__(self,  # pylint: disable=useless-super-delegation
                 learning_rate=0.01,
                 decay_type="",
                 decay_rate=0.,
                 decay_steps=100,
                 start_decay_at=0,
                 stop_decay_at=1e10,
                 min_learning_rate=1e-12,
                 staircase=False,
                 global_step=None,
                 use_locking=False,
                 name='SGD'):
        super(SGDConfig, self).__init__(learning_rate, decay_type, decay_rate, decay_steps,
                                        start_decay_at, stop_decay_at, min_learning_rate,
                                        staircase, global_step, use_locking, name)


class MomentumSchema(BaseOptimizerSchema):
    momentum = fields.Float(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return MomentumConfig(**data)

    @post_dump
    def unmake(self, data):
        return MomentumConfig.remove_reduced_attrs(data)


class MomentumConfig(BaseOptimizerConfig):
    """Optimizer that implements the Momentum.

    Momentum Optimizer accepts learning rate decay. When training a model,
    it is often recommended to lower the learning rate as the training
    progresses. The function returns the decayed learning rate.  It is
    computed as:

    ```python
    >>> decayed_learning_rate = learning_rate * decay_rate ^ (global_step / lr_decay_steps)
    ```

    Args:
        learning_rate: `float`. Learning rate.
        momentum: `float`. Momentum.
        decay_type: A decay function name defined in `tf.train`
        decay_rate: `float`. The learning rate decay to apply.
        decay_steps: `int`. Apply decay every provided steps.
        start_decay_at: `int`. Don't decay before this step.
        stop_decay_at: `int`. Don't decay after this step.
        min_learning_rate: `float`. Don't decay below this number.
        staircase: `bool`. It `True` decay learning rate at discrete intervals.
        global_step: Scalar int `Tensor`, step counter for each update.
        use_locking: If True use locks for update operations.
        name: `str`. Optional name prefix for the operations created when applying gradients.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      optimizer: Momentum
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      optimizer:
        Momentum:
          learning_rate: 0.21
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      optimizer:
        Momentum: {learning_rate: 0.21}
      # other model properties
    ```
    """
    IDENTIFIER = 'Momentum'
    SCHEMA = MomentumSchema

    def __init__(self,
                 learning_rate=0.001,
                 momentum=0.9,
                 decay_type="",
                 decay_rate=0.,
                 decay_steps=10000,
                 start_decay_at=0,
                 stop_decay_at=1e10,
                 min_learning_rate=1e-12,
                 staircase=False,
                 global_step=None,
                 use_locking=False,
                 name='Momentum'):
        self.momentum = momentum
        super(MomentumConfig, self).__init__(learning_rate, decay_type, decay_rate, decay_steps,
                                             start_decay_at, stop_decay_at, min_learning_rate,
                                             staircase, global_step, use_locking, name)


class NestrovSchema(BaseOptimizerSchema):
    momentum = fields.Float(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return NestrovConfig(**data)

    @post_dump
    def unmake(self, data):
        return NestrovConfig.remove_reduced_attrs(data)


class NestrovConfig(BaseOptimizerConfig):
    """Optimizer that implements the Nesterov.

    Same as Momentum optimizer but uses nestrov
    See [Sutskever et. al., 2013](http://jmlr.org/proceedings/papers/v28/sutskever13.pdf)

    ```python
    >>> decayed_learning_rate = learning_rate * decay_rate ^ (global_step / lr_decay_steps)
    ```
    Args:
        learning_rate: `float`. Learning rate.
        momentum: `float`. Momentum.
        decay_type: A decay function name defined in `tf.train`
        decay_rate: `float`. The learning rate decay to apply.
        decay_steps: `int`. Apply decay every provided steps.
        start_decay_at: `int`. Don't decay before this step.
        stop_decay_at: `int`. Don't decay after this step.
        min_learning_rate: `float`. Don't decay below this number.
        staircase: `bool`. It `True` decay learning rate at discrete intervals.
        global_step: Scalar int `Tensor`, step counter for each update.
        use_locking: If True use locks for update operations.
        name: `str`. Optional name prefix for the operations created when applying gradients.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      optimizer: Nestrov
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      optimizer:
        Nestrov:
          learning_rate: 0.21
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      optimizer:
        Nestrov: {learning_rate: 0.21}
      # other model properties
    ```
    """
    IDENTIFIER = 'Nestrov'
    SCHEMA = NestrovSchema

    def __init__(self,
                 learning_rate=0.001,
                 momentum=0.9,
                 decay_type="",
                 decay_rate=0.,
                 decay_steps=10000,
                 start_decay_at=0,
                 stop_decay_at=1e10,
                 min_learning_rate=1e-12,
                 staircase=False,
                 use_locking=False,
                 global_step=None,
                 name='Nestrov'):
        self.momentum = momentum
        super(NestrovConfig, self).__init__(learning_rate, decay_type, decay_rate, decay_steps,
                                            start_decay_at, stop_decay_at, min_learning_rate,
                                            staircase, global_step, use_locking, name)


class RMSPropSchema(BaseOptimizerSchema):
    decay = fields.Float(allow_none=True)
    momentum = fields.Float(allow_none=True)
    epsilon = fields.Float(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return RMSPropConfig(**data)

    @post_dump
    def unmake(self, data):
        return RMSPropConfig.remove_reduced_attrs(data)


class RMSPropConfig(BaseOptimizerConfig):
    """Optimizer that implements the RMSprop.

    Maintain a moving (discounted) average of the square of gradients.
    Divide gradient by the root of this average.

    Args:
        learning_rate: `float`. learning rate.
        decay: `float`. Discounting factor for the history/coming gradient.
        momentum: `float`. Momentum.
        epsilon: `float`. Small value to avoid zero denominator.
        decay_type: A decay function name defined in `tf.train`
        decay_rate: `float`. The learning rate decay to apply.
        decay_steps: `int`. Apply decay every provided steps.
        start_decay_at: `int`. Don't decay before this step.
        stop_decay_at: `int`. Don't decay after this step.
        min_learning_rate: `float`. Don't decay below this number.
        staircase: `bool`. It `True` decay learning rate at discrete intervals.
        global_step: Scalar int `Tensor`, step counter for each update.
        use_locking: If True use locks for update operations.
        name: Optional name prefix for the operations created when applying gradients.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      optimizer: RMSProp
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      optimizer:
        RMSProp:
          learning_rate: 0.21
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      optimizer:
        RMSProp: {learning_rate: 0.21}
      # other model properties
    ```
    """
    IDENTIFIER = 'RMSProp'
    SCHEMA = RMSPropSchema

    def __init__(self,
                 learning_rate=0.001,
                 decay=0.9,
                 momentum=0.0,
                 epsilon=1e-10,
                 decay_type="",
                 decay_rate=0.,
                 decay_steps=10000,
                 start_decay_at=0,
                 stop_decay_at=1e10,
                 min_learning_rate=1e-12,
                 staircase=False,
                 global_step=None,
                 use_locking=False,
                 name='RMSProp'):
        self.decay = decay
        self.momentum = momentum
        self.epsilon = epsilon
        super(RMSPropConfig, self).__init__(learning_rate, decay_type, decay_rate, decay_steps,
                                            start_decay_at, stop_decay_at, min_learning_rate,
                                            staircase, global_step, use_locking, name)


class AdamSchema(BaseOptimizerSchema):
    beta1 = fields.Float(allow_none=True)
    beta2 = fields.Float(allow_none=True)
    epsilon = fields.Float(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return AdamConfig(**data)

    @post_dump
    def unmake(self, data):
        return AdamConfig.remove_reduced_attrs(data)


class AdamConfig(BaseOptimizerConfig):
    """Optimizer that implements the Adam.

    The default value of 1e-8 for epsilon might not be a good default in
    general. For example, when training an Inception network on ImageNet a
    current good choice is 1.0 or 0.1.

    Args:
        learning_rate: `float`. learning rate.
        beta1: `float`. The exponential decay rate for the 1st moment estimates.
        beta2: `float`. The exponential decay rate for the 2nd moment estimates.
        epsilon: `float`. A small constant for numerical stability.
        epsilon: `float`. Small value to avoid zero denominator.
        decay_type: A decay function name defined in `tf.train`
        decay_rate: `float`. The learning rate decay to apply.
        decay_steps: `int`. Apply decay every provided steps.
        start_decay_at: `int`. Don't decay before this step.
        stop_decay_at: `int`. Don't decay after this step.
        min_learning_rate: `float`. Don't decay below this number.
        staircase: `bool`. It `True` decay learning rate at discrete intervals.
        global_step: Scalar int `Tensor`, step counter for each update.
        use_locking: If True use locks for update operations.
        name: `str`. Optional name prefix for the operations created when applying gradients.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      optimizer: Adam
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      optimizer:
        Adam:
          learning_rate: 0.21
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      optimizer:
        Adam: {learning_rate: 0.21}
      # other model properties
    ```
    """
    IDENTIFIER = 'Adam'
    SCHEMA = AdamSchema

    def __init__(self,
                 learning_rate=0.001,
                 beta1=0.9,
                 beta2=0.999,
                 epsilon=1e-8,
                 decay_type="",
                 decay_rate=0.,
                 decay_steps=10000,
                 start_decay_at=0,
                 stop_decay_at=1e10,
                 min_learning_rate=1e-12,
                 staircase=False,
                 global_step=None,
                 use_locking=False,
                 name='Adam'):
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        super(AdamConfig, self).__init__(learning_rate, decay_type, decay_rate, decay_steps,
                                         start_decay_at, stop_decay_at, min_learning_rate,
                                         staircase, global_step, use_locking, name)


class AdagradSchema(BaseOptimizerSchema):
    initial_accumulator_value = fields.Float(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return AdagradConfig(**data)

    @post_dump
    def unmake(self, data):
        return AdagradConfig.remove_reduced_attrs(data)


class AdagradConfig(BaseOptimizerConfig):
    """Optimizer that implements AdaGrad.

    Args:
        learning_rate: `float`. Learning rate.
        initial_accumulator_value: `float`. Starting value for the
            accumulators, must be positive.
        decay_type: A decay function name defined in `tf.train`
        decay_rate: `float`. The learning rate decay to apply.
        decay_steps: `int`. Apply decay every provided steps.
        start_decay_at: `int`. Don't decay before this step.
        stop_decay_at: `int`. Don't decay after this step.
        min_learning_rate: `float`. Don't decay below this number.
        staircase: `bool`. It `True` decay learning rate at discrete intervals.
        global_step: Scalar int `Tensor`, step counter for each update.
        use_locking: If True use locks for update operations.
        name: `str`. Optional name prefix for the operations created when applying gradients.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      optimizer: Adagrad
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      optimizer:
        Adagrad:
          learning_rate: 0.21
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      optimizer:
        Adagrad: {learning_rate: 0.21}
      # other model properties
    ```
    """
    IDENTIFIER = 'Adagrad'
    SCHEMA = AdagradSchema

    def __init__(self,
                 learning_rate=0.01,
                 initial_accumulator_value=0.1,
                 decay_type="",
                 decay_rate=0.,
                 decay_steps=10000,
                 start_decay_at=0,
                 stop_decay_at=1e10,
                 min_learning_rate=1e-12,
                 staircase=False,
                 global_step=None,
                 use_locking=False,
                 name='Adagrad'):
        self.initial_accumulator_value = initial_accumulator_value
        super(AdagradConfig, self).__init__(learning_rate, decay_type, decay_rate, decay_steps,
                                            start_decay_at, stop_decay_at, min_learning_rate,
                                            staircase, global_step, use_locking, name)


class AdadeltaSchema(BaseOptimizerSchema):
    rho = fields.Float(allow_none=True)
    epsilon = fields.Float(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return AdadeltaConfig(**data)

    @post_dump
    def unmake(self, data):
        return AdadeltaConfig.remove_reduced_attrs(data)


class AdadeltaConfig(BaseOptimizerConfig):
    """Optimizer that implements Ftrl Proximal.

    The Ftrl-proximal algorithm, abbreviated for Follow-the-regularized-leader,
    is described in the paper below.

    It can give a good performance vs. sparsity tradeoff.

    Ftrl-proximal uses its own global base learning rate and can behave like
    Adagrad with `learning_rate_power=-0.5`, or like gradient descent with
    `learning_rate_power=0.0`.

    Args:
        learning_rate: `float`. Learning rate.
        learning_rate_power: `float`. Must be less or equal to zero.
        initial_accumulator_value: `float`. The starting value for accumulators.
            Only positive values are allowed.
        l1_regularization_strength: `float`. Must be less or equal to zero.
        l2_regularization_strength: `float`. Must be less or equal to zero.
        decay_type: A decay function name defined in `tf.train`
        decay_rate: `float`. The learning rate decay to apply.
        decay_steps: `int`. Apply decay every provided steps.
        start_decay_at: `int`. Don't decay before this step.
        stop_decay_at: `int`. Don't decay after this step.
        min_learning_rate: `float`. Don't decay below this number.
        staircase: `bool`. It `True` decay learning rate at discrete intervals.
        global_step: Scalar int `Tensor`, step counter for each update.
        use_locking: If True use locks for update operations.
        name: `str`. Optional name prefix for the operations created when applying gradients.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      optimizer: Adadelta
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      optimizer:
        Adadelta:
          learning_rate: 0.21
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      optimizer:
        Adadelta: {learning_rate: 0.21}
      # other model properties
    ```
    """
    IDENTIFIER = 'Adadelta'
    SCHEMA = AdadeltaSchema

    def __init__(self,
                 learning_rate=0.99,
                 rho=0.95,
                 epsilon=1e-08,
                 decay_type="",
                 decay_rate=0.,
                 decay_steps=10000,
                 start_decay_at=0,
                 stop_decay_at=1e10,
                 min_learning_rate=1e-12,
                 staircase=False,
                 global_step=None,
                 use_locking=False,
                 name='Adadelta'):
        self.rho = rho
        self.epsilon = epsilon
        super(AdadeltaConfig, self).__init__(learning_rate, decay_type, decay_rate, decay_steps,
                                             start_decay_at, stop_decay_at, min_learning_rate,
                                             staircase, global_step, use_locking, name)


class FtrlSchema(BaseOptimizerSchema):
    learning_rate_power = fields.Float(allow_none=True)
    initial_accumulator_value = fields.Float(allow_none=True)
    l1_regularization_strength = fields.Float(allow_none=True)
    l2_regularization_strength = fields.Float(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return FtrlConfig(**data)

    @post_dump
    def unmake(self, data):
        return FtrlConfig.remove_reduced_attrs(data)


class FtrlConfig(BaseOptimizerConfig):
    """Optimizer that implements AdaDelta.

    Args:
        learning_rate: A `Tensor` or a floating point value. The learning rate.
        rho: A `Tensor` or a floating point value. The decay rate.
        epsilon: A `Tensor` or a floating point value.  A constant epsilon used to better
            conditioning the grad update.
        decay_type: A decay function name defined in `tf.train`
        decay_rate: `float`. The learning rate decay to apply.
        decay_steps: `int`. Apply decay every provided steps.
        start_decay_at: `int`. Don't decay before this step.
        stop_decay_at: `int`. Don't decay after this step.
        min_learning_rate: `float`. Don't decay below this number.
        staircase: `bool`. It `True` decay learning rate at discrete intervals.
        global_step: Scalar int `Tensor`, step counter for each update.
        use_locking: If True use locks for update operations.
        name: Optional name prefix for the operations created when applying gradients.

    Polyaxonfile usage:

    ```yaml
    model:
      # other model properties
      optimizer: Ftrl
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      optimizer:
        Ftrl:
          learning_rate: 0.21
      # other model properties
    ```

    or

    ```yaml
    model:
      # other model properties
      optimizer:
        Ftrl: {learning_rate: 0.21}
      # other model properties
    ```
    """
    IDENTIFIER = 'Ftrl'
    SCHEMA = FtrlSchema

    def __init__(self,
                 learning_rate=3.0,
                 learning_rate_power=-0.5,
                 initial_accumulator_value=0.1,
                 l1_regularization_strength=0.0,
                 l2_regularization_strength=0.0,
                 decay_type="",
                 decay_rate=0.,
                 decay_steps=10000,
                 start_decay_at=0,
                 stop_decay_at=1e10,
                 min_learning_rate=1e-12,
                 staircase=False,
                 global_step=None,
                 use_locking=False,
                 name='Ftrl'):
        self.learning_rate_power = learning_rate_power
        self.initial_accumulator_value = initial_accumulator_value
        self.l1_regularization_strength = l1_regularization_strength
        self.l2_regularization_strength = l2_regularization_strength
        super(FtrlConfig, self).__init__(learning_rate, decay_type, decay_rate, decay_steps,
                                         start_decay_at, stop_decay_at, min_learning_rate,
                                         staircase, global_step, use_locking, name)


class OptimizerSchema(BaseMultiSchema):
    __multi_schema_name__ = 'optimizer'
    __configs__ = {
        SGDConfig.IDENTIFIER: SGDConfig,
        MomentumConfig.IDENTIFIER: MomentumConfig,
        NestrovConfig.IDENTIFIER: NestrovConfig,
        RMSPropConfig.IDENTIFIER: RMSPropConfig,
        AdamConfig.IDENTIFIER: AdamConfig,
        AdagradConfig.IDENTIFIER: AdagradConfig,
        AdadeltaConfig.IDENTIFIER: AdadeltaConfig,
        FtrlConfig.IDENTIFIER: FtrlConfig,
    }
