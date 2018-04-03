import copy
from collections import deque


def get_dag(nodes, downstream_fn):
    """Return a dag representation of the nodes passed.

    This is equally used for pipelines and pipeline runs.

    Params:
        nodes: an instance of `Operation` | `OperationRun` the nodes to represent en dag.
        downstream_fn: a function that returns the downstream nodes of the a node.

    Returns:
         tuple: (dag, dict(node_id: node))
    """
    dag = {}
    node_by_ids = {}
    for node in nodes:
        downstream_ops = downstream_fn(node)
        dag[node.id] = set(downstream_ops)
        node_by_ids[node.id] = node

    return dag, node_by_ids


def get_independent_nodes(dag):
    """Get a list of all node in the graph with no dependencies."""
    nodes = set(dag.keys())
    dependent_nodes = set([node for downstream_nodes in dag.values() for node in downstream_nodes])
    return set(nodes - dependent_nodes)


def get_orphan_nodes(dag):
    """Get orphan nodes for given dag."""
    independent_nodes = get_independent_nodes(dag)
    return set([node for node in independent_nodes if not dag[node]])


def has_dependencies(node, dag):
    """Checks if the node has dependencies."""
    for downstream_nodes in dag.values():
        if node in downstream_nodes:
            return True
    return False


def sort_topologically(dag):
    """Sort the dag breath first topologically.

    Only the nodes inside the dag are returned, i.e. the nodes that are also keys.

    Returns:
         a topological ordering of the DAG.
    Raises:
         an error if this is not possible (graph is not valid).
    """
    dag = copy.deepcopy(dag)
    sorted_nodes = []
    independent_nodes = deque(get_independent_nodes(dag))
    while independent_nodes:
        node = independent_nodes.popleft()
        sorted_nodes.append(node)
        # this alters the dag so that we are sure we are visiting the nodes only once
        downstream_nodes = dag[node]
        while downstream_nodes:
            downstream_node = downstream_nodes.pop(0)
            if downstream_node not in dag:
                continue
            if not has_dependencies(downstream_node, dag):
                independent_nodes.append(downstream_node)

    if len(sorted_nodes) != len(dag.keys()):
        raise ValueError('graph is not acyclic')
    return sorted_nodes
