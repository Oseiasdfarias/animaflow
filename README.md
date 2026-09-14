# animaflow (animaflow.io)

> **Declarative, animated architecture flowcharts & diagrams in Python.**  
> Design clean, modern system flows once — render to **Manim** (MP4, GIF), **Web Canvas/SVG** (HTML preview), or export for **Remotion**.

[![PyPI version](https://img.shields.io/badge/pypi-animaflow-blue.svg)](https://pypi.org/project/animaflow/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

---

## 🚀 Why animaflow?

Creating animated system architecture diagrams for **LinkedIn**, **YouTube Shorts**, and **Technical Talks** usually requires:
- Handcrafting hundreds of lines of coordinate geometry in Manim or After Effects, or
- Using static diagram generators (Graphviz, Diagrams) with zero motion or storytelling capabilities.

**animaflow** solves this by separating **semantic flow definition** from **rendering engines**:
1. Define nodes, edges, labels and timeline actions in Python.
2. Animate packets travelling between services, state mutations, and system pulses declaratively.
3. Export to **Manim** (seamless video), **Interactive HTML/SVG Canvas** or **Remotion JSON**.

---

## 📦 Installation

```bash
# Core package
pip install animaflow

# With Manim video rendering support
pip install "animaflow[manim]"

# With interactive Web Canvas / SVG exporter
pip install "animaflow[web]"

# Full installation
pip install "animaflow[all]"
```

---

## ⚡ Quick Start

```python
import animaflow as af

# 1. Declare the Flow Diagram
flow = af.Flow(title="LLM Production Architecture", theme=af.themes.DarkTerminal)

usr = flow.add_node("User Client", icon="user", subtitle="Web / Mobile")
app = flow.add_node("API Gateway", icon="server", subtitle="FastAPI")
cfg = flow.add_node("Prompt Engine", icon="settings", subtitle="Langfuse v3")
llm = flow.add_node("LLM Service", icon="cpu", subtitle="Claude / GPT-4")

# 2. Connect with Edges
flow.connect(usr, app, label="POST /chat")
flow.connect(app, cfg, label="get_prompt()")
flow.connect(app, llm, label="stream completion")

# 3. Define the Animation Storyline
flow.timeline.reveal_sequence(delay=0.3)
flow.timeline.send_packet(from_node=usr, to_node=app, label="query payload")
flow.timeline.send_packet(from_node=app, to_node=cfg, label="lookup v3")
flow.timeline.highlight_node(cfg, status="accent")
flow.timeline.send_packet(from_node=app, to_node=llm)

# 4. Render to Manim or Export to Web
# In a Manim scene:
# flow.render_manim(self)
```

---

## 🛣️ Roadmap

- [x] Python Core Schema & Semantic Flow DSL
- [x] Auto-Layout engine (Horizontal, Vertical, Grid)
- [x] Manim Renderer Driver (MP4/GIF ready)
- [ ] Standalone HTML5 Canvas / SVG interactive preview
- [ ] React Flow / Remotion JSON bridge
- [ ] Visual Drag-and-Drop Web Builder on `animaflow.io`

---

## 📄 License

MIT License © 2026 [Oséias Farias](https://github.com/Oseiasdfarias)

