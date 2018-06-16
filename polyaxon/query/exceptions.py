class QueryError(Exception):
    pass


class QueryConditionException(QueryError):
    pass


class QueryParserException(QueryError):
    pass
