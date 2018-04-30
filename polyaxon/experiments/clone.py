class CloningStrategy(object):
    COPY = 'copy'
    RESTART = 'restart'
    RESUME = 'resume'

    VALUES = {COPY, RESTART, RESUME}

    CHOICES = (
        (COPY, COPY),
        (RESTART, RESTART),
        (RESUME, RESUME)
    )
