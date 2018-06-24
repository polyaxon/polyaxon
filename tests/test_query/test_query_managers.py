import pytest

from flaky import flaky

from django.db.models import Q

from db.models.experiments import Experiment
from query.builder import (
    ArrayCondition,
    ComparisonCondition,
    DateTimeCondition,
    QueryCondSpec,
    ValueCondition
)
from query.exceptions import QueryError
from query.managers.build import BuildQueryManager
from query.managers.experiment import ExperimentQueryManager
from query.managers.experiment_group import ExperimentGroupQueryManager
from query.managers.job import JobQueryManager
from query.parser import QueryOpSpec
from tests.utils import BaseTest


@pytest.mark.query_mark
class TestQueryManager(BaseTest):
    DISABLE_RUNNER = True

    def setUp(self):
        super().setUp()
        self.query1 = 'updated_at:<=2020-10-10, started_at:>2010-10-10, started_at:~2016-10-01'
        self.query2 = 'metric.loss:<=0.8, status:starting|running'
        self.query3 = 'finished_at:2012-12-12..2042-12-12'
        self.query4 = 'tags:~tag1|tag2,tags:tag3'
        self.query5 = 'foobar:2012-12-12..2042-12-12'

    def test_managers(self):
        assert ExperimentQueryManager.NAME == 'experiment'
        assert ExperimentGroupQueryManager.NAME == 'experiment_group'
        assert JobQueryManager.NAME == 'job'
        assert BuildQueryManager.NAME == 'build'

    def test_tokenize(self):
        tokenized_query = ExperimentQueryManager.tokenize(self.query1)
        assert dict(tokenized_query.items()) == {
            'updated_at': ['<=2020-10-10'],
            'started_at': ['>2010-10-10', '~2016-10-01'],
        }

        tokenized_query = ExperimentQueryManager.tokenize(self.query2)
        assert dict(tokenized_query) == {
            'metric.loss': ['<=0.8'],
            'status': ['starting|running'],
        }

        tokenized_query = ExperimentQueryManager.tokenize(self.query3)
        assert tokenized_query == {
            'finished_at': ['2012-12-12..2042-12-12'],
        }

        tokenized_query = ExperimentQueryManager.tokenize(self.query4)
        assert tokenized_query == {
            'tags': ['~tag1|tag2', 'tag3'],
        }

        with self.assertRaises(QueryError):
            ExperimentQueryManager.tokenize(self.query5)

    def test_parse(self):
        tokenized_query = ExperimentQueryManager.tokenize(self.query1)
        parsed_query = ExperimentQueryManager.parse(tokenized_query)
        assert parsed_query == {
            'updated_at': [QueryOpSpec(op='<=', negation=False, params='2020-10-10')],
            'started_at': [QueryOpSpec(op='>', negation=False, params='2010-10-10'),
                           QueryOpSpec(op='=', negation=True, params='2016-10-01')],
        }

        tokenized_query = ExperimentQueryManager.tokenize(self.query2)
        parsed_query = ExperimentQueryManager.parse(tokenized_query)
        assert parsed_query == {
            'metric.loss': [QueryOpSpec('<=', False, params=0.8)],
            'status': [QueryOpSpec('|', False, params=['starting', 'running'])],
        }

        tokenized_query = ExperimentQueryManager.tokenize(self.query3)
        parsed_query = ExperimentQueryManager.parse(tokenized_query)
        assert parsed_query == {
            'finished_at': [QueryOpSpec('..', False, params=['2012-12-12', '2042-12-12'])],
        }

        tokenized_query = ExperimentQueryManager.tokenize(self.query4)
        parsed_query = ExperimentQueryManager.parse(tokenized_query)
        assert parsed_query == {
            'tags': [QueryOpSpec('|', True, params=['tag1', 'tag2']),
                     QueryOpSpec('=', False, params='tag3')],
        }

    def test_build(self):
        tokenized_query = ExperimentQueryManager.tokenize(self.query1)
        parsed_query = ExperimentQueryManager.parse(tokenized_query)
        built_query = ExperimentQueryManager.build(parsed_query)
        assert built_query == {
            'updated_at': [
                QueryCondSpec(DateTimeCondition(op='<=', negation=False), params='2020-10-10')],
            'started_at': [
                QueryCondSpec(DateTimeCondition(op='>', negation=False), params='2010-10-10'),
                QueryCondSpec(DateTimeCondition(op='=', negation=True), params='2016-10-01')],
        }

        tokenized_query = ExperimentQueryManager.tokenize(self.query2)
        parsed_query = ExperimentQueryManager.parse(tokenized_query)
        built_query = ExperimentQueryManager.build(parsed_query)
        assert built_query == {
            'metric.loss': [
                QueryCondSpec(ComparisonCondition(op='<=', negation=False), params=0.8)],
            'status': [
                QueryCondSpec(ValueCondition(op='|', negation=False),
                              params=['starting', 'running'])],
        }

        tokenized_query = ExperimentQueryManager.tokenize(self.query3)
        parsed_query = ExperimentQueryManager.parse(tokenized_query)
        built_query = ExperimentQueryManager.build(parsed_query)
        assert built_query == {
            'finished_at': [
                QueryCondSpec(DateTimeCondition(op='..', negation=False),
                              params=['2012-12-12', '2042-12-12'])],
        }

        tokenized_query = ExperimentQueryManager.tokenize(self.query4)
        parsed_query = ExperimentQueryManager.parse(tokenized_query)
        built_query = ExperimentQueryManager.build(parsed_query)
        assert built_query == {
            'tags': [
                QueryCondSpec(ArrayCondition(op='|', negation=True),
                              params=['tag1', 'tag2']),
                QueryCondSpec(ArrayCondition(op='=', negation=False),
                              params='tag3')],
        }

    def test_handle(self):
        tokenized_query = ExperimentQueryManager.tokenize(self.query1)
        parsed_query = ExperimentQueryManager.parse(tokenized_query)
        built_query = ExperimentQueryManager.build(parsed_query)
        assert built_query == ExperimentQueryManager.handle_query(self.query1)

    @flaky(max_runs=3)
    def test_apply(self):
        result_queryset = ExperimentQueryManager.apply(query_spec=self.query1,
                                                       queryset=Experiment.objects)
        queries = [
            str(Experiment.objects.filter(
                updated_at__lte='2020-10-10'
            ).filter(
                started_at__gt='2010-10-10'
            ).filter(
                ~Q(started_at='2016-10-01')
            ).query),
            str(Experiment.objects.filter(
                started_at__gt='2010-10-10'
            ).filter(
                ~Q(started_at='2016-10-01')
            ).filter(
                updated_at__lte='2020-10-10'
            ).query),
            str(Experiment.objects.filter(
                ~Q(started_at='2016-10-01')
            ).filter(
                started_at__gt='2010-10-10'
            ).filter(
                updated_at__lte='2020-10-10'
            ).query),
        ]
        assert str(result_queryset.query) in queries

        result_queryset = ExperimentQueryManager.apply(query_spec=self.query2,
                                                       queryset=Experiment.objects)
        queries = [
            str(Experiment.objects.filter(
                metric__values__loss__lte=0.8
            ).filter(
                status__status__in=['starting', 'running']
            ).query),
            str(Experiment.objects.filter(
                status__status__in=['starting', 'running']
            ).filter(
                metric__values__loss__lte=0.8
            ).query)
        ]
        assert str(result_queryset.query) in queries

        result_queryset = ExperimentQueryManager.apply(query_spec=self.query4,
                                                       queryset=Experiment.objects)
        queries = [
            str(Experiment.objects.filter(
                ~Q(tags__overlap=['tag1', 'tag2'])
            ).filter(
                tags__contains=['tag3']
            ).query),
            str(Experiment.objects.filter(
                tags__contains=['tag3']
            ).filter(
                ~Q(tags__overlap=['tag1', 'tag2'])
            ).query)
        ]
        assert str(result_queryset.query) in queries
