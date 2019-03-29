class TensorboardSerializerMixin(object):

    def get_tensorboard(self, obj):
        return obj.tensorboard.id if obj.tensorboard else None
