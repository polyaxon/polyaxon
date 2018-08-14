from collections import namedtuple


class UriSpec(namedtuple("UriSpec", "user password host")):
    """
    A specification for uris configuration supported by Polyaxon.
    """
    pass
