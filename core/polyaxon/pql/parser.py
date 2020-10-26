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

from collections import defaultdict, namedtuple
from typing import Dict, Iterable, List, Optional, Tuple

from polyaxon.exceptions import PQLException


class QueryOpSpec(namedtuple("QueryOpSpec", "op negation params")):
    def items(self):
        return self._asdict().items()


def parse_negation_operation(operation: str) -> Tuple[bool, str]:
    """Parse the negation modifier in an operation."""
    _operation = operation.strip()
    if not _operation:
        raise PQLException("Operation is not valid: {}".format(operation))
    negation = False
    if _operation[0] == "~":
        negation = True
        _operation = _operation[1:]

    return negation, _operation.strip()


def parse_nil_operation(operation: str) -> Optional["QueryOpSpec"]:
    """Parse the nil operator in an operation."""
    _operation = operation.strip()
    if not _operation:
        raise PQLException("Operation is not valid: {}".format(operation))

    # Check negation
    negation, _operation = parse_negation_operation(_operation)

    # Check nil
    if _operation == "nil":
        return QueryOpSpec("nil", negation, None)

    return None


def parse_comparison_operation(operation: str) -> Tuple[Optional[str], str]:
    """Parse the comparison operator in an operation."""
    _operation = operation.strip()
    if not _operation:
        raise PQLException("Operation is not valid: {}".format(operation))
    # Check inclusion comparison
    if _operation[:2] in ("<=", "=<"):
        return "<=", _operation[2:].strip()

    if _operation[:2] in (">=", "=>"):
        return ">=", _operation[2:].strip()

    # Non inclusive
    if _operation[:1] in (">", "<"):
        return _operation[:1], _operation[1:].strip()

    return None, _operation


def parse_datetime_operation(operation: str) -> "QueryOpSpec":
    """Parse datetime operations.

    A datetime operation can be one of the following:

     * single value: start_date:2014-10-10, start_date:>2014-10-10, start_date:>=2014-10-10
     * negation single value: start_date:~2014-10-10
     * interval: start_date:2010-10-10 10:10 .. 2012-10-10
     * negation interval: start_date:~2010-10-10 10:10 .. 2012-10-10

    This parser does not allow `|`
    """
    _operation = operation.strip()
    if not _operation:
        raise PQLException("Operation is not valid: {}".format(operation))
    # Check not allowed ops
    if "|" in _operation:
        raise PQLException(
            "`|` is not allowed for datetime operations. "
            "Operation: {}".format(operation)
        )

    # Check nil operation
    spec = parse_nil_operation(_operation)
    if spec:
        return spec

    # Check negation
    negation, _operation = parse_negation_operation(_operation)

    # Check range operator
    if ".." in _operation:
        op = ".."
        params = _operation.split("..")
        params = [param.strip() for param in params if param]
        if len(params) != 2:
            raise PQLException(
                "Expression is not valid, ranges requires only 2 params, "
                "Operation: {}".format(operation)
            )
        return QueryOpSpec(op, negation, params)

    # Check comparison operators
    op, _operation = parse_comparison_operation(_operation)
    if not op:
        # Now the operation must be an equality param param
        op = "="

    if not _operation:
        raise PQLException(
            "Expression is not valid, it must be formatted as "
            "name:operation, "
            "Operation: {}".format(operation)
        )
    return QueryOpSpec(op, negation, _operation)


def parse_scalar_operation(operation: str) -> "QueryOpSpec":
    """Parse scalar operations.

    A scalar operation can be one of the following:

     * single value: start_date:12, metric1:>0.9, metric1:>=-0.12
     * negation single value: metric1:~1112, metric1:~<1112 equivalent to metric1:>=1112

    This parser does not allow `|` and `..`.
    """
    _operation = operation.strip()
    if not _operation:
        raise PQLException("Operation is not valid: {}".format(operation))
    # Check not allowed ops
    if "|" in _operation:
        raise PQLException(
            "`|` is not allowed for scalar operations. "
            "Operation: {}".format(operation)
        )
    if ".." in _operation:
        raise PQLException(
            "`..` is not allowed for scalar operations. "
            "Operation: {}".format(operation)
        )

    # Check nil operation
    spec = parse_nil_operation(_operation)
    if spec:
        return spec

    # Check negation
    negation, _operation = parse_negation_operation(_operation)

    # Check comparison operators
    op, _operation = parse_comparison_operation(_operation)
    if not op:
        # Now the operation must be an equality param
        op = "="

    # Check that params are scalar (int, float)
    try:
        _operation = int(_operation)
    except (ValueError, TypeError):
        try:
            _operation = float(_operation)
        except (ValueError, TypeError):
            raise PQLException(
                "Scalar operation requires int or float params, "
                "received {}.".format(operation)
            )
    return QueryOpSpec(op, negation, _operation)


def parse_value_operation(operation: str) -> "QueryOpSpec":
    """Parse value operations.

    A value operation can be one of the following:

     * single value: tag1:foo
     * negation single value: tag1:~foo
     * multiple values: tag1:foo|bar|moo
     * negation multiple values: tag1:~foo|bar|moo

    This parser does not allow `..`, '>', '<', '>=', and '<='.
    """
    _operation = operation.strip()
    if not _operation:
        raise PQLException("Operation is not valid: {}".format(operation))
    # Check range not allowed
    if ".." in _operation:
        raise PQLException(
            "`..` is not allowed for value operations. "
            "Operation: {}".format(operation)
        )

    # Check nil operation
    spec = parse_nil_operation(_operation)
    if spec:
        return spec

    # Check negation
    negation, _operation = parse_negation_operation(_operation)

    # Check comparison not allowed
    op, _operation = parse_comparison_operation(_operation)
    if op:
        raise PQLException(
            "`{}` is not allowed for value operations, "
            "Operation: {}".format(op, operation)
        )

    # Check in operator
    if "|" in _operation:
        op = "|"
        params = _operation.split("|")
        params = [param.strip() for param in params if param.strip()]
        if len(params) <= 1:
            raise PQLException(
                "`{}` is not allowed for value operations, "
                "Operation: {}".format(op, operation)
            )
        return QueryOpSpec(op, negation, params)

    if not _operation:
        raise PQLException(
            "Expression is not valid, it must be formatted as "
            "name:operation, "
            "Operation: {}".format(operation)
        )
    # Now the operation must be an equality param param
    return QueryOpSpec("=", negation, _operation)


def parse_search_operation(operation: str) -> "QueryOpSpec":
    """Parse search operations.

    A search operation can be one of the following:

     * single value: tag1:foo
     * negation single value: tag1:~foo
     * multiple values: tag1:foo|bar|moo
     * negation multiple values: tag1:~foo|bar|moo
     * like value: name:%foo or name:foo% or name:%foo%
     * not like value: name:~%foo or name:~foo% or name:~%foo%

    This parser does not allow `..`, '>', '<', '>=', and '<='.
    """
    _operation = operation.strip()
    if not _operation:
        raise PQLException("Operation is not valid: {}".format(operation))
    # Check range not allowed
    if ".." in _operation:
        raise PQLException(
            "`..` is not allowed for value operations. "
            "Operation: {}".format(operation)
        )

    # Check nil operation
    spec = parse_nil_operation(_operation)
    if spec:
        return spec

    # Check negation
    negation, _operation = parse_negation_operation(_operation)

    # Check comparison not allowed
    op, _operation = parse_comparison_operation(_operation)
    if op:
        raise PQLException(
            "`{}` is not allowed for value operations, "
            "Operation: {}".format(op, operation)
        )

    # Check in operator
    if "|" in _operation:
        op = "|"
        params = _operation.split("|")
        params = [param.strip() for param in params if param.strip()]
        if len(params) <= 1:
            raise PQLException(
                "`{}` is not allowed for value operations, "
                "Operation: {}".format(op, operation)
            )
        return QueryOpSpec(op, negation, params)

    # Check like operator
    start_like = _operation.endswith("%")
    end_like = _operation.startswith("%")
    if start_like and end_like:
        op = "%%"
        params = _operation.split("%")
        params = [param.strip() for param in params if param.strip()]
        if len(params) != 1:
            raise PQLException(
                "`{}` is not allowed for value operations, "
                "Operation: {}".format(op, operation)
            )
        return QueryOpSpec(op, negation, params[0])

    if start_like:
        op = "_%"
        params = _operation.split("%")
        params = [param.strip() for param in params if param.strip()]
        if len(params) != 1:
            raise PQLException(
                "`{}` is not allowed for value operations, "
                "Operation: {}".format(op, operation)
            )
        return QueryOpSpec(op, negation, params[0])

    if end_like:
        op = "%_"
        params = _operation.split("%")
        params = [param.strip() for param in params if param.strip()]
        if len(params) != 1:
            raise PQLException(
                "`{}` is not allowed for value operations, "
                "Operation: {}".format(op, operation)
            )
        return QueryOpSpec(op, negation, params[0])

    if not _operation:
        raise PQLException(
            "Expression is not valid, it must be formatted as "
            "name:operation, "
            "Operation: {}".format(operation)
        )
    # Now the operation must be an equality param param
    return QueryOpSpec("=", negation, _operation)


def parse_expression(expression: str) -> Tuple[str, str]:
    """Base parsing for expressions.

    Every expression must follow a basic format:
        `name:[modifier|operator]operation[*[operator]operation]`

    So this parser just split the expression into: field name, operation.
    """
    try:
        _expression = expression.strip()
        name, operation = _expression.split(":")
        name = name.strip()
        operation = operation.strip()
        if not name or not operation:
            raise ValueError
    except (ValueError, AttributeError):
        raise PQLException(
            "Expression is not valid, it must be formatted as "
            "name:operation, "
            "Expression: {}".format(expression)
        )
    return name, operation


def split_query(query: str) -> List[str]:
    """Split a query into different expressions.

    Example:
        name:bla, foo:<=1
    """
    try:
        _query = query.strip()
    except (ValueError, AttributeError):
        raise PQLException("query is not valid, received instead {}".format(query))

    expressions = _query.split(",")
    expressions = [exp.strip() for exp in expressions if exp.strip()]
    if not expressions:
        raise PQLException("Query is not valid: {}".format(query))

    return expressions


def tokenize_query(query: str) -> Dict[str, Iterable]:
    """Tokenizes a standard search query in name: operations mapping.

    Example:
        moo:bla, foo:~<=1, foo:ll..ff

        {
          'moo': ['bla'],
          'foo': ['~<=1', 'll..ff']
        }
    """
    expressions = split_query(query)
    name_operation_tuples = [parse_expression(expression) for expression in expressions]
    operation_by_name = defaultdict(list)
    for name, operation in name_operation_tuples:
        operation_by_name[name].append(operation)
    return operation_by_name


def parse_field(field: str) -> Tuple[str, Optional[str]]:
    """Parses fields with underscores, and return field and suffix.

    Example:
        foo => foo, None
        metrics.foo => metric, foo
    """
    _field = field.split(".")
    _field = [f.strip() for f in _field]
    if len(_field) == 1 and _field[0]:
        return _field[0], None
    elif len(_field) == 2 and _field[0] and _field[1]:
        return _field[0], _field[1]
    raise PQLException(
        "Query field must be either a single value,"
        "possibly with single underscores, "
        "or a prefix double underscore field. "
        "Received `{}`".format(field)
    )
