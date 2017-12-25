class IgnoreRawDecorator(object):
    """The `IgnoreRawDecorator` is a decorator to ignore raw/fixture data during signals handling.

    usage example:
        @receiver(post_save, sender=settings.AUTH_USER_MODEL)
        @ignore_raw
        def my_signal_handler(sender, instance=None, created=False, **kwargs):
            ...
            return ...
    """

    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        if kwargs.get('raw'):
            # Ignore signal handling for fixture loading
            return

        return self.f(*args, **kwargs)


ignore_raw = IgnoreRawDecorator
