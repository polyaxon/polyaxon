import pytest

from query.parser import (
    QueryParserException,
    parse_expression,
    parse_datetime_operation,
    parse_negation_operation,
    parse_scalar_operation,
    parse_value_operation,
    split_query,
    tokenize_query)
from tests.utils import BaseTest


@pytest.mark.conditions_mark
class TestParser(BaseTest):
    DISABLE_RUNNER = True

    def test_base_parser_raises_for_invalid_expressions(self):
        with self.assertRaises(QueryParserException):
            parse_expression('foo:bar:moo')

        with self.assertRaises(QueryParserException):
            parse_expression('foo')

        with self.assertRaises(QueryParserException):
            parse_expression(None)

        with self.assertRaises(QueryParserException):
            parse_expression(12)

        with self.assertRaises(QueryParserException):
            parse_expression('fff:')

        with self.assertRaises(QueryParserException):
            parse_expression(':dsf')

        with self.assertRaises(QueryParserException):
            parse_expression(':')

    def test_base_parser_passes_for_valid_expressions(self):
        assert parse_expression('foo:bar') == ('foo', 'bar')
        assert parse_expression('foo:>=bar') == ('foo', '>=bar')
        assert parse_expression('foo:bar|moo|boo') == ('foo', 'bar|moo|boo')
        assert parse_expression('foo:bar..moo') == ('foo', 'bar..moo')
        assert parse_expression('foo:!bar') == ('foo', '!bar')

        # Handles spaces
        assert parse_expression(' foo: bar ') == ('foo', 'bar')
        assert parse_expression('foo :>=bar ') == ('foo', '>=bar')
        assert parse_expression(' foo :bar|moo|boo') == ('foo', 'bar|moo|boo')
        assert parse_expression(' foo : bar..moo ') == ('foo', 'bar..moo')
        assert parse_expression(' foo : !bar ') == ('foo', '!bar')

    def test_parse_negation_operation(self):
        assert parse_negation_operation('foo') == (False, 'foo')
        assert parse_negation_operation('!foo') == (True, 'foo')
        assert parse_negation_operation('foo..boo') == (False, 'foo..boo')
        assert parse_negation_operation('!foo..boo') == (True, 'foo..boo')
        assert parse_negation_operation('>=foo') == (False, '>=foo')
        assert parse_negation_operation('!>=foo') == (True, '>=foo')
        assert parse_negation_operation('foo|boo') == (False, 'foo|boo')
        assert parse_negation_operation('!foo|boo') == (True, 'foo|boo')
        assert parse_negation_operation(' ! >=foo ') == (True, '>=foo')
        assert parse_negation_operation(' foo|boo ') == (False, 'foo|boo')
        assert parse_negation_operation('! foo|boo') == (True, 'foo|boo')

    def test_parse_datetime_operation(self):
        # Raises for not allowed operators
        with self.assertRaises(QueryParserException):
            parse_datetime_operation('foo|bar')

        with self.assertRaises(QueryParserException):
            parse_datetime_operation('')

        with self.assertRaises(QueryParserException):
            parse_datetime_operation('!')

        with self.assertRaises(QueryParserException):
            parse_datetime_operation('..')

        with self.assertRaises(QueryParserException):
            parse_datetime_operation('..da')

        with self.assertRaises(QueryParserException):
            parse_datetime_operation('asd..')

        with self.assertRaises(QueryParserException):
            parse_datetime_operation('asd..asd..asd')

        # Parses ranges
        assert parse_datetime_operation('foo..bar') == (
            '..', False, ['foo', 'bar'])
        assert parse_datetime_operation(' foo .. bar ') == (
            '..', False, ['foo', 'bar'])
        assert parse_datetime_operation('! foo .. bar ') == (
            '..', True, ['foo', 'bar'])

        # Comparison
        assert parse_datetime_operation('>=foo') == (
            '>=', False, 'foo')
        assert parse_datetime_operation(' ! <= bar ') == (
            '<=', True, 'bar')
        assert parse_datetime_operation('! > bar ') == (
            '>', True, 'bar')

        # Equality
        assert parse_datetime_operation('foo') == (
            '=', False, 'foo')
        assert parse_datetime_operation(' !  bar ') == (
            '=', True, 'bar')
        assert parse_datetime_operation('!bar') == (
            '=', True, 'bar')

    def test_parse_scalar_operation(self):
        # Raises for not allowed operators
        with self.assertRaises(QueryParserException):
            parse_scalar_operation('1|12')

        with self.assertRaises(QueryParserException):
            parse_scalar_operation('0.1..0.2')

        # Raise for not scalars
        with self.assertRaises(QueryParserException):
            parse_scalar_operation('>=f')

        with self.assertRaises(QueryParserException):
            parse_scalar_operation(' ! <=f1 ')

        with self.assertRaises(QueryParserException):
            parse_scalar_operation('! > bbb ')

        with self.assertRaises(QueryParserException):
            parse_datetime_operation('')

        with self.assertRaises(QueryParserException):
            parse_datetime_operation('!')

        with self.assertRaises(QueryParserException):
            parse_datetime_operation('>')

        # Comparison
        assert parse_scalar_operation('>=1') == (
            '>=', False, 1)
        assert parse_scalar_operation(' ! <= 0.1 ') == (
            '<=', True, 0.1)
        assert parse_scalar_operation('! > 20 ') == (
            '>', True, 20)

        # Equality
        assert parse_scalar_operation('1') == (
            '=', False, 1)
        assert parse_scalar_operation(' !  2 ') == (
            '=', True, 2)
        assert parse_scalar_operation('!0.1') == (
            '=', True, 0.1)

    def test_parse_value_operation(self):
        # Raises for not allowed operators
        with self.assertRaises(QueryParserException):
            parse_value_operation('0.1..0.2')

        with self.assertRaises(QueryParserException):
            parse_datetime_operation('')

        with self.assertRaises(QueryParserException):
            parse_datetime_operation('!')

        # Raises for comparison
        with self.assertRaises(QueryParserException):
            parse_value_operation('>=f')

        with self.assertRaises(QueryParserException):
            parse_value_operation(' ! <=f1 ')

        with self.assertRaises(QueryParserException):
            parse_value_operation('!|')

        with self.assertRaises(QueryParserException):
            parse_value_operation('|')

        with self.assertRaises(QueryParserException):
            parse_value_operation('!tag1 |')

        # Equality
        assert parse_value_operation('tag') == (
            '=', False, 'tag')
        assert parse_value_operation(' !  tag ') == (
            '=', True, 'tag')
        assert parse_value_operation('!tag') == (
            '=', True, 'tag')

        # In op
        assert parse_value_operation('tag1|tag2') == (
            '|', False, ['tag1', 'tag2'])
        assert parse_value_operation(' !  tag1|tag2 ') == (
            '|', True, ['tag1', 'tag2'])
        assert parse_value_operation('!tag1 | tag2| tag23') == (
            '|', True, ['tag1', 'tag2', 'tag23'])

    def test_split_query(self):
        with self.assertRaises(QueryParserException):
            split_query('')

        with self.assertRaises(QueryParserException):
            split_query(',')

        with self.assertRaises(QueryParserException):
            split_query(', , ')

        assert len(split_query('name:!tag1 | tag2| tag23')) == 1
        assert len(split_query('name:!tag1 | tag2| tag23, name2:foo')) == 2

    def test_tokenize_query(self):
        with self.assertRaises(QueryParserException):
            tokenize_query('')

        with self.assertRaises(QueryParserException):
            tokenize_query(',')

        with self.assertRaises(QueryParserException):
            tokenize_query(', , ')

        assert tokenize_query('name:!tag1 | tag2| tag23') == {'name': ['!tag1 | tag2| tag23']}
        assert tokenize_query('name1:!tag1 | tag2| tag23, name1:foo, name2:sdf..dsf') == {
            'name1': ['!tag1 | tag2| tag23', 'foo'],
            'name2': ['sdf..dsf']
        }
