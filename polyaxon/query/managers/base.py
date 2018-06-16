from query.builder import QueryCondSpec
from query.exceptions import QueryError
from query.parser import parse_field, tokenize_query


class BaseQueryManager(object):
    NAME = None
    FIELDS_PROXY = {}
    PARSERS_BY_FIELD = {}
    CONDITIONS_BY_FIELD = {}

    @classmethod
    def proxy_field(cls, field):
        field, suffix = parse_field(field)
        if field in cls.FIELDS_PROXY:
            field = cls.FIELDS_PROXY[field]
            return '{}__{}'.format(field, suffix) if suffix else field
        return field

    @classmethod
    def tokenize(cls, query_spec):
        tokenized_query = tokenize_query(query_spec)
        for key in tokenized_query.keys():
            field, _ = parse_field(key)
            if field and (field not in cls.PARSERS_BY_FIELD or
                          field not in cls.CONDITIONS_BY_FIELD):
                raise QueryError('key `{}` is not supported by query manager `{}`.'.format(
                    key, cls.NAME
                ))
        return tokenized_query

    @classmethod
    def parse(cls, tokenized_query):
        parsed_query = {}
        for key, expressions in tokenized_query.items():
            field, _ = parse_field(key)
            parsed_query[key] = [cls.PARSERS_BY_FIELD[field](exp) for exp in expressions]
        return parsed_query

    @classmethod
    def build(cls, parsed_query):
        built_query = {}
        for key, operations in parsed_query.items():
            field, _ = parse_field(key)
            built_query[key] = [
                QueryCondSpec(
                    cond=cls.CONDITIONS_BY_FIELD[field](op=op_spec.op, negation=op_spec.negation),
                    params=op_spec.params)
                for op_spec in operations]
        return built_query

    @classmethod
    def handle_query(cls, query_spec):
        tokenized_query = cls.tokenize(query_spec=query_spec)
        parsed_query = cls.parse(tokenized_query=tokenized_query)
        built_query = cls.build(parsed_query=parsed_query)
        return built_query

    @classmethod
    def apply(cls, query_spec, queryset):
        built_query = cls.handle_query(query_spec=query_spec)
        for key, cond_specs in built_query.items():
            key = cls.proxy_field(key)
            for cond_spec in cond_specs:
                queryset = cond_spec.cond.apply(
                    queryset=queryset, name=key, params=cond_spec.params)

        return queryset
