import datetime

import pytest

from django.db.models import Q

from constants.experiments import ExperimentLifeCycle
from db.models.experiments import Experiment, ExperimentMetric
from factories.factory_experiments import (
    ExperimentFactory,
    ExperimentMetricFactory,
    ExperimentStatusFactory
)
from libs.date_utils import DateTimeFormatter
from query.builder import ComparisonCondition, DateTimeCondition, EqualityCondition, ValueCondition
from query.exceptions import QueryConditionException
from tests.utils import BaseTest

# pylint:disable=protected-access


@pytest.mark.query_mark
class TestEqualityCondition(BaseTest):
    DISABLE_RUNNER = True

    def test_equality_operators(self):
        op = EqualityCondition._eq_operator('field', 'value')
        assert op == Q(field='value')
        op = EqualityCondition._neq_operator('field', 'value')
        assert op == ~Q(field='value')

    def test_equality_condition_init_with_correct_operator(self):
        eq_cond = EqualityCondition(op='eq')
        assert eq_cond.operator == EqualityCondition._eq_operator
        neq_cond = EqualityCondition(op='eq', negation=True)
        assert neq_cond.operator == EqualityCondition._neq_operator

    def test_equality_apply(self):
        eq_cond = EqualityCondition(op='eq')
        neq_cond = EqualityCondition(op='eq', negation=True)

        ExperimentStatusFactory(status=ExperimentLifeCycle.SCHEDULED)

        # eq
        queryset = eq_cond.apply(queryset=Experiment.objects,
                                 name='status__status',
                                 params=ExperimentLifeCycle.SCHEDULED)
        assert queryset.count() == 1

        queryset = eq_cond.apply(queryset=Experiment.objects,
                                 name='status__status',
                                 params=ExperimentLifeCycle.SUCCEEDED)
        assert queryset.count() == 0

        # neq
        queryset = neq_cond.apply(queryset=Experiment.objects,
                                  name='status__status',
                                  params=ExperimentLifeCycle.SCHEDULED)
        assert queryset.count() == 0

        queryset = neq_cond.apply(queryset=Experiment.objects,
                                  name='status__status',
                                  params=ExperimentLifeCycle.SUCCEEDED)
        assert queryset.count() == 1


@pytest.mark.query_mark
class TestComparisonCondition(BaseTest):
    DISABLE_RUNNER = True

    def test_comparison_operators(self):
        op = ComparisonCondition._lt_operator('field', 'value')
        assert op == Q(field__lt='value')
        op = ComparisonCondition._gt_operator('field', 'value')
        assert op == Q(field__gt='value')
        op = ComparisonCondition._lte_operator('field', 'value')
        assert op == Q(field__lte='value')
        op = ComparisonCondition._gte_operator('field', 'value')
        assert op == Q(field__gte='value')

    def test_comparison_condition_init_with_correct_operator(self):
        lt_cond = ComparisonCondition(op='lt')
        assert lt_cond.operator == ComparisonCondition._lt_operator
        nlt_cond = ComparisonCondition(op='lt', negation=True)
        assert nlt_cond.operator == ComparisonCondition._gte_operator

        gt_cond = ComparisonCondition(op='gt')
        assert gt_cond.operator == ComparisonCondition._gt_operator
        ngt_cond = ComparisonCondition(op='gt', negation=True)
        assert ngt_cond.operator == ComparisonCondition._lte_operator

        lte_cond = ComparisonCondition(op='lte')
        assert lte_cond.operator == ComparisonCondition._lte_operator
        nlte_cond = ComparisonCondition(op='lte', negation=True)
        assert nlte_cond.operator == ComparisonCondition._gt_operator

        gte_cond = ComparisonCondition(op='gte')
        assert gte_cond.operator == ComparisonCondition._gte_operator
        ngte_cond = ComparisonCondition(op='gte', negation=True)
        assert ngte_cond.operator == ComparisonCondition._lt_operator

    def test_comparison_apply(self):
        ExperimentMetricFactory(values={'loss': 0.1, 'step': 1})
        ExperimentMetricFactory(values={'loss': 0.3, 'step': 10})
        ExperimentMetricFactory(values={'loss': 0.9, 'step': 100})
        ExperimentFactory(declarations={'rate': 1, 'loss': 'foo'})
        ExperimentFactory(declarations={'rate': -1, 'loss': 'bar'})

        eq_cond = ComparisonCondition(op='eq')
        neq_cond = ComparisonCondition(op='eq', negation=True)
        lt_cond = ComparisonCondition(op='lt')
        lte_cond = ComparisonCondition(op='lte')
        gt_cond = ComparisonCondition(op='gt')
        gte_cond = ComparisonCondition(op='gte')

        # eq
        queryset = eq_cond.apply(queryset=Experiment.objects,
                                 name='metric__values__loss',
                                 params=0.1)
        assert queryset.count() == 1

        queryset = eq_cond.apply(queryset=Experiment.objects,
                                 name='metric__values__loss',
                                 params=0.2)
        assert queryset.count() == 0

        queryset = eq_cond.apply(queryset=Experiment.objects,
                                 name='metric__values__step',
                                 params=10)
        assert queryset.count() == 1

        # neq must use the table directly
        queryset = neq_cond.apply(queryset=Experiment.objects,
                                  name='declarations__rate',
                                  params=1)
        assert queryset.count() == 4

        queryset = neq_cond.apply(queryset=Experiment.objects,
                                  name='declarations__rate',
                                  params=-1)
        assert queryset.count() == 4

        queryset = neq_cond.apply(queryset=Experiment.objects,
                                  name='declarations__rate',
                                  params=-12)
        assert queryset.count() == 5

        queryset = neq_cond.apply(queryset=Experiment.objects,
                                  name='declarations__loss',
                                  params='foo')
        assert queryset.count() == 4

        queryset = neq_cond.apply(queryset=Experiment.objects,
                                  name='declarations__loss',
                                  params='moo')
        assert queryset.count() == 5

        # lt
        queryset = lt_cond.apply(queryset=Experiment.objects,
                                 name='metric__values__loss',
                                 params=0.1)
        assert queryset.count() == 0

        queryset = lt_cond.apply(queryset=Experiment.objects,
                                 name='metric__values__loss',
                                 params=0.2)
        assert queryset.count() == 1

        queryset = lt_cond.apply(queryset=Experiment.objects,
                                 name='metric__values__loss',
                                 params=0.9)
        assert queryset.count() == 2

        # lte
        queryset = lte_cond.apply(queryset=Experiment.objects,
                                  name='metric__values__loss',
                                  params=0.1)
        assert queryset.count() == 1

        queryset = lte_cond.apply(queryset=Experiment.objects,
                                  name='metric__values__loss',
                                  params=0.2)
        assert queryset.count() == 1

        queryset = lte_cond.apply(queryset=Experiment.objects,
                                  name='metric__values__loss',
                                  params=0.9)
        assert queryset.count() == 3

        # gt
        queryset = gt_cond.apply(queryset=Experiment.objects,
                                 name='metric__values__loss',
                                 params=0.1)
        assert queryset.count() == 2

        queryset = gt_cond.apply(queryset=Experiment.objects,
                                 name='metric__values__loss',
                                 params=0.2)
        assert queryset.count() == 2

        queryset = gt_cond.apply(queryset=Experiment.objects,
                                 name='metric__values__loss',
                                 params=0.9)
        assert queryset.count() == 0

        # gte
        queryset = gte_cond.apply(queryset=Experiment.objects,
                                  name='metric__values__loss',
                                  params=0.1)
        assert queryset.count() == 3

        queryset = gte_cond.apply(queryset=Experiment.objects,
                                  name='metric__values__loss',
                                  params=0.2)
        assert queryset.count() == 2

        queryset = gte_cond.apply(queryset=Experiment.objects,
                                  name='metric__values__loss',
                                  params=0.9)
        assert queryset.count() == 1


@pytest.mark.query_mark
class TestDateTimeCondition(BaseTest):
    DISABLE_RUNNER = True

    def test_range_operators(self):
        with self.assertRaises(AssertionError):
            DateTimeCondition._range_operator('field', 'value')

        with self.assertRaises(AssertionError):
            DateTimeCondition._nrange_operator('field', 'value')

        with self.assertRaises(QueryConditionException):
            DateTimeCondition._range_operator(
                'field', ('v1', 'v2'))

        with self.assertRaises(QueryConditionException):
            DateTimeCondition._nrange_operator(
                'field', ('v1', '2010-01-01'))

        with self.assertRaises(QueryConditionException):
            DateTimeCondition._nrange_operator(
                'field', ('2010-01-01', 'v2'))

        assert DateTimeCondition._range_operator(
            'field', ('2010-01-01', '2010-01-01')) == Q(
            field__range=(DateTimeFormatter.extract('2010-01-01'),
                          DateTimeFormatter.extract('2010-01-01')))
        assert DateTimeCondition._nrange_operator(
            'field', ('2010-01-01 10:10', '2010-01-01')) == ~Q(
            field__range=(DateTimeFormatter.extract('2010-01-01 10:10'),
                          DateTimeFormatter.extract('2010-01-01')))

    def test_range_condition_init_with_correct_operator(self):
        range_cond = DateTimeCondition(op='range')
        assert range_cond.operator == DateTimeCondition._range_operator
        nrange_cond = DateTimeCondition(op='range', negation=True)
        assert nrange_cond.operator == DateTimeCondition._nrange_operator

    def test_range_apply(self):
        ExperimentMetricFactory(created_at=datetime.datetime(2018, 1, 1))
        ExperimentMetricFactory(created_at=datetime.datetime(2010, 1, 1))

        eq_cond = DateTimeCondition(op='eq')
        lt_cond = DateTimeCondition(op='lt')
        lte_cond = DateTimeCondition(op='lte')
        gt_cond = DateTimeCondition(op='gt')
        gte_cond = DateTimeCondition(op='gte')
        range_cond = DateTimeCondition(op='range')
        nrange_cond = DateTimeCondition(op='range', negation=True)

        # eq
        queryset = eq_cond.apply(queryset=ExperimentMetric.objects,
                                 name='created_at',
                                 params='2018-01-01')
        assert queryset.count() == 1

        queryset = eq_cond.apply(queryset=ExperimentMetric.objects,
                                 name='created_at',
                                 params='2018-02-01')
        assert queryset.count() == 0

        # lt
        queryset = lt_cond.apply(queryset=ExperimentMetric.objects,
                                 name='created_at',
                                 params='2018-02-01')
        assert queryset.count() == 2

        queryset = lt_cond.apply(queryset=ExperimentMetric.objects,
                                 name='created_at',
                                 params='2018-01-01')
        assert queryset.count() == 1

        queryset = lt_cond.apply(queryset=ExperimentMetric.objects,
                                 name='created_at',
                                 params='2008-01-01')
        assert queryset.count() == 0

        # lte
        queryset = lte_cond.apply(queryset=ExperimentMetric.objects,
                                  name='created_at',
                                  params='2018-02-01')
        assert queryset.count() == 2

        queryset = lte_cond.apply(queryset=ExperimentMetric.objects,
                                  name='created_at',
                                  params='2018-01-01')
        assert queryset.count() == 2

        queryset = lte_cond.apply(queryset=ExperimentMetric.objects,
                                  name='created_at',
                                  params='2008-01-01')
        assert queryset.count() == 0

        # gt
        queryset = gt_cond.apply(queryset=ExperimentMetric.objects,
                                 name='created_at',
                                 params='2018-02-01')
        assert queryset.count() == 0

        queryset = gt_cond.apply(queryset=ExperimentMetric.objects,
                                 name='created_at',
                                 params='2018-01-01')
        assert queryset.count() == 0

        queryset = gt_cond.apply(queryset=ExperimentMetric.objects,
                                 name='created_at',
                                 params='2008-01-01')
        assert queryset.count() == 2

        # lte
        queryset = gte_cond.apply(queryset=ExperimentMetric.objects,
                                  name='created_at',
                                  params='2018-02-01')
        assert queryset.count() == 0

        queryset = gte_cond.apply(queryset=ExperimentMetric.objects,
                                  name='created_at',
                                  params='2018-01-01')
        assert queryset.count() == 1

        queryset = gte_cond.apply(queryset=ExperimentMetric.objects,
                                  name='created_at',
                                  params='2008-01-01')
        assert queryset.count() == 2

        # range
        queryset = range_cond.apply(
            queryset=ExperimentMetric.objects,
            name='created_at',
            params=(DateTimeFormatter.extract('2018-02-01 00:00'),
                    DateTimeFormatter.extract('2018-03-01 00:00')))
        assert queryset.count() == 0

        queryset = range_cond.apply(
            queryset=ExperimentMetric.objects,
            name='created_at',
            params=(DateTimeFormatter.extract('2018-02-01'),
                    DateTimeFormatter.extract('2008-03-01')))
        assert queryset.count() == 0

        queryset = range_cond.apply(
            queryset=ExperimentMetric.objects,
            name='created_at',
            params=(DateTimeFormatter.extract('2017-02-01'),
                    DateTimeFormatter.extract('2018-03-01')))
        assert queryset.count() == 1

        queryset = range_cond.apply(
            queryset=ExperimentMetric.objects,
            name='created_at',
            params=(DateTimeFormatter.extract('2008-02-01 00:00:12'),
                    DateTimeFormatter.extract('2018-03-01')))
        assert queryset.count() == 2

        queryset = range_cond.apply(
            queryset=ExperimentMetric.objects,
            name='created_at',
            params=(DateTimeFormatter.extract('2010-01-01'),
                    DateTimeFormatter.extract('2010-01-01')))
        assert queryset.count() == 0

        # nrange
        queryset = nrange_cond.apply(
            queryset=ExperimentMetric.objects,
            name='created_at',
            params=(DateTimeFormatter.extract('2018-02-01 00:00'),
                    DateTimeFormatter.extract('2018-03-01 00:00')))
        assert queryset.count() == 2

        queryset = nrange_cond.apply(
            queryset=ExperimentMetric.objects,
            name='created_at',
            params=(DateTimeFormatter.extract('2018-02-01'),
                    DateTimeFormatter.extract('2008-03-01')))
        assert queryset.count() == 2

        queryset = nrange_cond.apply(
            queryset=ExperimentMetric.objects,
            name='created_at',
            params=(DateTimeFormatter.extract('2017-02-01'),
                    DateTimeFormatter.extract('2018-03-01')))
        assert queryset.count() == 1

        queryset = nrange_cond.apply(
            queryset=ExperimentMetric.objects,
            name='created_at',
            params=(DateTimeFormatter.extract('2008-02-01 00:00:12'),
                    DateTimeFormatter.extract('2018-03-01')))
        assert queryset.count() == 0

        queryset = nrange_cond.apply(
            queryset=ExperimentMetric.objects,
            name='created_at',
            params=(DateTimeFormatter.extract('2010-01-01'),
                    DateTimeFormatter.extract('2010-01-01')))
        assert queryset.count() == 2


@pytest.mark.query_mark
class TestValueCondition(BaseTest):
    DISABLE_RUNNER = True

    def test_value_operators(self):
        op = ValueCondition._in_operator('field', ['v1', 'v2'])
        assert op == Q(field__in=['v1', 'v2'])
        op = ValueCondition._nin_operator('field', ['v1', 'v2'])
        assert op == ~Q(field__in=['v1', 'v2'])

    def test_range_apply(self):
        ExperimentFactory(declarations={'rate': 1, 'loss': 'foo'})
        ExperimentFactory(declarations={'rate': -1, 'loss': 'bar'})
        ExperimentFactory(declarations={'rate': 11.1, 'loss': 'moo'})

        eq_cond = ValueCondition(op='eq')
        neq_cond = ValueCondition(op='eq', negation=True)
        in_cond = ValueCondition(op='in')
        nin_cond = ValueCondition(op='in', negation=True)

        # eq
        queryset = eq_cond.apply(queryset=Experiment.objects,
                                 name='declarations__loss',
                                 params='foo')
        assert queryset.count() == 1

        queryset = eq_cond.apply(queryset=Experiment.objects,
                                 name='declarations__rate',
                                 params=0.2)
        assert queryset.count() == 0

        queryset = eq_cond.apply(queryset=Experiment.objects,
                                 name='declarations__rate',
                                 params=11.1)
        assert queryset.count() == 1

        # neq
        queryset = neq_cond.apply(queryset=Experiment.objects,
                                  name='declarations__loss',
                                  params='foo')
        assert queryset.count() == 2

        queryset = neq_cond.apply(queryset=Experiment.objects,
                                  name='declarations__rate',
                                  params=0.2)
        assert queryset.count() == 3

        queryset = neq_cond.apply(queryset=Experiment.objects,
                                  name='declarations__rate',
                                  params=11.1)
        assert queryset.count() == 2

        # in
        queryset = in_cond.apply(queryset=Experiment.objects,
                                 name='declarations__loss',
                                 params=['foo', 'bar'])
        assert queryset.count() == 2

        queryset = in_cond.apply(queryset=Experiment.objects,
                                 name='declarations__rate',
                                 params=[0.2, 11.1])
        assert queryset.count() == 1

        queryset = in_cond.apply(queryset=Experiment.objects,
                                 name='declarations__loss',
                                 params=['lll', 'ppp'])
        assert queryset.count() == 0

        queryset = in_cond.apply(queryset=Experiment.objects,
                                 name='declarations__loss',
                                 params=['lll', 'ppp', 'foo', 'bar', 'moo'])
        assert queryset.count() == 3

        # in
        queryset = nin_cond.apply(queryset=Experiment.objects,
                                  name='declarations__loss',
                                  params=['foo', 'bar'])
        assert queryset.count() == 1

        queryset = nin_cond.apply(queryset=Experiment.objects,
                                  name='declarations__rate',
                                  params=[0.2, 11.1])
        assert queryset.count() == 2

        queryset = nin_cond.apply(queryset=Experiment.objects,
                                  name='declarations__loss',
                                  params=['lll', 'ppp'])
        assert queryset.count() == 3

        queryset = nin_cond.apply(queryset=Experiment.objects,
                                  name='declarations__loss',
                                  params=['lll', 'ppp', 'foo', 'bar', 'moo'])
        assert queryset.count() == 0
