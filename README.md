<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Oseiasdfarias/animaflow/main/docs/assets/readme/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Oseiasdfarias/animaflow/main/docs/assets/readme/banner-light.svg">
  <img alt="animaflow: animated architecture diagrams, written as code" src="https://raw.githubusercontent.com/Oseiasdfarias/animaflow/main/docs/assets/readme/banner-dark.svg" width="100%">
</picture>

<a href="https://pypi.org/project/animaflow/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/animaflow?style=flat-square&labelColor=141416&color=d4885a&logo=pypi&logoColor=d4885a"/></a>
<a href="https://pypi.org/project/animaflow/"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/animaflow?style=flat-square&labelColor=141416&color=d4885a&logo=python&logoColor=d4885a"/></a>
<a href="https://oseiasdfarias.github.io/animaflow/"><img alt="Docs" src="https://img.shields.io/badge/docs-online-d4885a?style=flat-square&labelColor=141416&logo=materialformkdocs&logoColor=d4885a"/></a>
<a href="https://github.com/Oseiasdfarias/animaflow/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-d4885a?style=flat-square&labelColor=141416"/></a>

**English** · [Português](https://github.com/Oseiasdfarias/animaflow/blob/main/README.pt-BR.md)

</div>

## Gallery

<table>
  <tr>
    <td width="33%"><img src="https://raw.githubusercontent.com/Oseiasdfarias/animaflow/main/docs/assets/event_driven_pipeline_stream.gif" alt="Event-driven pipeline with a continuous stream"></td>
    <td width="33%"><img src="https://raw.githubusercontent.com/Oseiasdfarias/animaflow/main/docs/assets/multi_agent_swarm.png" alt="Multi-agent swarm orchestration"></td>
    <td width="33%"><img src="https://raw.githubusercontent.com/Oseiasdfarias/animaflow/main/docs/assets/rag_pipeline.png" alt="RAG retrieval pipeline"></td>
  </tr>
  <tr>
    <td align="center"><sub><b>Continuous stream</b>: particles flowing in real time</sub></td>
    <td align="center"><sub><b>Multi-agent swarm</b>: layered orchestration DAG</sub></td>
    <td align="center"><sub><b>RAG pipeline</b>: retrieval and LLM architecture</sub></td>
  </tr>
</table>

## Why animaflow?

Architecture diagrams for **LinkedIn and X posts**, **technical videos** and **talks** usually force a bad choice:

- write hundreds of lines of geometry, absolute coordinates and updaters in Manim or After Effects, **or**
- use static generators (Graphviz, PlantUML, Diagrams) with no motion, no pacing and no data moving through the system.

**animaflow** separates **what the flow is** from **how it is rendered**:

1. **Declare nodes and connections** in a small Python DSL: services, databases, labels and metadata.
2. **Let the layout engine arrange them** in rows, columns or DAG layers, with spacing that avoids overlaps.
3. **Script the story on a timeline**: reveal nodes, send packets, stream particles, highlight a step.
4. **Render to several backends**: **Manim CE** (MP4 and GIF) or a self-contained **interactive HTML/SVG** page.

## How it works

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Oseiasdfarias/animaflow/main/docs/assets/readme/pipeline-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Oseiasdfarias/animaflow/main/docs/assets/readme/pipeline-light.svg">
  <img alt="animaflow architecture: declare, arrange and animate, render" src="https://raw.githubusercontent.com/Oseiasdfarias/animaflow/main/docs/assets/readme/pipeline-dark.svg" width="100%">
</picture>

| Module | What it does | Built with |
| --- | --- | --- |
| **Flow core** (`core.flow`) | Graph topology, node metadata, connectors and visual parameters | Pure Python, dataclasses |
| **Layout engine** (`core.layout`) | Automatic arrangement (horizontal, vertical, layered DAG) with minimum widths and spacing | Graph layout algorithms |
| **Timeline engine** (`core.timeline`) | Time-based actions: `reveal`, `send_packet`, `stream_packets`, `highlight_node`, `wait` | Declarative event engine |
| **Manim backend** (`backends.manim`) | Turns nodes and edges into vector Mobjects with clean typography and renders the scene | Manim Community Edition |
| **Web backend** (`backends.web`) | Generates standalone interactive HTML/SVG with a particle simulation in plain JavaScript | Native SVG + ES6 |

## Installation

```bash
pip install animaflow
```

To render animations with Manim:

```bash
pip install "animaflow[manim]"
```

Video rendering with Manim also needs FFmpeg installed on the system.

## Quick example

```python
import animaflow as af

flow = af.Flow(title="Order pipeline")
api = flow.add_node("API", subtitle="Receives orders")
worker = flow.add_node("Worker", subtitle="Processes events")
database = flow.add_node("Database", subtitle="Stores results")

flow.connect(api, worker, label="event")
flow.connect(worker, database, label="persist")
flow.auto_layout(mode="horizontal")
flow.timeline.reveal_sequence(delay_per_item=0.3)
flow.export_html("pipeline.html")
```

Open `pipeline.html` in any browser.

## Ready-made examples

All demo scripts live in the [examples folder](https://github.com/Oseiasdfarias/animaflow/tree/main/examples).

| Example | Description | How to run |
| --- | --- | --- |
| [`event_driven_pipeline.py`](https://github.com/Oseiasdfarias/animaflow/blob/main/examples/event_driven_pipeline.py) | Event pipeline with a continuous animation | `manim -qm examples/event_driven_pipeline.py EventDrivenPipelineAnimation` |
| [`multi_agent_swarm.py`](https://github.com/Oseiasdfarias/animaflow/blob/main/examples/multi_agent_swarm.py) | Layered multi-agent orchestration | `manim -qm examples/multi_agent_swarm.py AgentSwarmAnimation` |
| [`rag_pipeline_manim.py`](https://github.com/Oseiasdfarias/animaflow/blob/main/examples/rag_pipeline_manim.py) | RAG pipeline rendered with Manim | `manim -qm examples/rag_pipeline_manim.py RAGFlowAnimation` |
| [`rag_pipeline_web.py`](https://github.com/Oseiasdfarias/animaflow/blob/main/examples/rag_pipeline_web.py) | Export to interactive HTML/SVG | `python examples/rag_pipeline_web.py` |

## License

MIT. See the [license file](https://github.com/Oseiasdfarias/animaflow/blob/main/LICENSE).

Built by **[Oséias Farias](https://github.com/Oseiasdfarias)**.
