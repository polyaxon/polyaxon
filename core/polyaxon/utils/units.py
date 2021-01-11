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


def to_unit_memory(number):
    """Creates a string representation of memory size given `number`."""
    kb = 1024

    number /= kb

    if number < 100:
        return "{} Kb".format(round(number, 2))

    number /= kb
    if number < 300:
        return "{} Mb".format(round(number, 2))

    number /= kb

    return "{} Gb".format(round(number, 2))


def to_percentage(number, rounding=2):
    """Creates a percentage string representation from the given `number`. The
    number is multiplied by 100 before adding a '%' character.

    Raises `ValueError` if `number` cannot be converted to a number.
    """
    number = float(number) * 100
    number_as_int = int(number)
    rounded = round(number, rounding)

    return "{}%".format(number_as_int if number_as_int == rounded else rounded)


def format_sizeof(num, suffix="B"):
    """
    Print in human friendly format
    """
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)
