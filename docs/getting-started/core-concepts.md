# Conceitos Fundamentais

A arquitetura do **animaflow** apoia-se em quatro pilares conceituais fundamentais: **Nós**, **Arestas**, **Layouts** e **Linha do Tempo**.

---

## 1. O Modelo do Grafo (`Flow`)

O `Flow` é o contêiner raiz que armazena a topologia da arquitetura. Ele mantém as listas de nós registrados, arestas direcionadas, configurações visuais e a linha do tempo de eventos.

```python
import animaflow as af

flow = af.Flow(title="Production Topology")
```

---

## 2. Nós (`Node`)

Um nó representa um serviço, componente de infraestrutura, banco de dados ou ator do sistema:

- **`id`**: Identificador único (gerado automaticamente se omitido).
- **`name`**: Título principal exibido em destaque no cartão (ex: `"API Gateway"`).
- **`subtitle`**: Texto secundário explicativo para contexto técnico (ex: `"FastAPI / Python"`).
- **`icon`**: Símbolo ou categoria visual.

---

## 3. Arestas (`Edge`)

As arestas representam canais de comunicação, chamadas de rede ou filas de eventos entre dois nós:

- **Direcionalidade**: Do nó de origem (`src`) para o nó de destino (`tgt`).
- **`label`**: Texto opcional que descreve o protocolo ou payload (ex: `"gRPC stream"`).
- **Wrapping Inteligente**: Se o rótulo for longo, o algoritmo calcula quebras de linha automáticas para evitar que o texto invada o retângulo dos nós adjacentes.

---

## 4. O Motor de Layout (`LayoutEngine`)

Diferente de frameworks que exigem coordenadas Manim absolutas como `node.move_to([2.5, -1.2, 0])`, o animaflow calcula as posições automaticamente com base na topologia:

- **Margens Dinâmicas**: Calcula a largura real de cada nó (baseado no tamanho do texto e subtítulo) e define um espaçamento mínimo seguro (`gap`).
- **Empilhamento em Camadas (DAG)**: Suporta estruturas de nós paralelos centralizados em colunas sem risco de colisão.

---

## 5. A Linha do Tempo (`Timeline`)

A narrativa de animação é declarada como uma sequência de eventos:

```python
# Revelação sequencial dos nós
flow.timeline.reveal_sequence(delay=0.3)

# Pulso de pacote único
flow.timeline.send_packet(from_node=src, to_node=tgt, label="auth token")

# Pulso contínuo de fluxo de partículas
flow.timeline.stream_packets(count=5, speed=0.7, duration=3.0)

# Realce visual de um nó específico
flow.timeline.highlight_node(node)
```

