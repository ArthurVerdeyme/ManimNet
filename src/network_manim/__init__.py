"""Top‑level package for Network‑Manim."""
from importlib.metadata import version as _v
__version__ = _v("network-manim", default="0.0.0")

# Public API
from .scenes.multi_clique import MultiCliqueAnimated7  # noqa: F401