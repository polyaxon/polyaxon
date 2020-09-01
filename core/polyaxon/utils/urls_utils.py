#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
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

try:
    from urllib.parse import urlparse  # pylint:disable=import-error
except ImportError:
    raise ImportError("This module depends on django.")


def validate_url(url):
    if not url.startswith(("http://", "https://")):
        return False
    parsed = urlparse(url)
    if not parsed.hostname:
        return False
    return True


URL_FORMAT = "{protocol}://{domain}{path}"
