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

import sys

from contextlib import contextmanager

from polyaxon.utils.constants import NEWLINES

INDENT_CHAR = " "
INDENT_STRINGS = []
STDOUT = sys.stdout.write
STDERR = sys.stderr.write


def _indent(depth=0, quote=""):
    """Indent util function, compute new indent_string"""
    if depth > 0:
        indent_string = "".join((str(quote), (INDENT_CHAR * (depth - len(quote)))))
    else:
        indent_string = "".join((("\x08" * (-1 * (depth - len(quote)))), str(quote)))

    if indent_string:
        INDENT_STRINGS.append(indent_string)


@contextmanager
def _indent_context():
    """Indentation context manager."""
    try:
        yield
    finally:
        # Remove indent
        INDENT_STRINGS.pop()


def indent(depth=4, quote=""):
    """Indentation manager, return an indentation context manager."""
    _indent(depth, quote)
    return _indent_context()


def split_many(string, delimiters):
    """Behaves str.split but supports tuples of delimiters."""
    delimiters = tuple(delimiters)
    if len(delimiters) < 1:
        return [string]
    final_delimiter = delimiters[0]
    for i in delimiters[1:]:
        string = string.replace(i, final_delimiter)
    return string.split(final_delimiter)


def puts(s="", newline=True, stream=STDOUT):
    """Prints given string to stdout."""
    if newline:
        s = split_many(s, NEWLINES)
        s = map(str, s)
        indentation = "".join(INDENT_STRINGS)

        s = (str("\n" + indentation)).join(s)

    outputs = "".join(("".join(INDENT_STRINGS), str(s), "\n" if newline else ""))
    stream(outputs)
