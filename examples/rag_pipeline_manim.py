import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from manim import Scene, config
import animaflow as af

config.pixel_width = 1080
config.pixel_height = 1080
config.frame_rate = 30


class RAGFlowAnimation(Scene):
    def construct(self):
        # 1. Declare flow
        flow = af.Flow(title="LLM RAG Architecture", theme=af.DarkTerminal)

        client = flow.add_node("Client", subtitle="Chat UI")
        gateway = flow.add_node("Gateway", subtitle="FastAPI")
        vdb = flow.add_node("Vector DB", subtitle="Qdrant")
        llm = flow.add_node("LLM Engine", subtitle="Claude 3.5")

        flow.connect(client, gateway, label="prompt")
        flow.connect(gateway, vdb, label="search")
        flow.connect(gateway, llm, label="context")

        flow.auto_layout(mode="horizontal", spacing=2.15)

        # 2. Add narrative actions
        flow.timeline.reveal_sequence(delay_per_item=0.3)
        flow.timeline.send_packet(client, gateway, duration=0.6)
        flow.timeline.send_packet(gateway, vdb, duration=0.6)
        flow.timeline.highlight_node(vdb, status="active", duration=0.6)
        flow.timeline.send_packet(gateway, llm, duration=0.6)
        flow.timeline.highlight_node(llm, status="success", duration=0.7)
        flow.timeline.wait(1.5)

        # 3. Render directly using animaflow's Manim driver
        flow.render_manim(self)
