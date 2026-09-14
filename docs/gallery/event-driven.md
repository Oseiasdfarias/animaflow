# Galeria: Pipeline de Eventos em Tempo Real

Este caso de uso demonstra uma arquitetura moderna orientada a eventos (*Event-Driven Pipeline*) utilizando a API de **stream contínuo de partículas** do animaflow.

---

## 📸 Demonstração Visual

<p align="center">
  <img src="../../assets/event_driven_pipeline_stream.gif" width="750" alt="Event-Driven Pipeline Stream">
</p>

---

## 💻 Código Completo

Disponível em [`examples/event_driven_pipeline.py`](https://github.com/Oseiasdfarias/animaflow/blob/main/examples/event_driven_pipeline.py):

```python
from manim import Scene
import animaflow as af

class EventDrivenPipelineAnimation(Scene):
    def construct(self):
        flow = af.Flow(title="Real-Time Event Processing Pipeline")

        # 1. Componentes do sistema
        client = flow.add_node("IoT Devices", subtitle="MQTT Producer")
        broker = flow.add_node("Kafka Broker", subtitle="Event Bus")
        worker = flow.add_node("Stream Worker", subtitle="Flink / Python")
        lake   = flow.add_node("Data Lake", subtitle="ClickHouse")

        # 2. Layout em camadas
        flow.auto_layout_layers(
            layers=[[client], [broker], [worker], [lake]],
            h_gap=1.6
        )

        # 3. Conexões
        flow.connect(client, broker, label="telemetry")
        flow.connect(broker, worker, label="ingest")
        flow.connect(worker, lake, label="batch write")

        # 4. Linha do Tempo com Stream Contínuo
        flow.timeline.reveal_sequence(delay=0.3)
        flow.timeline.stream_packets(count=6, speed=0.8, duration=3.0)
        flow.timeline.wait(1.0)

        # 5. Renderização
        flow.render_manim(self)
```

---

## 🚀 Como Executar

```bash
manim -qm examples/event_driven_pipeline.py EventDrivenPipelineAnimation
```
