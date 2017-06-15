class Modes(object):
    """Standard names for model modes.

    The following standard keys are defined:

    * `TRAIN`: training mode.
    * `EVAL`: evaluation mode.
    * `PREDICT`: standard forward inference mode.
    * `GENERATE`: generate inference mode.
    * `ENCODE`: encode inference mode.
    """

    TRAIN = 'train'
    EVAL = 'eval'
    PREDICT = 'infer'
    GENERATE = 'generate'
    ENCODE = 'encode'

    @classmethod
    def is_train(cls, mode):
        return mode == cls.TRAIN

    @classmethod
    def is_eval(cls, mode):
        return mode == cls.EVAL

    @classmethod
    def is_infer(cls, mode):
        return mode in [cls.PREDICT, cls.GENERATE, cls.ENCODE]
