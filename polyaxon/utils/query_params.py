def get_query_params(limit=None, offset=None, query=None, sort=None):
    params = {}
    if limit:
        params["limit"] = limit
    if offset:
        params["offset"] = offset
    if query:
        params["query"] = query
    if sort:
        params["sort"] = sort

    return params
