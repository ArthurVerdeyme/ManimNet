"""Unit tests for the reusable helpers in `network_manim.graph_utils`.

These tests focus on *logic*, not rendered pixels, so they run quickly in CI.
"""
from itertools import combinations

from manim import Dot, Line

from network_manim.graph_utils import CustomDot, build_edge, build_clique


# --------------------------------------------------------------------------- #
#   CustomDot
# --------------------------------------------------------------------------- #

def test_customdot_numeric():
    """Passing a coordinate returns a regular Manim `Dot`."""
    dot = CustomDot([0, 0, 0])
    assert isinstance(dot, Dot)


def test_customdot_fallback_dot():
    """Unknown label falls back to a coloured `Dot` (no PNG available)."""
    dot = CustomDot("unknown_label")
    assert isinstance(dot, Dot)


# --------------------------------------------------------------------------- #
#   build_edge
# --------------------------------------------------------------------------- #

def test_build_edge_properties():
    node_a = CustomDot([0, 0, 0])
    node_b = CustomDot([2, 0, 0])
    edge = build_edge(node_a, node_b, color="RED", width=7)

    # The edge should be a `Line` connecting the two centres
    assert isinstance(edge, Line)
    assert all(edge.get_start() == node_a.get_center())
    assert all(edge.get_end() == node_b.get_center())
    assert edge.stroke_color == "RED"
    assert edge.stroke_width == 7


# --------------------------------------------------------------------------- #
#   build_clique
# --------------------------------------------------------------------------- #

def test_build_clique_edge_count():
    nodes = [CustomDot([i, 0, 0]) for i in range(4)]
    clique = build_clique(nodes)

    expected_edges = len(list(combinations(nodes, 2)))  # nC2
    assert len(clique) == expected_edges