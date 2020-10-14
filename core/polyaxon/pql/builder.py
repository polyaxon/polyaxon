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

from collections import namedtuple
from typing import Any, Callable, Optional

from polyaxon.exceptions import PolyaxonDateTimeFormatterException, PQLException
from polyaxon.utils.bool_utils import to_bool
from polyaxon.utils.date_utils import DateTimeFormatter
from polyaxon.utils.list_utils import to_list


class QueryCondSpec(namedtuple("QueryCondSpec", "cond params")):
    def items(self):
        return self._asdict().items()


class QueryBuilder:
    """The `QueryBuild` adds filters to a `QuerySet` from a `params` mapping.

    Filters are a mapping of <name: Condition>, Condition being an object that update the queryset.
    """

    def __init__(self, filters):
        self.filters = filters

    def build(self, queryset: Any, params: Any) -> Any:
        for name, condition in self.filters.items():
            if name in params:
                queryset = condition.apply(queryset, name, params[name])
        return queryset


class BaseCondition:
    """The base condition representing a single filter to apply to a `QuerySet`"""

    def apply(
        self, queryset: Any, name: str, params: Any, query_backend: Any, timezone: str
    ):
        raise NotImplementedError


class BaseOperatorCondition(BaseCondition):
    def __init__(self, op: str, negation: bool = False) -> None:
        if op not in self.VALUES and op not in self.REPRESENTATIONS:
            raise PQLException(
                "Received an invalid operator `{}`, "
                "possible values `{}` or `{}`.".format(
                    op, self.VALUES, self.REPRESENTATIONS
                )
            )

        self.operator = self._get_operator(op, negation)

    def __eq__(self, other: "BaseOperatorCondition") -> bool:
        return self.operator == other.operator

    def apply(
        self, queryset: Any, name: str, params: Any, query_backend: Any, timezone: str
    ) -> Any:
        return queryset.filter(
            self.operator(
                name=name, params=params, query_backend=query_backend, timezone=timezone
            )
        )

    def apply_operator(
        self, name: str, params: Any, query_backend: Any, timezone: str
    ) -> Any:
        return self.operator(
            name=name, params=params, query_backend=query_backend, timezone=timezone
        )


class CallbackCondition(BaseCondition):
    """The `CallbackCondition` represents a filter based on a callback to apply."""

    def __init__(self, callback: Callable) -> None:
        self.callback = callback
        self.negation = False

    def __call__(self, op, negation: bool = False) -> "CallbackCondition":
        self.negation = negation
        return self

    def apply(
        self, queryset: Any, name: str, params: Any, query_backend: Any, timezone: str
    ) -> Any:
        return self.callback(
            queryset,
            params,
            self.negation,
            query_backend=query_backend,
            timezone=timezone,
        )

    def apply_operator(
        self, name: str, params: Any, query_backend: Any, timezone: str
    ) -> Any:
        return self.callback(
            query_backend,
            params=params,
            negation=self.negation,
            query_backend=query_backend,
            timezone=timezone,
        )


class EqualityCondition(BaseOperatorCondition):
    VALUES = {"eq"}
    REPRESENTATIONS = {"="}
    REPRESENTATION_MAPPING = (("=", "eq"),)

    @classmethod
    def _get_operator(cls, op: str, negation: bool = False) -> Optional[Callable]:
        if op not in cls.VALUES and op not in cls.REPRESENTATIONS:
            return None

        if negation:
            return cls._neq_operator
        return cls._eq_operator

    @staticmethod
    def _eq_operator(name: str, params: Any, query_backend: Any, timezone: str) -> Any:
        return query_backend(**{name: params})

    @classmethod
    def _neq_operator(
        cls, name: str, params: Any, query_backend: Any, timezone: str
    ) -> any:
        return ~cls._eq_operator(name, params, query_backend, timezone)


class BoolCondition(EqualityCondition):
    @staticmethod
    def _eq_operator(name: str, params: Any, query_backend: Any, timezone: str) -> Any:
        return query_backend(**{name: to_bool(params)})


class ComparisonCondition(EqualityCondition):
    VALUES = EqualityCondition.VALUES | {"lt", "lte", "gt", "gte"}
    REPRESENTATIONS = EqualityCondition.REPRESENTATIONS | {"<", "<=", ">", ">="}
    REPRESENTATION_MAPPING = EqualityCondition.REPRESENTATION_MAPPING + (
        ("<", "lt"),
        ("<=", "lte"),
        (">", "gt"),
        (">=", "gte"),
    )

    @classmethod
    def _get_operator(cls, op: str, negation: bool = False) -> Optional[Callable]:
        if op not in cls.VALUES and op not in cls.REPRESENTATIONS:
            return None

        _op = EqualityCondition._get_operator(op, negation)
        if _op:
            return _op

        if op == "lt" or op == "<":
            if negation:
                return cls._gte_operator
            return cls._lt_operator

        if op == "lte" or op == "<=":
            if negation:
                return cls._gt_operator
            return cls._lte_operator

        if op == "gt" or op == ">":
            if negation:
                return cls._lte_operator
            return cls._gt_operator

        if op == "gte" or op == ">=":
            if negation:
                return cls._lt_operator
            return cls._gte_operator

    @staticmethod
    def _lt_operator(name: str, params: Any, query_backend: Any, timezone: str) -> Any:
        name = "{}__lt".format(name)
        return query_backend(**{name: params})

    @staticmethod
    def _gt_operator(name: str, params: Any, query_backend: Any, timezone: str) -> Any:
        name = "{}__gt".format(name)
        return query_backend(**{name: params})

    @staticmethod
    def _lte_operator(name: str, params: Any, query_backend: Any, timezone: str) -> Any:
        name = "{}__lte".format(name)
        return query_backend(**{name: params})

    @staticmethod
    def _gte_operator(name: str, params: Any, query_backend: Any, timezone: str) -> Any:
        name = "{}__gte".format(name)
        return query_backend(**{name: params})


class DateTimeCondition(ComparisonCondition):
    VALUES = ComparisonCondition.VALUES | {"range"}
    REPRESENTATIONS = ComparisonCondition.REPRESENTATIONS | {".."}
    REPRESENTATION_MAPPING = ComparisonCondition.REPRESENTATION_MAPPING + (
        ("..", "range"),
    )

    @classmethod
    def _get_operator(cls, op: str, negation: bool = False) -> Optional[Callable]:
        if op not in cls.VALUES and op not in cls.REPRESENTATIONS:
            return None

        _op = ComparisonCondition._get_operator(op, negation)
        if _op:
            return _op

        if negation:
            return cls._nrange_operator
        return cls._range_operator

    @staticmethod
    def _range_operator(
        name: str, params: Any, query_backend: Any, timezone: str
    ) -> Any:
        assert len(params) == 2
        try:
            start_date = DateTimeFormatter.extract(params[0], timezone)
            end_date = DateTimeFormatter.extract(params[1], timezone)
        except PolyaxonDateTimeFormatterException as e:
            raise PQLException(e)

        name = "{}__range".format(name)
        return query_backend(**{name: (start_date, end_date)})

    @classmethod
    def _nrange_operator(
        cls, name: str, params: Any, query_backend: Any, timezone: str
    ) -> Any:
        return ~cls._range_operator(
            name, params, query_backend=query_backend, timezone=timezone
        )


class ValueCondition(EqualityCondition):
    VALUES = EqualityCondition.VALUES | {"in"}
    REPRESENTATIONS = EqualityCondition.REPRESENTATIONS | {"|"}
    REPRESENTATION_MAPPING = EqualityCondition.REPRESENTATION_MAPPING + (("|", "in"),)

    @classmethod
    def _get_operator(cls, op: str, negation: bool = False) -> Any:
        if op not in cls.VALUES and op not in cls.REPRESENTATIONS:
            return None

        _op = EqualityCondition._get_operator(op, negation)
        if _op:
            return _op

        if negation:
            return cls._nin_operator
        return cls._in_operator

    @staticmethod
    def _in_operator(name: str, params: Any, query_backend: Any, timezone: str) -> Any:
        assert isinstance(params, (list, tuple))
        name = "{}__in".format(name)
        return query_backend(**{name: params})

    @classmethod
    def _nin_operator(
        cls, name: str, params: Any, query_backend: Any, timezone: str
    ) -> Any:
        return ~cls._in_operator(name, params, query_backend, timezone)


class SearchCondition(ValueCondition):
    VALUES = ValueCondition.VALUES | {"icontains", "istartswith", "iendswith"}
    REPRESENTATIONS = ValueCondition.REPRESENTATIONS | {"%%", "%_", "_%"}
    REPRESENTATION_MAPPING = EqualityCondition.REPRESENTATION_MAPPING + (
        ("%%", "icontains"),
        ("_%", "istartswith"),
        ("%_", "iendswith"),
    )

    @classmethod
    def _get_operator(cls, op: str, negation: bool = False) -> Any:
        if op not in cls.VALUES and op not in cls.REPRESENTATIONS:
            return None

        _op = ValueCondition._get_operator(op, negation)
        if _op:
            return _op

        if op == "%%" or op == "icontains":
            if negation:
                return cls._ncontains_operator
            return cls._contains_operator

        if op == "_%" or op == "istartswith":
            if negation:
                return cls._nstartswith_operator
            return cls._startswith_operator

        if op == "%_" or op == "iendswith":
            if negation:
                return cls._nendswith_operator
            return cls._endswith_operator

    @staticmethod
    def _contains_operator(
        name: str, params: str, query_backend: Any, timezone: str
    ) -> Any:
        assert isinstance(params, str)
        name = "{}__icontains".format(name)
        return query_backend(**{name: params})

    @classmethod
    def _ncontains_operator(
        cls, name: str, params: str, query_backend: Any, timezone: str
    ) -> Any:
        return ~cls._contains_operator(name, params, query_backend, timezone)

    @staticmethod
    def _startswith_operator(
        name: str, params: str, query_backend: Any, timezone: str
    ) -> Any:
        assert isinstance(params, str)
        name = "{}__istartswith".format(name)
        return query_backend(**{name: params})

    @classmethod
    def _nstartswith_operator(
        cls, name: str, params: str, query_backend: Any, timezone: str
    ) -> Any:
        return ~cls._startswith_operator(
            name, params, query_backend=query_backend, timezone=timezone
        )

    @staticmethod
    def _endswith_operator(
        name: str, params: str, query_backend: Any, timezone: str
    ) -> Any:
        assert isinstance(params, str)
        name = "{}__iendswith".format(name)
        return query_backend(**{name: params})

    @classmethod
    def _nendswith_operator(
        cls, name: str, params: str, query_backend: Any, timezone: str
    ) -> Any:
        return ~cls._endswith_operator(name, params, query_backend, timezone)


class ArrayCondition(EqualityCondition):
    VALUES = EqualityCondition.VALUES | {"in"}
    REPRESENTATIONS = EqualityCondition.REPRESENTATIONS | {"|"}
    REPRESENTATION_MAPPING = EqualityCondition.REPRESENTATION_MAPPING + (("|", "in"),)

    @classmethod
    def _get_operator(cls, op: str, negation: bool = False) -> Optional[Callable]:
        if op not in cls.VALUES and op not in cls.REPRESENTATIONS:
            return None

        _op = cls._get_eq_operator(op, negation)
        if _op:
            return _op

        if negation:
            return cls._nin_operator
        return cls._in_operator

    @classmethod
    def _get_eq_operator(cls, op: str, negation: bool = False) -> Optional[Callable]:
        if (
            op not in EqualityCondition.VALUES
            and op not in EqualityCondition.REPRESENTATIONS
        ):
            return None

        if negation:
            return cls._neq_operator
        return cls._eq_operator

    @staticmethod
    def _eq_operator(name: str, params: Any, query_backend: Any, timezone: str) -> Any:
        name = "{}__contains".format(name)
        return query_backend(**{name: to_list(params)})

    @staticmethod
    def _in_operator(name: str, params: Any, query_backend: Any, timezone: str) -> Any:
        assert isinstance(params, (list, tuple))
        name = "{}__overlap".format(name)
        return query_backend(**{name: params})

    @classmethod
    def _nin_operator(
        cls, name: str, params: Any, query_backend: Any, timezone: str
    ) -> Any:
        return ~cls._in_operator(name, params, query_backend, timezone)
