from typing import Any


class BaseHandler(object):

    def get(self, option: 'Option') -> Any:
        raise NotImplementedError()

    def set(self, option: 'Option', value: Any) -> None:
        raise NotImplementedError()

    def delete(self, option: 'Option') -> Any:
        raise NotImplementedError()
