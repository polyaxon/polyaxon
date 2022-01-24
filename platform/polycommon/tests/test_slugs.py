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

from unittest import TestCase

from django.utils.functional import lazy

from polycommon.validation.slugs import slugify


class TestSlugify(TestCase):
    def test_slugify(self):
        self.assertEqual(
            slugify(
                " Jack & Jill like numbers 1,2,3 and 4 and silly characters ?%.$!/"
            ),
            "Jack-Jill-like-numbers-123-and-4-and-silly-characters-",
        )

    def test_unicode(self):
        self.assertEqual(
            slugify("Un \xe9l\xe9phant \xe0 l'or\xe9e du bois"),
            "Un-elephant-a-loree-du-bois",
        )

    def test_non_string_input(self):
        self.assertEqual(slugify(123), "123")

    def test_slugify_lazy_string(self):
        lazy_str = lazy(lambda string: string, str)
        self.assertEqual(
            slugify(
                lazy_str(
                    " Jack & Jill like numbers 1,2,3 and 4 and silly characters ?%.$!/"
                )
            ),
            "Jack-Jill-like-numbers-123-and-4-and-silly-characters-",
        )
