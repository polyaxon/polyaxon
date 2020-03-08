from enum import Enum
from typing import Iterable, List, Set, Tuple, Type, Union


def enum_to_choices(enumeration: Type[Enum]) -> Iterable[Tuple]:
    return tuple((e.value, e.value) for e in enumeration)


def enum_to_set(enumeration: Type[Enum]) -> Set:
    return set(e.value for e in enumeration)


def values_to_choices(enumeration: Union[List, Set]) -> Iterable[Tuple]:
    return tuple((e, e) for e in enumeration)
