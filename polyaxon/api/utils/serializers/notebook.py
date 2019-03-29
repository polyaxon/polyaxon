class NotebookSerializerMixin(object):

    def get_tensorboard(self, obj):
        return obj.notebook.id if obj.tensorboard else None
