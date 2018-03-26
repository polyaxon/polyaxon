import copy


def get_independent_operations(dag):
    """Get a list of all operation in the graph with no dependencies."""
    ops = set(dag.keys())
    dependent_ops = set([op for downstream_ops in dag.values() for op in downstream_ops])
    return set(ops - dependent_ops)


def get_orphan_operations(dag):
    """Get orphan operations for given dag."""
    independent_operations = get_independent_operations(dag)
    return [operation for operation in independent_operations if not dag[operation]]


def has_dependencies(operation, dag):
    """Checks if the operation has dependencies."""
    for _, downstream_operations in dag.items():
        if operation in downstream_operations:
            return True
    return False


def sort_topologically(dag):
    """
    :return: a topological ordering of the DAG.
    :raise: an error if this is not possible (graph is not valid).
    """
    dag = copy.deepcopy(dag)
    sorted_ops = []
    independent_ops = get_independent_operations(dag)
    while independent_ops:
        op = independent_ops.pop()
        sorted_ops.append(op)
        downstream_ops = dag[op]
        while downstream_ops:
            downstream_op = downstream_ops.pop()
            if downstream_op not in dag:
                continue
            if not has_dependencies(downstream_op, dag):
                independent_ops.add(downstream_op)

    if len(sorted_ops) != len(dag.keys()):
        raise ValueError('graph is not acyclic')
    return sorted_ops
