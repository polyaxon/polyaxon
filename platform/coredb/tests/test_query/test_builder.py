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

import datetime

import pytest

from django.conf import settings
from django.db.models import Q

from coredb.factories.runs import RunFactory
from coredb.managers.statuses import new_run_status
from coredb.models.runs import Run
from polyaxon.exceptions import PQLException
from polyaxon.lifecycle import V1StatusCondition, V1Statuses
from polyaxon.pql.builder import (
    BoolCondition,
    ComparisonCondition,
    DateTimeCondition,
    EqualityCondition,
    SearchCondition,
    ValueCondition,
)
from polyaxon.utils.date_utils import DateTimeFormatter
from tests.test_query.base import BaseTestQuery

# pylint:disable=protected-access


class TestEqualityCondition(BaseTestQuery):
    def test_equality_operators(self):
        op = EqualityCondition._eq_operator(
            "field", "value", query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == Q(field="value")
        op = EqualityCondition._neq_operator(
            "field", "value", query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == ~Q(field="value")

    def test_equality_condition_init_with_correct_operator(self):
        eq_cond = EqualityCondition(op="eq")
        assert eq_cond.operator == EqualityCondition._eq_operator
        neq_cond = EqualityCondition(op="eq", negation=True)
        assert neq_cond.operator == EqualityCondition._neq_operator

    def test_equality_apply(self):
        eq_cond = EqualityCondition(op="eq")
        neq_cond = EqualityCondition(op="eq", negation=True)

        new_run_status(
            run=self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.SCHEDULED, status=True
            ),
        )

        # eq
        queryset = eq_cond.apply(
            queryset=Run.objects,
            name="status",
            params=V1Statuses.SCHEDULED,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = eq_cond.apply(
            queryset=Run.objects,
            name="status",
            params=V1Statuses.SUCCEEDED,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        # neq
        queryset = neq_cond.apply(
            queryset=Run.objects,
            name="status",
            params=V1Statuses.SCHEDULED,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        queryset = neq_cond.apply(
            queryset=Run.objects,
            name="status",
            params=V1Statuses.SUCCEEDED,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1


class TestBoolCondition(BaseTestQuery):
    def test_bool_operators(self):
        op = BoolCondition._eq_operator(
            "field", "false", query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == Q(field=False)
        op = BoolCondition._eq_operator(
            "field", 0, query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == Q(field=False)
        op = BoolCondition._eq_operator(
            "field", False, query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == Q(field=False)
        op = BoolCondition._neq_operator(
            "field", "true", query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == ~Q(field=True)
        op = BoolCondition._neq_operator(
            "field", 1, query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == ~Q(field=True)
        op = BoolCondition._neq_operator(
            "field", True, query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == ~Q(field=True)

    def test_bool_condition_init_with_correct_operator(self):
        eq_cond = BoolCondition(op="eq")
        assert eq_cond.operator == BoolCondition._eq_operator
        neq_cond = BoolCondition(op="eq", negation=True)
        assert neq_cond.operator == BoolCondition._neq_operator

    def test_bool_apply(self):
        eq_cond = BoolCondition(op="eq")
        neq_cond = BoolCondition(op="eq", negation=True)

        # eq
        queryset = eq_cond.apply(
            queryset=Run.objects,
            name="deleted",
            params=0,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1
        queryset = eq_cond.apply(
            queryset=Run.objects,
            name="deleted",
            params="false",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1
        queryset = eq_cond.apply(
            queryset=Run.objects,
            name="deleted",
            params=False,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = eq_cond.apply(
            queryset=Run.objects,
            name="deleted",
            params=1,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0
        queryset = eq_cond.apply(
            queryset=Run.objects,
            name="deleted",
            params="true",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0
        queryset = eq_cond.apply(
            queryset=Run.objects,
            name="deleted",
            params=True,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        # neq
        queryset = neq_cond.apply(
            queryset=Run.objects,
            name="deleted",
            params=0,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0
        queryset = neq_cond.apply(
            queryset=Run.objects,
            name="deleted",
            params="false",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0
        queryset = neq_cond.apply(
            queryset=Run.objects,
            name="deleted",
            params=False,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        queryset = neq_cond.apply(
            queryset=Run.objects,
            name="deleted",
            params=1,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1
        queryset = neq_cond.apply(
            queryset=Run.objects,
            name="deleted",
            params="true",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1
        queryset = neq_cond.apply(
            queryset=Run.objects,
            name="deleted",
            params=True,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

    # class TestComparisonCondition(BaseTestQuery):
    #     def test_comparison_operators(self):
    #         op = ComparisonCondition._lt_operator("field", "value")
    #         assert op == Q(field__lt="value")
    #         op = ComparisonCondition._gt_operator("field", "value")
    #         assert op == Q(field__gt="value")
    #         op = ComparisonCondition._lte_operator("field", "value")
    #         assert op == Q(field__lte="value")
    #         op = ComparisonCondition._gte_operator("field", "value")
    #         assert op == Q(field__gte="value")
    #
    #     def test_comparison_condition_init_with_correct_operator(self):
    #         lt_cond = ComparisonCondition(op="lt")
    #         assert lt_cond.operator == ComparisonCondition._lt_operator
    #         nlt_cond = ComparisonCondition(op="lt", negation=True)
    #         assert nlt_cond.operator == ComparisonCondition._gte_operator
    #
    #         gt_cond = ComparisonCondition(op="gt")
    #         assert gt_cond.operator == ComparisonCondition._gt_operator
    #         ngt_cond = ComparisonCondition(op="gt", negation=True)
    #         assert ngt_cond.operator == ComparisonCondition._lte_operator
    #
    #         lte_cond = ComparisonCondition(op="lte")
    #         assert lte_cond.operator == ComparisonCondition._lte_operator
    #         nlte_cond = ComparisonCondition(op="lte", negation=True)
    #         assert nlte_cond.operator == ComparisonCondition._gt_operator
    #
    #         gte_cond = ComparisonCondition(op="gte")
    #         assert gte_cond.operator == ComparisonCondition._gte_operator
    #         ngte_cond = ComparisonCondition(op="gte", negation=True)
    #         assert ngte_cond.operator == ComparisonCondition._lt_operator

    # def test_comparison_apply(self):
    #     self.run.label_annotations.set(
    #         [
    #             LabelAnnotation.objects.create(
    #                 project=self.project, value=0.1, name="loss"
    #             ),
    #             LabelAnnotation.objects.create(
    #                 project=self.project, name="step", value=1
    #             ),
    #         ]
    #     )
    #     self.run.metric_annotations.set(
    #         [
    #             MetricAnnotation.objects.create(
    #                 project=self.project, value=0.1, name="loss"
    #             ),
    #             MetricAnnotation.objects.create(
    #                 project=self.project, name="step", value=1
    #             ),
    #         ]
    #     )
    #     run = RunFactory(project=self.project, operation=self.operation)
    #     run.label_annotations.set(
    #         [
    #             LabelAnnotation.objects.create(
    #                 project=self.project, value=0.3, name="loss"
    #             ),
    #             LabelAnnotation.objects.create(
    #                 project=self.project, name="step", value=10
    #             ),
    #         ]
    #     )
    #     run.metric_annotations.set(
    #         [
    #             MetricAnnotation.objects.create(
    #                 project=self.project, value=0.3, name="loss"
    #             ),
    #             MetricAnnotation.objects.create(
    #                 project=self.project, name="step", value=10
    #             ),
    #         ]
    #     )
    #     run = RunFactory(project=self.project, operation=self.operation)
    #     run.label_annotations.set(
    #         [
    #             LabelAnnotation.objects.create(
    #                 project=self.project, value=0.9, name="loss"
    #             ),
    #             LabelAnnotation.objects.create(
    #                 project=self.project, name="step", value=100
    #             ),
    #         ]
    #     )
    #     run.metric_annotations.set(
    #         [
    #             MetricAnnotation.objects.create(
    #                 project=self.project, value=0.9, name="loss"
    #             ),
    #             MetricAnnotation.objects.create(
    #                 project=self.project, name="step", value=100
    #             ),
    #         ]
    #     )
    #     run = RunFactory(project=self.project, operation=self.operation)
    #     run.label_annotations.set(
    #         [
    #             LabelAnnotation.objects.create(
    #                 project=self.project, name="rate", value=-1
    #             ),
    #             LabelAnnotation.objects.create(
    #                 project=self.project, name="loss", value="bar"
    #             ),
    #         ]
    #     )
    #
    #     eq_cond = ComparisonCondition(op="eq")
    #     neq_cond = ComparisonCondition(op="eq", negation=True)
    #     lt_cond = ComparisonCondition(op="lt")
    #     lte_cond = ComparisonCondition(op="lte")
    #     gt_cond = ComparisonCondition(op="gt")
    #     gte_cond = ComparisonCondition(op="gte")
    #
    #     # eq
    #     queryset = Run.objects.filter(
    #         eq_cond.apply_operator(name="label_annotations__value", params=0.1),
    #         eq_cond.apply_operator(name="label_annotations__name", params="loss"),
    #     )
    #     assert queryset.count() == 1
    #
    #     queryset = Run.objects.filter(
    #         eq_cond.apply_operator(name="label_annotations__value", params=0.2),
    #         eq_cond.apply_operator(name="label_annotations__name", params="loss"),
    #     )
    #     assert queryset.count() == 0
    #
    #     queryset = Run.objects.filter(
    #         eq_cond.apply_operator(name="label_annotations__value", params=100),
    #         eq_cond.apply_operator(name="label_annotations__name", params="step"),
    #     )
    #     assert queryset.count() == 1
    #
    #     # neq must use the table directly
    #     queryset = Run.objects.filter(
    #         neq_cond.apply_operator(name="label_annotations__value", params=1),
    #         eq_cond.apply_operator(name="label_annotations__name", params="rate"),
    #     )
    #     assert queryset.count() == 1
    #
    #     queryset = Run.objects.filter(
    #         neq_cond.apply_operator(name="label_annotations__value", params=-1)
    #     )
    #     assert queryset.count() == 3
    #
    #     # lt
    #     queryset = lt_cond.apply(
    #         queryset=Run.objects, name="metric_annotations__value", params=0.1
    #     )
    #     queryset = eq_cond.apply(
    #         queryset=queryset, name="metric_annotations__name", params="loss"
    #     )
    #     assert queryset.count() == 0
    #
    #     queryset = lt_cond.apply(
    #         queryset=Run.objects, name="metric_annotations__value", params=0.2
    #     )
    #     queryset = eq_cond.apply(
    #         queryset=queryset, name="metric_annotations__name", params="loss"
    #     )
    #     assert queryset.count() == 1
    #
    #     queryset = lt_cond.apply(
    #         queryset=Run.objects, name="metric_annotations__value", params=0.9
    #     )
    #     queryset = eq_cond.apply(
    #         queryset=queryset, name="metric_annotations__name", params="loss"
    #     )
    #     assert queryset.count() == 2
    #
    #     # lte
    #     queryset = lte_cond.apply(
    #         queryset=Run.objects, name="metric_annotations__value", params=0.1
    #     )
    #     queryset = eq_cond.apply(
    #         queryset=queryset, name="metric_annotations__name", params="loss"
    #     )
    #     assert queryset.count() == 1
    #
    #     queryset = lte_cond.apply(
    #         queryset=Run.objects, name="metric_annotations__value", params=0.2
    #     )
    #     queryset = eq_cond.apply(
    #         queryset=queryset, name="metric_annotations__name", params="loss"
    #     )
    #     assert queryset.count() == 1
    #
    #     queryset = lte_cond.apply(
    #         queryset=Run.objects, name="metric_annotations__value", params=0.9
    #     )
    #     queryset = eq_cond.apply(
    #         queryset=queryset, name="metric_annotations__name", params="loss"
    #     )
    #     assert queryset.count() == 3
    #
    #     # gt
    #     queryset = Run.objects.filter(
    #         gt_cond.apply_operator(name="metric_annotations__value", params=0.1),
    #         eq_cond.apply_operator(name="metric_annotations__name", params="loss"),
    #     )
    #     assert queryset.count() == 2
    #
    #     queryset = Run.objects.filter(
    #         gt_cond.apply_operator(name="metric_annotations__value", params=0.2),
    #         eq_cond.apply_operator(name="metric_annotations__name", params="loss"),
    #     )
    #     assert queryset.count() == 2
    #
    #     queryset = Run.objects.filter(
    #         gt_cond.apply_operator(name="metric_annotations__value", params=0.9),
    #         eq_cond.apply_operator(name="metric_annotations__name", params="loss"),
    #     )
    #     assert queryset.count() == 0
    #
    #     # gte
    #     queryset = Run.objects.filter(
    #         gte_cond.apply_operator(name="metric_annotations__value", params=0.1),
    #         eq_cond.apply_operator(name="metric_annotations__name", params="loss"),
    #     )
    #     assert queryset.count() == 3
    #
    #     queryset = Run.objects.filter(
    #         gte_cond.apply_operator(name="metric_annotations__value", params=0.2),
    #         eq_cond.apply_operator(name="metric_annotations__name", params="loss"),
    #     )
    #     assert queryset.count() == 2
    #
    #     queryset = Run.objects.filter(
    #         gte_cond.apply_operator(name="metric_annotations__value", params=0.9),
    #         eq_cond.apply_operator(name="metric_annotations__name", params="loss"),
    #     )
    #     assert queryset.count() == 1


class TestComparisonCondition(BaseTestQuery):
    def test_comparison_operators(self):
        op = ComparisonCondition._lt_operator(
            "field", "value", query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == Q(field__lt="value")
        op = ComparisonCondition._gt_operator(
            "field", "value", query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == Q(field__gt="value")
        op = ComparisonCondition._lte_operator(
            "field", "value", query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == Q(field__lte="value")
        op = ComparisonCondition._gte_operator(
            "field", "value", query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == Q(field__gte="value")

    def test_comparison_condition_init_with_correct_operator(self):
        lt_cond = ComparisonCondition(op="lt")
        assert lt_cond.operator == ComparisonCondition._lt_operator
        nlt_cond = ComparisonCondition(op="lt", negation=True)
        assert nlt_cond.operator == ComparisonCondition._gte_operator

        gt_cond = ComparisonCondition(op="gt")
        assert gt_cond.operator == ComparisonCondition._gt_operator
        ngt_cond = ComparisonCondition(op="gt", negation=True)
        assert ngt_cond.operator == ComparisonCondition._lte_operator

        lte_cond = ComparisonCondition(op="lte")
        assert lte_cond.operator == ComparisonCondition._lte_operator
        nlte_cond = ComparisonCondition(op="lte", negation=True)
        assert nlte_cond.operator == ComparisonCondition._gt_operator

        gte_cond = ComparisonCondition(op="gte")
        assert gte_cond.operator == ComparisonCondition._gte_operator
        ngte_cond = ComparisonCondition(op="gte", negation=True)
        assert ngte_cond.operator == ComparisonCondition._lt_operator

    def test_comparison_apply(self):
        self.run.inputs = {"rate": 1, "loss": "foo"}
        self.run.save()
        RunFactory(
            project=self.project, is_managed=False, outputs={"loss": 0.1, "step": 1}
        )
        RunFactory(
            project=self.project, is_managed=False, outputs={"loss": 0.3, "step": 10}
        )
        RunFactory(
            project=self.project, is_managed=False, inputs={"rate": -1, "loss": "bar"}
        )

        RunFactory(
            project=self.project, is_managed=False, outputs={"loss": 0.9, "step": 100}
        )

        eq_cond = ComparisonCondition(op="eq")
        neq_cond = ComparisonCondition(op="eq", negation=True)
        lt_cond = ComparisonCondition(op="lt")
        lte_cond = ComparisonCondition(op="lte")
        gt_cond = ComparisonCondition(op="gt")
        gte_cond = ComparisonCondition(op="gte")

        # eq
        queryset = eq_cond.apply(
            queryset=Run.objects,
            name="outputs__loss",
            params=0.1,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = eq_cond.apply(
            queryset=Run.objects,
            name="outputs__loss",
            params=0.2,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        queryset = eq_cond.apply(
            queryset=Run.objects,
            name="outputs__step",
            params=10,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        # neq must use the table directly
        queryset = neq_cond.apply(
            queryset=Run.objects,
            name="inputs__rate",
            params=1,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 4

        queryset = neq_cond.apply(
            queryset=Run.objects,
            name="inputs__rate",
            params=-1,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 4

        queryset = neq_cond.apply(
            queryset=Run.objects,
            name="inputs__rate",
            params=-12,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 5

        queryset = neq_cond.apply(
            queryset=Run.objects,
            name="inputs__loss",
            params="foo",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 4

        queryset = neq_cond.apply(
            queryset=Run.objects,
            name="inputs__loss",
            params="moo",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 5

        # lt
        queryset = lt_cond.apply(
            queryset=Run.objects,
            name="outputs__loss",
            params=0.1,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        queryset = lt_cond.apply(
            queryset=Run.objects,
            name="outputs__loss",
            params=0.2,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = lt_cond.apply(
            queryset=Run.objects,
            name="outputs__loss",
            params=0.9,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        # lte
        queryset = lte_cond.apply(
            queryset=Run.objects,
            name="outputs__loss",
            params=0.1,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = lte_cond.apply(
            queryset=Run.objects,
            name="outputs__loss",
            params=0.2,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = lte_cond.apply(
            queryset=Run.objects,
            name="outputs__loss",
            params=0.9,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 3

        # gt
        queryset = gt_cond.apply(
            queryset=Run.objects,
            name="outputs__loss",
            params=0.1,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        queryset = gt_cond.apply(
            queryset=Run.objects,
            name="outputs__loss",
            params=0.2,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        queryset = gt_cond.apply(
            queryset=Run.objects,
            name="outputs__loss",
            params=0.9,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        # gte
        queryset = gte_cond.apply(
            queryset=Run.objects,
            name="outputs__loss",
            params=0.1,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 3

        queryset = gte_cond.apply(
            queryset=Run.objects,
            name="outputs__loss",
            params=0.2,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        queryset = gte_cond.apply(
            queryset=Run.objects,
            name="outputs__loss",
            params=0.9,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1


class TestDateTimeCondition(BaseTestQuery):
    def test_range_operators(self):
        with self.assertRaises(AssertionError):
            DateTimeCondition._range_operator(
                "field", "value", query_backend=Q, timezone=settings.TIME_ZONE
            )

        with self.assertRaises(AssertionError):
            DateTimeCondition._nrange_operator(
                "field", "value", query_backend=Q, timezone=settings.TIME_ZONE
            )

        with self.assertRaises(PQLException):
            DateTimeCondition._range_operator(
                "field", ("v1", "v2"), query_backend=Q, timezone=settings.TIME_ZONE
            )

        with self.assertRaises(PQLException):
            DateTimeCondition._nrange_operator(
                "field",
                ("v1", "2010-01-01"),
                query_backend=Q,
                timezone=settings.TIME_ZONE,
            )

        with self.assertRaises(PQLException):
            DateTimeCondition._nrange_operator(
                "field",
                ("2010-01-01", "v2"),
                query_backend=Q,
                timezone=settings.TIME_ZONE,
            )

        assert DateTimeCondition._range_operator(
            "field",
            ("2010-01-01", "2010-01-01"),
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        ) == Q(
            field__range=(
                DateTimeFormatter.extract("2010-01-01", settings.TIME_ZONE),
                DateTimeFormatter.extract("2010-01-01", settings.TIME_ZONE),
            )
        )
        assert DateTimeCondition._nrange_operator(
            "field",
            ("2010-01-01 10:10", "2010-01-01"),
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        ) == ~Q(
            field__range=(
                DateTimeFormatter.extract("2010-01-01 10:10", settings.TIME_ZONE),
                DateTimeFormatter.extract("2010-01-01", settings.TIME_ZONE),
            )
        )

    def test_range_condition_init_with_correct_operator(self):
        range_cond = DateTimeCondition(op="range")
        assert range_cond.operator == DateTimeCondition._range_operator
        nrange_cond = DateTimeCondition(op="range", negation=True)
        assert nrange_cond.operator == DateTimeCondition._nrange_operator

    @pytest.mark.filterwarnings("ignore::RuntimeWarning")
    def test_range_apply(self):
        # Delete current run
        self.run.delete()

        run = RunFactory(
            project=self.project,
            is_managed=False,
            outputs={"accuracy": 0.9, "precision": 0.9},
        )
        run.created_at = datetime.datetime(2018, 1, 1)
        run.save()
        run = RunFactory(
            project=self.project,
            is_managed=False,
            outputs={"accuracy": 0.9, "precision": 0.9},
        )
        run.created_at = datetime.datetime(2010, 1, 1)
        run.save()

        eq_cond = DateTimeCondition(op="eq")
        lt_cond = DateTimeCondition(op="lt")
        lte_cond = DateTimeCondition(op="lte")
        gt_cond = DateTimeCondition(op="gt")
        gte_cond = DateTimeCondition(op="gte")
        range_cond = DateTimeCondition(op="range")
        nrange_cond = DateTimeCondition(op="range", negation=True)

        # eq
        queryset = eq_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params="2018-01-01",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = eq_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params="2018-02-01",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        # lt
        queryset = lt_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params="2018-02-01",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        queryset = lt_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params="2018-01-01",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = lt_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params="2008-01-01",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        # lte
        queryset = lte_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params="2018-02-01",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        queryset = lte_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params="2018-01-01",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        queryset = lte_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params="2008-01-01",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        # gt
        queryset = gt_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params="2018-02-01",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        queryset = gt_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params="2018-01-01",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        queryset = gt_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params="2008-01-01",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        # lte
        queryset = gte_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params="2018-02-01",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        queryset = gte_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params="2018-01-01",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = gte_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params="2008-01-01",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        # range
        queryset = range_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params=(
                DateTimeFormatter.extract("2018-02-01 00:00", settings.TIME_ZONE),
                DateTimeFormatter.extract("2018-03-01 00:00", settings.TIME_ZONE),
            ),
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        queryset = range_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params=(
                DateTimeFormatter.extract("2018-02-01", settings.TIME_ZONE),
                DateTimeFormatter.extract("2008-03-01", settings.TIME_ZONE),
            ),
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        queryset = range_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params=(
                DateTimeFormatter.extract("2017-02-01", settings.TIME_ZONE),
                DateTimeFormatter.extract("2018-03-01", settings.TIME_ZONE),
            ),
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = range_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params=(
                DateTimeFormatter.extract("2008-02-01 00:00:12", settings.TIME_ZONE),
                DateTimeFormatter.extract("2018-03-01", settings.TIME_ZONE),
            ),
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        queryset = range_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params=(
                DateTimeFormatter.extract("2010-01-01", settings.TIME_ZONE),
                DateTimeFormatter.extract("2010-01-01", settings.TIME_ZONE),
            ),
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        # nrange
        queryset = nrange_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params=(
                DateTimeFormatter.extract("2018-02-01 00:00", settings.TIME_ZONE),
                DateTimeFormatter.extract("2018-03-01 00:00", settings.TIME_ZONE),
            ),
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        queryset = nrange_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params=(
                DateTimeFormatter.extract("2018-02-01", settings.TIME_ZONE),
                DateTimeFormatter.extract("2008-03-01", settings.TIME_ZONE),
            ),
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        queryset = nrange_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params=(
                DateTimeFormatter.extract("2017-02-01", settings.TIME_ZONE),
                DateTimeFormatter.extract("2018-03-01", settings.TIME_ZONE),
            ),
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = nrange_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params=(
                DateTimeFormatter.extract("2008-02-01 00:00:12", settings.TIME_ZONE),
                DateTimeFormatter.extract("2018-03-01", settings.TIME_ZONE),
            ),
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        queryset = nrange_cond.apply(
            queryset=Run.objects,
            name="created_at",
            params=(
                DateTimeFormatter.extract("2010-01-01", settings.TIME_ZONE),
                DateTimeFormatter.extract("2010-01-01", settings.TIME_ZONE),
            ),
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2


class TestValueCondition(BaseTestQuery):
    def test_value_operators(self):
        op = ValueCondition._in_operator(
            "field", ["v1", "v2"], query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == Q(field__in=["v1", "v2"])
        op = ValueCondition._nin_operator(
            "field", ["v1", "v2"], query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == ~Q(field__in=["v1", "v2"])

    def test_range_apply(self):
        new_run_status(
            self.run,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.FAILED, status=True
            ),
        )
        run2 = RunFactory(project=self.project)
        new_run_status(
            run2,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.STOPPED, status=True
            ),
        )
        run3 = RunFactory(project=self.project)
        new_run_status(
            run3,
            condition=V1StatusCondition.get_condition(
                type=V1Statuses.RUNNING, status=True
            ),
        )

        eq_cond = ValueCondition(op="eq")
        neq_cond = ValueCondition(op="eq", negation=True)
        in_cond = ValueCondition(op="in")
        nin_cond = ValueCondition(op="in", negation=True)

        # eq
        queryset = eq_cond.apply(
            queryset=Run.objects,
            name="status",
            params=V1Statuses.STOPPED,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = eq_cond.apply(
            queryset=Run.objects,
            name="status",
            params="foo",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        # neq
        queryset = neq_cond.apply(
            queryset=Run.objects,
            name="status",
            params=V1Statuses.STOPPED,
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        queryset = neq_cond.apply(
            queryset=Run.objects,
            name="status",
            params="doo",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 3

        # in
        queryset = in_cond.apply(
            queryset=Run.objects,
            name="status",
            params=[V1Statuses.STOPPED, V1Statuses.RUNNING],
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        queryset = in_cond.apply(
            queryset=Run.objects,
            name="status",
            params=[V1Statuses.STOPPED, V1Statuses.RESUMING],
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = in_cond.apply(
            queryset=Run.objects,
            name="status",
            params=[V1Statuses.RESUMING, V1Statuses.SKIPPED],
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        queryset = in_cond.apply(
            queryset=Run.objects,
            name="status",
            params=[V1Statuses.FAILED, V1Statuses.STOPPED, V1Statuses.RUNNING],
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 3

        # nin
        queryset = nin_cond.apply(
            queryset=Run.objects,
            name="status",
            params=[V1Statuses.STOPPED, V1Statuses.RUNNING],
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = nin_cond.apply(
            queryset=Run.objects,
            name="status",
            params=[V1Statuses.STOPPED, V1Statuses.RESUMING],
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        queryset = nin_cond.apply(
            queryset=Run.objects,
            name="status",
            params=[V1Statuses.RESUMING, V1Statuses.SKIPPED],
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 3

        queryset = nin_cond.apply(
            queryset=Run.objects,
            name="status",
            params=[V1Statuses.FAILED, V1Statuses.STOPPED, V1Statuses.RUNNING],
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0


class TestSearchCondition(BaseTestQuery):
    def test_contains_operators(self):
        op = SearchCondition._contains_operator(
            "field", "v1", query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == Q(field__icontains="v1")
        op = SearchCondition._ncontains_operator(
            "field", "v1", query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == ~Q(field__icontains="v1")

    def test_startswith_operators(self):
        op = SearchCondition._startswith_operator(
            "field", "v1", query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == Q(field__istartswith="v1")
        op = SearchCondition._nstartswith_operator(
            "field", "v1", query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == ~Q(field__istartswith="v1")

    def test_endswith_operators(self):
        op = SearchCondition._endswith_operator(
            "field", "v1", query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == Q(field__iendswith="v1")
        op = SearchCondition._nendswith_operator(
            "field", "v1", query_backend=Q, timezone=settings.TIME_ZONE
        )
        assert op == ~Q(field__iendswith="v1")

    def test_range_apply(self):
        RunFactory(project=self.project, name="foo_bar")
        RunFactory(project=self.project, name="foo_moo")
        self.run.name = "moo_boo"
        self.run.save()

        contains_cond = SearchCondition(op="icontains")
        ncontains_cond = SearchCondition(op="icontains", negation=True)
        startswith_cond = SearchCondition(op="istartswith")
        nstartswith_cond = SearchCondition(op="istartswith", negation=True)
        endswith_cond = SearchCondition(op="iendswith")
        nendswith_cond = SearchCondition(op="iendswith", negation=True)

        # contains
        queryset = contains_cond.apply(
            queryset=Run.objects,
            name="name",
            params="foo",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        queryset = contains_cond.apply(
            queryset=Run.objects,
            name="name",
            params="bar",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = contains_cond.apply(
            queryset=Run.objects,
            name="name",
            params="boo",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = contains_cond.apply(
            queryset=Run.objects,
            name="name",
            params="none",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        # ncontains
        queryset = ncontains_cond.apply(
            queryset=Run.objects,
            name="name",
            params="foo",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = ncontains_cond.apply(
            queryset=Run.objects,
            name="name",
            params="bar",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        queryset = ncontains_cond.apply(
            queryset=Run.objects,
            name="name",
            params="boo",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        queryset = ncontains_cond.apply(
            queryset=Run.objects,
            name="name",
            params="none",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 3

        # startswith
        queryset = startswith_cond.apply(
            queryset=Run.objects,
            name="name",
            params="foo",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        queryset = startswith_cond.apply(
            queryset=Run.objects,
            name="name",
            params="bar",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        queryset = startswith_cond.apply(
            queryset=Run.objects,
            name="name",
            params="moo",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        # nstartswith
        queryset = nstartswith_cond.apply(
            queryset=Run.objects,
            name="name",
            params="foo",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = nstartswith_cond.apply(
            queryset=Run.objects,
            name="name",
            params="bar",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 3

        queryset = nstartswith_cond.apply(
            queryset=Run.objects,
            name="name",
            params="moo",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        # endswith
        queryset = endswith_cond.apply(
            queryset=Run.objects,
            name="name",
            params="foo",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 0

        queryset = endswith_cond.apply(
            queryset=Run.objects,
            name="name",
            params="bar",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        queryset = endswith_cond.apply(
            queryset=Run.objects,
            name="name",
            params="moo",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 1

        # nendswith
        queryset = nendswith_cond.apply(
            queryset=Run.objects,
            name="name",
            params="foo",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 3

        queryset = nendswith_cond.apply(
            queryset=Run.objects,
            name="name",
            params="bar",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2

        queryset = nendswith_cond.apply(
            queryset=Run.objects,
            name="name",
            params="moo",
            query_backend=Q,
            timezone=settings.TIME_ZONE,
        )
        assert queryset.count() == 2


del BaseTestQuery
