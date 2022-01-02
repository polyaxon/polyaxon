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

import datetime
import re
import unicodedata

from decimal import Decimal
from typing import Callable


def strip_spaces(value, sep=None, join=True):
    """Cleans trailing whitespaces and replaces also multiple whitespaces with a single space."""
    value = value.strip()
    value = [v.strip() for v in value.split(sep)]
    join_sep = sep or " "
    return join_sep.join(value) if join else value


def is_protected_type(obj):
    """
    A check for preserving a type as-is when passed to force_text(strings_only=True).
    """
    return isinstance(
        obj,
        (
            type(None),
            int,
            float,
            Decimal,
            datetime.datetime,
            datetime.date,
            datetime.time,
        ),
    )


def force_bytes(value, encoding="utf-8", strings_only=False, errors="strict"):
    """
    Resolve any value to strings.

    If `strings_only` is True, skip protected objects.
    """
    # Handle the common case first for performance reasons.
    if isinstance(value, bytes):
        if encoding == "utf-8":
            return value
        return value.decode("utf-8", errors).encode(encoding, errors)
    if strings_only and is_protected_type(value):
        return value
    if isinstance(value, memoryview):
        return bytes(value)
    return value.encode(encoding, errors)


def slugify(value: str, mark_safe: Callable = None) -> str:
    """
    Convert spaces/dots to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Also strip leading and trailing whitespace.
    """
    value = str(value)
    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub(r"[^\w\.\s-]", "", value).strip()
    value = re.sub(r"[-\.\s]+", "-", value)
    return mark_safe(value) if mark_safe else value


def validate_slug(value: str) -> bool:
    return value == slugify(value)


def to_camel_case(snake_str):
    parts = iter(snake_str.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


def to_snake_case(camel_str):
    regex1 = re.compile(r"([A-Z]+)([A-Z][a-z])")
    regex2 = re.compile(r"([a-z\d])([A-Z])")
    return regex2.sub(r"\1_\2", regex1.sub(r"\1_\2", camel_str)).lower()
