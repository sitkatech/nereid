import itertools
import string
import copy

import pytest
import networkx as nx


def _construct_graph_objs():

    graphs = []
    for graph_type in [nx.Graph, nx.MultiGraph, nx.DiGraph, nx.MultiDiGraph]:
        g1 = nx.from_edgelist(
            [("2", "1"), ("3", "1"), ("1", "0")], create_using=graph_type
        )

        g2 = g1.copy()
        attrs = {
            n: {l: i} for i, (n, l) in enumerate(zip(g2.nodes, string.ascii_lowercase))
        }
        nx.set_node_attributes(g2, attrs)

        g3 = copy.deepcopy(g2)
        attrs = {
            e: {l: i} for i, (e, l) in enumerate(zip(g2.edges, string.ascii_lowercase))
        }
        nx.set_edge_attributes(g3, attrs)

        graphs.extend([(g1, True), (g2, True), (g3, True)])

    graphs.extend(
        [
            # one out edge; these are 'valid' in `nereid`
            (nx.gn_graph(25, seed=42), True),
            # many out edges; these are not 'valid' in `nereid`
            (nx.gnc_graph(25, seed=42), False),
        ]
    )
    return graphs


@pytest.fixture(params=_construct_graph_objs())
def graph_obj_isvalid(request):
    yield request.param


def _construct_graph_dicts():

    dicts = []

    for directed, multigraph in itertools.product([True, False], [True, False]):

        g1 = {
            "directed": directed,
            "multigraph": multigraph,
            "edges": [
                {"source": "A", "target": "B"},
                {"source": "C", "target": "B"},
                {"source": "B", "target": "D"},
            ],
        }

        if not directed:
            # hack to make sure undirected graphs have their edges sorted
            # prior to graph creation. this is because networkx internally
            # coerces edges defined as ['c', 'a'] into the _ordered_ variant
            # ['a', 'c'] if the graph is not directed. This is annoying, I know.
            oe = [
                {
                    "source": sorted([e["source"], e["target"]])[0],
                    "target": sorted([e["source"], e["target"]])[1],
                }
                for e in g1["edges"]
            ]
            g1["edges"] = [dict(e, **oe) for e, oe in zip(g1["edges"], oe)]

        for dct in g1["edges"]:
            dct["metadata"] = {}

        if multigraph:
            for dct in g1["edges"]:
                dct["metadata"]["key"] = 0

        g2 = copy.deepcopy(g1)

        g2["nodes"] = [{"id": "A"}, {"id": "B"}, {"id": "C"}, {"id": "D"}]

        for i, (dct, l) in enumerate(zip(g2["nodes"], string.ascii_lowercase)):
            dct["metadata"] = {}
            dct["metadata"][l] = i

        g3 = copy.deepcopy(g2)
        for i, (dct, l) in enumerate(zip(g3["edges"], string.ascii_lowercase)):
            dct["metadata"][l] = i

        g4 = copy.deepcopy(g3)
        for i, (dct, l) in enumerate(zip(g4["edges"], string.ascii_lowercase)):
            dct["metadata"][l] = {i: copy.deepcopy(dct["metadata"])}

        dicts.extend([(g1, True), (g2, True), (g3, True), (g4, True)])

    return dicts


@pytest.fixture(params=_construct_graph_dicts())
def graph_dict_isvalid(request):
    yield request.param


@pytest.fixture
def subgraph_request_dict():
    graph = {
        "graph": {
            "directed": True,
            "edges": [
                {"source": "3", "target": "1"},
                {"source": "5", "target": "3"},
                {"source": "7", "target": "1"},
                {"source": "9", "target": "1"},
                {"source": "11", "target": "1"},
                {"source": "13", "target": "3"},
                {"source": "15", "target": "9"},
                {"source": "17", "target": "7"},
                {"source": "19", "target": "17"},
                {"source": "21", "target": "15"},
                {"source": "23", "target": "1"},
                {"source": "25", "target": "5"},
                {"source": "27", "target": "11"},
                {"source": "29", "target": "7"},
                {"source": "31", "target": "11"},
                {"source": "33", "target": "25"},
                {"source": "35", "target": "23"},
                {"source": "4", "target": "2"},
                {"source": "6", "target": "2"},
                {"source": "8", "target": "6"},
                {"source": "10", "target": "2"},
                {"source": "12", "target": "2"},
                {"source": "14", "target": "2"},
                {"source": "16", "target": "12"},
                {"source": "18", "target": "12"},
                {"source": "20", "target": "8"},
                {"source": "22", "target": "6"},
                {"source": "24", "target": "12"},
            ],
        },
        "nodes": [{"id": "3"}, {"id": "29"}, {"id": "18"}],
    }

    return graph
