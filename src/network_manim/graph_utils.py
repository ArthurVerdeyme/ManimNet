"""Shared helper functions extracted from the monolith."""
from __future__ import annotations

import os
import numpy as np

import itertools
from pathlib import Path
from typing import Sequence

from functools import lru_cache

from manim import (
    Dot,
    FadeIn,
    FadeOut,
    Group,
    ImageMobject,
    Line,
    Scene,
    VGroup,
)
from .config import EDGE_WIDTH, NODE_RADIUS_IMAGE, COLORS

# --------------------------------------------------------------------------- #
#   Assets directory – PNGs named exactly like node labels
# --------------------------------------------------------------------------- #
_ASSETS_DIR = Path(__file__).with_suffix("").parent / "assets"


def circular_image_node(label: str, radius: float = NODE_RADIUS_IMAGE) -> ImageMobject:
    """Return a circular node wrapping ``assets/{label}.png`` (fallback Dot)."""
    path = _ASSETS_DIR / f"{label}.png"
    if path.exists():
        img = ImageMobject(str(path), z_index=1)
        img.height = 2 * radius
        # thin stroke so edges overlap neatly
        img.set_stroke(width=1, opacity=1)
        return img

    # Fallback – plain dot with colour from the palette or white
    return Dot(radius=radius, color=COLORS.get(label, "WHITE"), z_index=1)


def replace_dot_list(dot_list, replacement_map):
    new_list = []
    for dot in dot_list:
        for old, new in replacement_map.items():
            if np.allclose(dot.get_center(), old.get_center()):
                new_list.append(new)
                break
        else:
            new_list.append(dot)
    return new_list


# Keep a reference to the original Dot for fallback
OriginalDot = Dot

def CustomDot(label_or_pos, **kwargs):
    if isinstance(label_or_pos, str):
        return circular_image_node(label_or_pos, radius=kwargs.get("radius", NODE_RADIUS_IMAGE))
    return OriginalDot(label_or_pos, **kwargs)


def build_edge(
    n1: VGroup,
    n2: VGroup,
    *,
    color: str = "WHITE",
    width: float = EDGE_WIDTH,
    buff: float | None = None,
) -> Line:
    """Return a straight edge connecting centers of *n1* and *n2*."""
    line = Line(
        n1.get_center(),
        n2.get_center(),
        buff=buff if buff is not None else n1.width * 0.5,
        stroke_color=color,
        stroke_width=width,
        z_index=0,
    )
    return line


def build_clique(
    nodes: Sequence[VGroup],
    *,
    color: str = "WHITE",
    width: float = EDGE_WIDTH,
) -> VGroup:
    """Fully connect *nodes* and return the :class:`~manim.mobject.types.VGroup` of edges."""
    edges = VGroup(
        *(build_edge(a, b, color=color, width=width) for a, b in itertools.combinations(nodes, 2))
    )
    return edges


# --------------------------------------------------------------------------- #
#   Tiny animation helpers
# --------------------------------------------------------------------------- #

def fade_in_group(scene: Scene, mob: VGroup | Group, **kwargs):
    """Play a :class:`~manim.animation.transform.FadeIn` for *mob* immediately."""
    scene.play(FadeIn(mob, **kwargs))


def fade_out_group(scene: Scene, mob: VGroup | Group, **kwargs):
    scene.play(FadeOut(mob, **kwargs))