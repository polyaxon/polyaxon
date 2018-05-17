from django.utils.crypto import salted_hmac


def get_hmac(key_salt, value):
    return salted_hmac(key_salt, value).hexdigest()
