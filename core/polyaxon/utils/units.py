#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Union


def to_cpu_value(cpu_definition: Union[str, int, float]) -> float:
    try:
        return float(cpu_definition)
    except (ValueError, TypeError):
        pass

    cpu_definition = cpu_definition.lower()
    cpu_unit = cpu_definition[-1]
    cpu_value = cpu_definition[:-1]
    if cpu_unit == "m":
        cpu = int(cpu_value) / 1000
    elif cpu_unit == "u":
        cpu = int(cpu_value) / 1000 ** 2
    elif cpu_unit == "n":
        cpu = int(cpu_value) / 1000 ** 3
    else:
        cpu = cpu_definition
    return float(cpu)


def to_memory_bytes(mem_definition: Union[str, int, float]) -> int:
    try:
        return int(float(mem_definition))
    except (ValueError, TypeError):
        pass

    def _get_value(unit, value, multiplier):
        if unit in multiplier.keys():
            return int(value) * multiplier.get(unit, 1)

    fixed_point_unit_multiplier = {
        "k": 1000,
        "m": 1000 ** 2,
        "g": 1000 ** 3,
        "t": 1000 ** 4,
        "p": 1000 ** 5,
        "e": 1000 ** 6,
    }

    power_two_unit_multiplier = {
        "ki": 1024,
        "mi": 1024 ** 2,
        "gi": 1024 ** 3,
        "ti": 1024 ** 4,
        "pi": 1024 ** 5,
        "ei": 1024 ** 6,
    }

    mem_definition = mem_definition.lower()

    mem_unit = mem_definition[-2:]
    mem_value = mem_definition[:-2]
    memory = _get_value(mem_unit, mem_value, power_two_unit_multiplier)
    if memory is not None:
        return memory

    mem_unit = mem_definition[-1:]
    mem_value = mem_definition[:-1]
    memory = _get_value(mem_unit, mem_value, fixed_point_unit_multiplier)
    if memory is not None:
        return memory

    return 0


def to_unit_memory(number, precision: int = 2):
    """Creates a string representation of memory size given `number`."""
    kb = 1024

    number /= kb

    if number < 100:
        return "{} Ki".format(round(number, precision))

    number /= kb
    if number < 300:
        return "{} Mi".format(round(number, precision))

    number /= kb
    if number < 900:
        return "{} Gi".format(round(number, precision))

    number /= kb
    if number < 900:
        return "{} Ti".format(round(number, precision))

    number /= kb
    if number < 900:
        return "{} Pi".format(round(number, precision))

    number /= kb
    return "{} Ei".format(round(number, precision))


def number_percentage_format(x, precision: int = None, use_comma: bool = False):
    if precision is None:
        return x
    eps = 0.000000001
    comma = "," if use_comma else ""
    num_format = (
        "{{0:{}.0f}}".format(comma)
        if abs(int(x) - x) < eps
        else "{{0:{}.{}f}}".format(comma, precision)
    )
    return num_format.format(x)


def to_percentage(
    number, rounding: int = 2, precision: int = None, use_comma: bool = False
):
    """Creates a percentage string representation from the given `number`. The
    number is multiplied by 100 before adding a '%' character.

    Raises `ValueError` if `number` cannot be converted to a number.
    """
    number = float(number) * 100
    number_as_int = int(number)
    rounded = round(number, rounding)
    value = (
        number_as_int
        if number_as_int == rounded
        else number_percentage_format(rounded, precision, use_comma)
    )

    return "{}%".format(value)


def format_sizeof(num, suffix="B"):
    """
    Print in human friendly format
    """
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)
