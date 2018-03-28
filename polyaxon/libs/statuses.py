class BaseStatuses(object):
    VALUES = []
    CHOICES = ()
    STARTING_STATUS = []
    DONE_STATUS = []
    RUNNING_STATUS = []
    FAILED_STATUS = []
    TRANSITION_MATRIX = {}

    @classmethod
    def can_transition(cls, status_from, status_to):
        if status_to not in cls.TRANSITION_MATRIX:
            return False

        return status_from in cls.TRANSITION_MATRIX[status_to]

    @classmethod
    def is_starting(cls, status):
        return status in cls.STARTING_STATUS

    @classmethod
    def is_running(cls, status):
        return status in cls.RUNNING_STATUS

    @classmethod
    def is_done(cls, status):
        return status in cls.DONE_STATUS

    @classmethod
    def failed(cls, status):
        return status in cls.FAILED_STATUS

    @classmethod
    def succeeded(cls, status):
        return status == cls.SUCCEEDED

    @classmethod
    def stopped(cls, status):
        return status == cls.STOPPED

    @classmethod
    def skipped(cls, status):
        return status == cls.SKIPPED
