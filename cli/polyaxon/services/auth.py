class AuthenticationError(Exception):
    pass


class AuthenticationTypes(object):
    TOKEN = "Token"
    INTERNAL_TOKEN = "Internaltoken"
    EPHEMERAL_TOKEN = "EphemeralToken"

    VALUES = {TOKEN, INTERNAL_TOKEN, EPHEMERAL_TOKEN}
