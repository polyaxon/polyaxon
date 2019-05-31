from collections import namedtuple


class RegistryContextSpec(namedtuple("RegistryContextSpec", "host secret secret_keys insecure")):

    def items(self):
        return self._asdict().items()
