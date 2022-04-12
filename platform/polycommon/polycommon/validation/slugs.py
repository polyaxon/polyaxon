#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
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

from django.core.validators import RegexValidator
from django.utils.regex_helper import _lazy_re_compile

try:
    from django.utils.safestring import mark_safe
except ImportError:
    raise ImportError("This module depends on django.")


from polyaxon.utils.string_utils import slugify as core_slugify


def slugify(value: str) -> str:
    return core_slugify(value, mark_safe)


slug_dots_re = _lazy_re_compile(r"^[-a-zA-Z0-9_.]+\Z")
validate_slug_with_dots = RegexValidator(
    slug_dots_re,
    # Translators: "letters" means latin letters: a-z and A-Z.
    "Enter a valid “value” consisting of letters, numbers, underscores, hyphens, or dots.",
    "invalid",
)
