from typing import Tuple

from hestia.manager_interface import ManagerInterface


class OptionManager(ManagerInterface):

    def _get_state_data(self,  # pylint:disable=arguments-differ
                        option: 'Option') -> Tuple[str, 'Option']:
        return option.key, option

    def subscribe(self, option: 'Option') -> None:  # pylint:disable=arguments-differ
        """
        >>> subscribe(SomeOption)
        """
        super().subscribe(obj=option)

    def get(self, key: str) -> 'option':  # pylint:disable=arguments-differ
        return super().get(key=key)
