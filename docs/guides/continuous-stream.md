# Fluxo Contínuo de Partículas (Stream Packets)

O método `stream_packets` foi projetado para animar fluxos em tempo real, pipelines orientados a eventos e filas de streaming contínuo (Kafka, Flink, WebSockets).

Em vez de enviar apenas uma bolinha isolada, o `stream_packets` gera uma série contínua e periódica de partículas que percorrem as arestas do grafo suavemente com fade-in no início e fade-out no final.

---

## :material-waves: Sintaxe Básica

```python
# Dispara um fluxo contínuo de partículas em todas as arestas
flow.timeline.stream_packets(
    count=6,        # Quantidade de partículas por aresta
    speed=0.75,     # Velocidade de trânsito ao longo do percurso
    duration=3.5    # Tempo total que o streaming permanecerá ativo
)
```

---

## :material-crosshairs-gps: Direcionando para Arestas Específicas

Você também pode ativar o streaming em apenas uma conexão específica entre dois serviços de interesse:

```python
# Ativa o fluxo apenas entre a fila Kafka e o consumidor Flink
flow.timeline.stream_packets(
    from_node=kafka_broker,
    to_node=flink_worker,
    count=8,
    speed=1.0,
    duration=4.0
)
```

---

## :material-tune-variant: Parâmetros Detalhados

| Parâmetro | Tipo | Padrão | Descrição |
| --- | --- | --- | --- |
| `from_node` | `Node` / `str` | `None` | Nó de origem. Se `None`, anima todas as arestas do fluxo simultaneamente |
| `to_node` | `Node` / `str` | `None` | Nó de destino |
| `count` | `int` | `5` | Número de partículas distribuídas ao longo da extensão do trajeto |
| `speed` | `float` | `0.65` | Velocidade relativa de avanço das partículas |
| `duration` | `float` | `2.5` | Duração em segundos da reprodução do stream na cena |
| `color` | `str` | `None` | Cor de destaque das partículas. Se omitido, utiliza a cor acento do tema |

---

## :material-eye-outline: Efeito Visual nos Renderizadores

- **No Manim (Vídeo/GIF)**: Utiliza um grupo de `Dot`s vetoriais gerenciados por um `updater` único de alta performance. As partículas possuem opacidade modelada por curva senoidal: entram transparentes, atingem brilho máximo no meio do caminho e desaparecem suavemente ao atingir o nó de destino.
- **Na Web (HTML Canvas/SVG)**: Spawna círculos SVG animados com CSS transitions e temporizadores em JavaScript puro, sem travar a thread principal da página.

