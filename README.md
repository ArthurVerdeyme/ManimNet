### `README.md`
Below is the exact text you should paste into **README.md** — **do not** include any surrounding triple‑backtick lines.

<h1 align="center">ManimNet</h1>
<p align="center">
  <em>Your launch‑pad for building <strong>Manim</strong> animations that explain network‑science &amp; graph‑theory concepts.</em>
</p>

<p align="center">
  <a href="https://github.com/ArthurVerdeyme/ManimNet/actions?query=workflow%3ACI"><img src="https://img.shields.io/github/actions/workflow/status/ArthurVerdeyme/ManimNet/ci.yml?branch=main&amp;label=CI&amp;logo=github" alt="CI" /></a>
  <a href="https://pypi.org/project/manimnet/"><img src="https://img.shields.io/pypi/v/manimnet?logo=pypi" alt="PyPI" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License" /></a>
</p>

---

## 🌟 Why this repo?

If you’re a **researcher, educator, or student** who wants to turn abstract graph‑theory ideas into eye‑catching videos, **ManimNet** gives you:

| What you get            | What it covers                                                                                                                     |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| **Ready‑made scenes**   | • Community detection (Louvain / modularity)<br>• Common network topologies (star, ring, scale‑free, small‑world …)<br>• Adjacency‑matrix ↔ graph dual views<br>• Graph‑theoretic building blocks (paths, cycles, cliques, MST) |
| **Reusable helpers**    | `CustomDot`, `build_edge`, `build_clique`, colour palettes, image nodes                                                             |
| **Scaffold &amp; tests** | CI, pre‑commit hooks, pytest, docs skeleton                                                                                        |
| **CLI**                 | `mnet render &lt;scene&gt;` one‑liner rendering                                                                                        |

> **Goal:** shorten the time from *idea* → *high‑res MP4* so you can focus on the story rather than boilerplate.

---

## 🚀 Quick start

Install ManimNet (once published to PyPI) and render an example:

```bash
pip install manimnet
mnet render multi‑clique             # <— plays a community‑detection example