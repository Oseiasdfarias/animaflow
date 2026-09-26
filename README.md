![animaflow](https://raw.githubusercontent.com/Oseiasdfarias/animaflow/main/brand/png/logo-horizontal-solido-800.png)

<p align="center">
  <strong>Diagramas e fluxogramas de arquitetura declarativos, animados e programáveis em Python</strong><br>
  <sub>Modele fluxos uma vez e exporte para HTML/SVG interativo ou animações com Manim</sub>
</p>

<p align="center">
  <a href="https://pypi.org/project/animaflow/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/animaflow"/></a>
  <a href="https://pypi.org/project/animaflow/"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/animaflow"/></a>
  <a href="https://github.com/Oseiasdfarias/animaflow/blob/main/LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-green.svg"/></a>
</p>

---

## Galeria & Exemplos

<table>
  <tr>
    <td width="33%"><img src="https://raw.githubusercontent.com/Oseiasdfarias/animaflow/main/docs/assets/event_driven_pipeline_stream.gif" alt="Event-Driven Pipeline com Continuous Stream"></td>
    <td width="33%"><img src="https://raw.githubusercontent.com/Oseiasdfarias/animaflow/main/docs/assets/multi_agent_swarm.png" alt="Multi-Agent Swarm Orchestration"></td>
    <td width="33%"><img src="https://raw.githubusercontent.com/Oseiasdfarias/animaflow/main/docs/assets/rag_pipeline.png" alt="RAG Retrieval Pipeline"></td>
  </tr>
  <tr>
    <td align="center"><sub><b>Streaming Contínuo</b> — fluxo em tempo real de partículas</sub></td>
    <td align="center"><sub><b>Multi-Agent Swarm</b> — DAG de orquestração em camadas</sub></td>
    <td align="center"><sub><b>RAG Pipeline</b> — arquitetura de busca e LLM</sub></td>
  </tr>
</table>

---

## Por que o animaflow?

Criar diagramas de arquitetura de software para **redes profissionais (LinkedIn, X/Twitter)**, **vídeos técnicos (YouTube, Reels)** e **apresentações corporativas** geralmente exige:
- Escrever centenas de linhas manuais de geometria, coordenadas absolutas e updaters no Manim ou After Effects, **ou**
- Usar geradores estáticos (Graphviz, PlantUML, Diagrams) sem qualquer suporte a movimento, ritmo narrativo ou pulso de dados.

O **animaflow** resolve isso separando a **definição semântica do fluxo** dos **motores de renderização**:
1. **Declare Nós e Conexões**: especifique nós, serviços, banco de dados, labels e metadados via DSL simples em Python.
2. **Auto-Layout Inteligente**: organize automaticamente nós em camadas (DAGs), colunas ou sequências horizontais/verticais com alinhamento e margens dinâmicas anti-sobreposição.
3. **Timeline Narrativa**: anime pacotes individuais, streams contínuos de partículas, transições de estado e realces de nós de forma declarativa.
4. **Múltiplos Backends**: exporte diretamente para **Manim CE** (vídeos MP4 e GIFs em alta definição) e **HTML/Web Canvas interativo**.

---

## Como funciona a arquitetura

O núcleo do **animaflow** é modular e extensível:

| Módulo / Subsistema | O que faz | Tecnologia / Detalhes |
| --- | --- | --- |
| **Flow Core** (`core.flow`) | Armazena a topologia do grafo, metadados dos nós, conectores e parâmetros visuais | Python Puro / Dataclasses |
| **Layout Engine** (`core.layout`) | Algoritmos de arranjo automático (horizontal, vertical, empilhamento em camadas DAG) calculando larguras mínimas e espaçamento | Algoritmos de layout de grafos |
| **Timeline Engine** (`core.timeline`) | Orquestra as ações temporais: sequências de aparição (`reveal`), envio de pacotes (`send_packet`), streams contínuos (`stream_packets`), realces (`highlight_node`) e esperas (`wait`) | Motor declarativo de eventos |
| **Manim Backend** (`backends.manim`) | Converte nós e conexões em Mobjects vetoriais modernos com tipografia refinada, sombras sutis, badges de subtítulo e renderiza a cena | Manim Community Edition (CE) |
| **Web Canvas Backend** (`backends.web`) | Gera código HTML/SVG independente e interativo com simulação física de partículas em JavaScript puro | SVG nativo + ES6 Vanilla JS |

---

## Instalação

```bash
pip install animaflow
```

Para renderizar animações com Manim:

```bash
pip install "animaflow[manim]"
```

A renderização de vídeo com Manim também requer FFmpeg instalado no sistema.

## Exemplo rápido

```python
import animaflow as af

flow = af.Flow(title="Pipeline de pedidos")
api = flow.add_node("API", subtitle="Recebe pedidos")
worker = flow.add_node("Worker", subtitle="Processa eventos")
database = flow.add_node("Database", subtitle="Armazena resultados")

flow.connect(api, worker, label="evento")
flow.connect(worker, database, label="persistência")
flow.auto_layout(mode="horizontal")
flow.timeline.reveal_sequence(delay_per_item=0.3)
flow.export_html("pipeline.html")
```

O arquivo `pipeline.html` pode ser aberto diretamente em um navegador.

---

## Exemplos Prontos

Os scripts de demonstração e seus comandos de execução estão na [pasta de exemplos do GitHub](https://github.com/Oseiasdfarias/animaflow/tree/main/examples).

| Exemplo | Descrição | Como Executar |
| --- | --- | --- |
| [`event_driven_pipeline.py`](https://github.com/Oseiasdfarias/animaflow/blob/main/examples/event_driven_pipeline.py) | Pipeline de eventos com animação contínua | `manim -qm examples/event_driven_pipeline.py EventDrivenPipelineAnimation` |
| [`multi_agent_swarm.py`](https://github.com/Oseiasdfarias/animaflow/blob/main/examples/multi_agent_swarm.py) | Orquestração multiagente em camadas | `manim -qm examples/multi_agent_swarm.py AgentSwarmAnimation` |
| [`rag_pipeline_manim.py`](https://github.com/Oseiasdfarias/animaflow/blob/main/examples/rag_pipeline_manim.py) | Pipeline RAG renderizado com Manim | `manim -qm examples/rag_pipeline_manim.py RAGFlowAnimation` |
| [`rag_pipeline_web.py`](https://github.com/Oseiasdfarias/animaflow/blob/main/examples/rag_pipeline_web.py) | Exportação para HTML/SVG interativo | `python examples/rag_pipeline_web.py` |

## Licença

Distribuído sob a licença MIT. Consulte o [arquivo de licença](https://github.com/Oseiasdfarias/animaflow/blob/main/LICENSE).
