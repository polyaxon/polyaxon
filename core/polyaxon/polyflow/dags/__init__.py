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

from collections import namedtuple

from polyaxon.exceptions import PolyaxonSchemaError


class DagOpSpec(namedtuple("DagOpSpec", "op upstream downstream")):
    def items(self):
        return self._asdict().items()

    def set_op(self, op):
        return self._replace(op=op)


def set_dag_op(dag, op_id, op=None, upstream=None, downstream=None):
    upstream = set(upstream) if upstream else set([])
    downstream = set(downstream) if downstream else set([])
    if op_id in dag:
        if op and dag[op_id].op is None:
            dag[op_id] = dag[op_id].set_op(op)
        dag[op_id].upstream.update(upstream)
        dag[op_id].downstream.update(downstream)
    else:
        dag[op_id] = DagOpSpec(op=op, upstream=upstream, downstream=downstream)

    return dag


def process_op(dag, op, upstream):
    set_dag_op(dag=dag, op_id=op.id, op=op, upstream=upstream, downstream=None)
    for op_upstream in upstream:
        dag = set_dag_op(dag=dag, op_id=op_upstream, downstream=[op.id])

    return dag


def process_dag(ops):
    dag = {}
    for op, upstream in ops:
        dag = process_op(dag, op, upstream=upstream)

    return dag


def get_independent_ops(dag):
    """Get a list of all node in the graph with no dependencies."""
    ops = set(dag.keys())
    dependent_nodes = {
        op_downstream for op in dag.values() for op_downstream in op.downstream
    }
    return ops - dependent_nodes


def has_dependencies(op, dag):
    """Checks if the node has dependencies."""
    for op_spec in dag.values():
        if op in op_spec.downstream:
            return True
    return False


def get_orphan_ops(dag):
    """Get orphan ops for given dag."""
    independent_ops = get_independent_ops(dag)
    return {op for op in independent_ops if dag[op].op is None}


def sort_topologically(dag, flatten=False):
    """Sort the dag breath first topologically.

    Only the nodes inside the dag are returned, i.e. the nodes that are also keys.

    Returns:
         a topological ordering of the DAG.
    Raises:
         an error if this is not possible (graph is not valid).
    """

    def _get_independent_ops():
        if current_independent_ops:
            return current_independent_ops.pop()
        current_independent_ops.update(next_independent_ops)
        next_independent_ops.clear()
        sorted_ops.append(current_sorted_ops[:])
        del current_sorted_ops[:]  # in python3 it should use .clear()
        if current_independent_ops:
            return current_independent_ops.pop()

    visited_ops = set()
    next_independent_ops = set()
    current_sorted_ops = []
    sorted_ops = []
    current_independent_ops = get_independent_ops(dag)
    op = _get_independent_ops()
    while op is not None:
        current_sorted_ops.append(op)
        visited_ops.add(op)
        downstream_ops = dag[op].downstream.copy()
        while downstream_ops:
            downstream_op = downstream_ops.pop()

            if downstream_op not in dag:
                continue

            if downstream_op in visited_ops:
                continue

            if not dag[downstream_op].upstream - visited_ops:
                next_independent_ops.add(downstream_op)

        op = _get_independent_ops()

    flatten_sorted_ops = [i for il in sorted_ops for i in il]
    if len(flatten_sorted_ops) != len(dag.keys()):
        raise PolyaxonSchemaError("Pipeline's graph is not acyclic.")
    return flatten_sorted_ops if flatten else sorted_ops
