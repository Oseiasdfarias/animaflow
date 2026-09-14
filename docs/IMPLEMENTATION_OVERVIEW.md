# Implementação da Biblioteca **animaflow**

## ✅ Funcionalidades já implementadas

| Área | Descrição | Arquivo(s) principais |
|------|-----------|-----------------------|
| **Core** | Modelos de nó/aresta, DSL de construção de grafos, layout automático em camadas | `src/animaflow/core/flow.py`, `src/animaflow/core/layout.py` |
| **Timeline / Ações** | Sequenciamento declarativo de animações; novo enum `STREAM_PACKETS` e método `Timeline.stream_packets` para fluxo contínuo | `src/animaflow/core/timeline.py` |
| **Renderizadores** | *Manim* – gera MP4/GIF com animação de partículas contínuas; *Web Canvas* – SVG + animação JavaScript com `setInterval` | `src/animaflow/backends/manim/renderer.py`, `src/animaflow/backends/web/canvas.py` |
| **Exemplos** | `event_driven_pipeline.py` (pipeline com fluxo contínuo) e `multi_agent_swarm.py` (lay‑out em camadas) | `examples/event_driven_pipeline.py`, `examples/multi_agent_swarm.py` |
| **Testes** | Testes unitários básicos que cobrem criação de fluxo e exportação | `tests/` |
| **Mídia gerada** | GIF e MP4 demonstrando a nova animação | `media/event_driven_pipeline_stream.gif`, `media/videos/event_driven_pipeline/.../EventDrivenPipelineAnimation.mp4` |

## ⚠️ Gaps / Oportunidades de expansão

| Tema | O que ainda falta | Onde observar / TODO |
|------|-------------------|----------------------|
| **Tipos de diagramas** | Suporte a diagramas de sequência, state‑machine, ER, class | Ainda não há módulos específicos em `src/animaflow/core/` |
| **Ações de timeline não usadas** | `TRANSITION_NODE` está declarado mas nunca tratado | `src/animaflow/core/timeline.py` (enum) e `src/animaflow/backends/manim/renderer.py` (dispatch) |
| **Customização de estilos** | API pública para forma, cor, espessura de nós/arestas, temas | Atualmente apenas atributos básicos em `Node`/`Edge` |
| **Interatividade Web** | Play/pause, zoom/pan, tooltips | `src/animaflow/backends/web/canvas.py` – implementação estática |
| **Escalabilidade** | Performance para grafos grandes (>150 nós), cache de caminhos | `LayoutEngine.arrange_layers` calcula tudo em memória; `renderer.play_on_scene` cria todas as partículas de uma vez |
| **Documentação** | Guia de usuário detalhado, exemplos de `stream_packets` e `auto_layout_layers` | `README.md` ainda não cobre as novidades |
| **Cobertura de testes** | Testes de renderização (Manim/Web) e combinações avançadas de timeline | Apenas testes de construção básica em `tests/` |
| **CLI** | Ferramenta de linha de comando para renderizar scripts e escolher backend | Nenhum ponto de entrada de console ainda |
| **Exportação avançada** | PlantUML, GraphViz DOT, PDF direto | Backends atuais só geram MP4/GIF/HTML |
| **Animações adicionais** | `HIGHLIGHT_PATH`, `FADE_IN_NODE`, transições de estado | `renderer.py` pode ser estendido com novos `ActionType` |

## 🚀 Próximos passos (roadmap)

### Curto prazo (1‑2 semanas)
- **Limpar enum**: remover ou implementar `TRANSITION_NODE`.
- **Documentar API**: atualizar `README.md` com seção “Fluxo contínuo e layout em camadas”, exemplos de uso de `Timeline.stream_packets`.
- **Play/Pause Web**: adicionar botões que controlam `requestAnimationFrame`/`clearInterval`.
- **Teste de integração**: script que gera GIF a partir de exemplo e verifica a existência do arquivo (uso de `subprocess.run` + `ffprobe`).

### Médio prazo (3‑4 semanas)
- **Diagramas de sequência**: nova classe `SequenceDiagram` (core) + renderização Manim (setas temporais) e Web (linhas de tempo).
- **Novas ações de timeline**: `HIGHLIGHT_PATH`, `FADE_IN_NODE`, `FADE_OUT_EDGE` + implementação nos renderizadores.
- **API de estilos**: permitir passagem de `style=dict(color=…, shape=…, radius=…)` ao criar nós/arestas; propagar ao renderer.
- **Caching de caminhos**: memoizar `Path.point_at_fraction` para melhorar performance em grafos grandes.

### Longo prazo (1‑2 meses)
- **Outros tipos de diagramas**: ER, class, state‑machine – módulos separados em `core/diagrams/`.
- **CLI** (`animaflow-cli`): `argparse` para renderizar scripts, escolher backend, definir parâmetros de saída.
- **Exportação múltipla**: gerar DOT/PlantUML, converter para PDF via `graphviz`.
- **Profiling**: medir e otimizar renderização de grafos >150 nós, possivelmente introduzir renderização por *tiles* ou *lazy loading*.

---

*Este documento serve como ponto de partida para a documentação de implementação e para o planejamento futuro da biblioteca.*

