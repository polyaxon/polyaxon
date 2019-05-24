from picklefield import PickledObjectField

import encryptor


class EncryptedPickledObjectField(PickledObjectField):
    def get_db_prep_value(self, value, *args, **kwargs):
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        value = super().get_db_prep_value(value, *args, **kwargs)
        return encryptor.encrypt(value)

    def to_python(self, value):
        if value is not None and isinstance(value, str):
            value = encryptor.decrypt(value)
        return super().to_python(value)

    def get_prep_lookup(self, lookup_type, value):
        raise NotImplementedError(
            '{} lookup type for {} is not supported'.format(lookup_type, self))
