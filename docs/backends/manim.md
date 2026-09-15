# Backend Manim (Vídeos & GIFs)

O renderizador **Manim CE** (`backends.manim.renderer`) é o motor principal para converter a definição semântica do `Flow` em animações vetoriais de altíssima fidelidade gráfica.

---

## :material-movie-play-outline: Como Usar em uma Cena Manim

Basta instanciar uma classe que herda de `Scene` do Manim e invocar `flow.render_manim(self)`:

```python
from manim import Scene, config
import animaflow as af

# Configurações opcionais de saída
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60

class MinhaCenaAnimada(Scene):
    def construct(self):
        flow = af.Flow(title="Microservices Overview")
        
        # ... declare nós, arestas e timeline ...
        
        # Renderiza automaticamente
        flow.render_manim(self)
```

---

## :material-console: Comandos de Linha de Comando Manim

Para renderizar seus scripts, utilize os parâmetros padrão da CLI do Manim:

```bash
# Prévia rápida em baixa resolução (480p a 15fps)
manim -ql meu_script.py MinhaCenaAnimada

# Qualidade intermediária para validação (720p a 30fps)
manim -qm meu_script.py MinhaCenaAnimada

# Qualidade de produção (1080p a 60fps)
manim -qh --fps 60 meu_script.py MinhaCenaAnimada

# Gerar GIF diretamente
manim -qm -i meu_script.py MinhaCenaAnimada
```

---

## :material-palette-outline: Características Visuais do Renderer

- **Mobjects Refinados**: Cartões com cantos arredondados, bordas de destaque e preenchimento escuro de alta legibilidade.
- **Hierarquia Tipográfica**: O título do nó é exibido em peso SemiBold e o subtítulo é estilizado como uma badge de metadados técnicos.
- **Roteamento Curvado**: As setas de conexão utilizam vetores suavizados e evitam sobreposição com rótulos e caixas.
- **Animações em 60fps**: Updaters otimizados para streams de partículas garantem renderização fluida sem queda de frames.

