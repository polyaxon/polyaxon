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

from typing import Any, Dict, Iterable

from polyaxon.exceptions import PQLException
from polyaxon.pql.builder import QueryCondSpec
from polyaxon.pql.parser import parse_field, tokenize_query


class PQLManager(object):
    NAME = None
    FIELDS_USE_UUID = None
    FIELDS_PROXY = {}
    FIELDS_TRANS = {}
    FIELDS_ORDERING = None
    FIELDS_ORDERING_PROXY = None
    FIELDS_DEFAULT_ORDERING = None
    CHECK_ALIVE = True
    PARSERS_BY_FIELD = {}
    CONDITIONS_BY_FIELD = {}
    QUERY_BACKEND = None
    TIMEZONE = None

    @classmethod
    def proxy_field(cls, field: str) -> str:
        field, suffix = parse_field(field)
        if field in cls.FIELDS_PROXY:
            field = cls.FIELDS_PROXY[field]
        if cls.FIELDS_USE_UUID and not suffix and field in cls.FIELDS_USE_UUID:
            suffix = "uuid"
        return "{}__{}".format(field, suffix) if suffix else field

    @classmethod
    def trans_field(
        cls,
        key: str,
        tokenized_query: Dict[str, Iterable],
        update_tokenized_query: Dict[str, Iterable],
    ) -> None:
        field, suffix = parse_field(key)
        if field in cls.FIELDS_TRANS:
            field_trans = cls.FIELDS_TRANS[field]["field"]
            update_tokenized_query["{}_value".format(field_trans)] = tokenized_query[
                key
            ]
            update_tokenized_query["{}_name".format(field_trans)] = [suffix]
            if cls.FIELDS_TRANS[field].get("type"):
                update_tokenized_query[
                    "{}_type".format(field_trans)
                ] = cls.FIELDS_TRANS[field]["type"]
        else:
            update_tokenized_query[key] = tokenized_query[key]

    @classmethod
    def tokenize(cls, query_spec: str) -> Dict[str, Iterable]:
        tokenized_query = tokenize_query(query_spec)
        results = {}
        for key in tokenized_query.keys():
            field, _ = parse_field(key)
            if field and (
                field not in cls.PARSERS_BY_FIELD
                or field not in cls.CONDITIONS_BY_FIELD
            ):
                raise PQLException(
                    "key `{}` is not supported by query manager `{}`.".format(
                        key, cls.NAME
                    )
                )
            cls.trans_field(key, tokenized_query, results)
        return results

    @classmethod
    def parse(cls, tokenized_query: Dict[str, Iterable]) -> Dict[str, Iterable]:
        parsed_query = {}
        for key, expressions in tokenized_query.items():
            field, _ = parse_field(key)
            parsed_query[key] = [
                cls.PARSERS_BY_FIELD[field](exp) for exp in expressions
            ]
        return parsed_query

    @classmethod
    def build(cls, parsed_query: Dict[str, Iterable]) -> Dict[str, Iterable]:
        built_query = {}
        for key, operations in parsed_query.items():
            field, _ = parse_field(key)
            built_query[key] = [
                QueryCondSpec(
                    cond=cls.CONDITIONS_BY_FIELD[field](
                        op=op_spec.op, negation=op_spec.negation
                    ),
                    params=op_spec.params,
                )
                for op_spec in operations
            ]
        return built_query

    @classmethod
    def handle_query(cls, query_spec: str) -> Dict[str, Iterable]:
        tokenized_query = cls.tokenize(query_spec=query_spec)
        parsed_query = cls.parse(tokenized_query=tokenized_query)
        built_query = cls.build(parsed_query=parsed_query)
        return built_query

    @classmethod
    def apply(cls, query_spec: str, queryset: Any) -> Any:
        built_query = cls.handle_query(query_spec=query_spec)
        operators = []
        for key, cond_specs in built_query.items():
            key = cls.proxy_field(key)
            for cond_spec in cond_specs:
                operators.append(
                    cond_spec.cond.apply_operator(
                        name=key,
                        params=cond_spec.params,
                        query_backend=cls.QUERY_BACKEND,
                        timezone=cls.TIMEZONE,
                    )
                )

        return queryset.filter(*operators)
