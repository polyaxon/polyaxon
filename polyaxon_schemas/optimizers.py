# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load

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
    def make_load(self, data):
        return SGDConfig(**data)


class SGDConfig(BaseOptimizerConfig):
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
    def make_load(self, data):
        return MomentumConfig(**data)


class MomentumConfig(BaseOptimizerConfig):
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
    def make_load(self, data):
        return NestrovConfig(**data)


class NestrovConfig(BaseOptimizerConfig):
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
    def make_load(self, data):
        return RMSPropConfig(**data)


class RMSPropConfig(BaseOptimizerConfig):
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
    def make_load(self, data):
        return AdamConfig(**data)


class AdamConfig(BaseOptimizerConfig):
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
    def make_load(self, data):
        return AdagradConfig(**data)


class AdagradConfig(BaseOptimizerConfig):
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
    def make_load(self, data):
        return AdadeltaConfig(**data)


class AdadeltaConfig(BaseOptimizerConfig):
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
    def make_load(self, data):
        return FtrlConfig(**data)


class FtrlConfig(BaseOptimizerConfig):
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
