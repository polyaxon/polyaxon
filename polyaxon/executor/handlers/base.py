class BaseHandler(object):
    SUBJECT = None

    @classmethod
    def record_event(cls, event: 'Event') -> None:
        pass
