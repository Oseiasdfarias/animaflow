# Criando seu Primeiro Diagrama

Neste tutorial rápido, você vai criar do zero um diagrama animado de microsserviços e renderizá-lo em vídeo com o Manim.

---

## :material-file-code-outline: Passo 1: O Script Python

Crie um arquivo chamado `meu_primeiro_fluxo.py`:

```python
from manim import Scene
import animaflow as af

class PrimeiroFluxoAnimado(Scene):
    def construct(self):
        # 1. Instanciando o Flow
        flow = af.Flow(title="Arquitetura de Mensageria")

        # 2. Adicionando os Nós (Entidades do Sistema)
        app = flow.add_node("Web App", subtitle="Next.js Frontend")
        api = flow.add_node("API Core", subtitle="FastAPI")
        queue = flow.add_node("Task Queue", subtitle="Redis / Celery")
        worker = flow.add_node("Worker", subtitle="Async Consumer")

        # 3. Organizando em Camadas Automáticas
        flow.auto_layout_layers(
            layers=[[app], [api], [queue], [worker]],
            h_gap=1.6,
            v_gap=0.8
        )

        # 4. Conectando as Arestas
        flow.connect(app, api, label="POST /job")
        flow.connect(api, queue, label="enqueue")
        flow.connect(queue, worker, label="consume")

        # 5. Programando a Linha do Tempo
        flow.timeline.reveal_sequence(delay=0.25)
        flow.timeline.send_packet(from_node=app, to_node=api, label="dispatch")
        flow.timeline.send_packet(from_node=api, to_node=queue)
        flow.timeline.highlight_node(queue)
        flow.timeline.stream_packets(from_node=queue, to_node=worker, count=4, speed=0.75, duration=2.5)
        flow.timeline.wait(1.0)

        # 6. Renderização
        flow.render_manim(self)
```

---

## :material-video-outline: Passo 2: Executando a Renderização

Para renderizar o vídeo em qualidade média (720p) ou alta (1080p), utilize a CLI do Manim:

```bash
# Renderização rápida (qualidade baixa/média para iteração)
manim -qm meu_primeiro_fluxo.py PrimeiroFluxoAnimado

# Renderização final para publicação (1080p a 60fps)
manim -qh --fps 60 meu_primeiro_fluxo.py PrimeiroFluxoAnimado
```

O vídeo gerado estará disponível na pasta `media/videos/meu_primeiro_fluxo/`.

---

## :material-web: Alternativa: Exportando para Web (HTML)

Se preferir exportar uma página web interativa independente sem precisar do Manim ou do ffmpeg:

```python
html_page = flow.export_html()
with open("fluxo.html", "w", encoding="utf-8") as f:
    f.write(html_page)
```

Abra o arquivo `fluxo.html` em qualquer navegador para interagir com o diagrama em tempo real!

