class PullPolicies(object):
    ALWAYS = 'Always'
    IF_NOT_PRESENT = 'IfNotPresent'
    NEVER = 'Never'

    VALUES = {ALWAYS, IF_NOT_PRESENT, NEVER}

    CHOICES = (
        (ALWAYS, ALWAYS),
        (IF_NOT_PRESENT, IF_NOT_PRESENT),
        (NEVER, NEVER)
    )
