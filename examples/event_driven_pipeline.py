import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from manim import Scene, config
import animaflow as af

config.pixel_width = 1080
config.pixel_height = 1080
config.frame_rate = 30


class EventDrivenPipelineAnimation(Scene):
    """Event-Driven Distributed Streaming Architecture:
    [API Gateway] ──> [Kafka Event Log]
                           ├──> [Flink Engine] ────> [Redis Cache]
                           └──> [ETL Indexer] ────> [PostgreSQL]
    """

    def construct(self):
        flow = af.Flow(
            title="Real-Time Event Stream Architecture",
            theme=af.DarkTerminal,
        )

        # Stage 1: Ingestion
        gateway = flow.add_node("API Gateway", subtitle="Ingress Envoy")

        # Stage 2: Event Broker
        kafka = flow.add_node("Kafka Topic", subtitle="events.orders")

        # Stage 3: Stream Processors (Parallel Consumer Group)
        flink = flow.add_node("Flink Engine", subtitle="Window Aggregator")
        indexer = flow.add_node("ETL Indexer", subtitle="Async Consumer")

        # Stage 4: Sinks / Storage
        redis = flow.add_node("Redis Cache", subtitle="Sub-ms Latency")
        postgres = flow.add_node("PostgreSQL", subtitle="ACID Relational")

        # Topologies / Edges
        flow.connect(gateway, kafka, label="produce")
        flow.connect(kafka, flink, label="stream")
        flow.connect(kafka, indexer, label="consume")
        flow.connect(flink, redis, label="upsert")
        flow.connect(indexer, postgres, label="commit")

        # Auto-layout in 4 stages
        flow.auto_layout_layers(
            [
                [gateway],
                [kafka],
                [flink, indexer],
                [redis, postgres],
            ],
            h_gap=1.20,
            v_gap=1.00,
        )

        # Interactive Timeline
        flow.timeline.reveal_sequence(delay_per_item=0.20)

        # Step 1: Ingestion
        flow.timeline.send_packet(gateway, kafka, duration=0.55)
        flow.timeline.highlight_node(kafka, status="active", duration=0.4)

        # Step 2: Parallel Stream Fan-out
        flow.timeline.send_packet(kafka, flink, duration=0.55)
        flow.timeline.send_packet(kafka, indexer, duration=0.55)
        flow.timeline.highlight_node(flink, status="active", duration=0.45)
        flow.timeline.highlight_node(indexer, status="active", duration=0.45)

        # Step 3: Sink to Datastores
        flow.timeline.send_packet(flink, redis, duration=0.55)
        flow.timeline.send_packet(indexer, postgres, duration=0.55)
        flow.timeline.highlight_node(redis, status="success", duration=0.6)
        flow.timeline.highlight_node(postgres, status="success", duration=0.6)

        flow.timeline.wait(1.5)

        # Render
        flow.render_manim(self)
