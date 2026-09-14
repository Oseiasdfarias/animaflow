import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from manim import Scene, config
import animaflow as af

config.pixel_width = 1080
config.pixel_height = 1080
config.frame_rate = 30


class AgentSwarmAnimation(Scene):
    """Complex 2D Multi-Branch Architecture:
    User -> Router Agent
      ├── Code Agent -> Critic Gate
      └── Search Agent -> Critic Gate
    """

    def construct(self):
        flow = af.Flow(title="Multi-Agent Orchestrator", theme=af.MidnightCyber)

        # Level 1: Input
        user = flow.add_node("User Task", subtitle="Goal Input")

        # Level 2: Orchestrator
        orchestrator = flow.add_node("Router Agent", subtitle="Task Decomposer")

        # Level 3: Specialized Branch Workers (Top and Bottom branches)
        code_agent = flow.add_node("Code Agent", subtitle="Python Sandbox")
        search_agent = flow.add_node("Search Agent", subtitle="Web Retriever")

        # Level 4: Evaluator & Output
        critic = flow.add_node("Critic Agent", subtitle="Quality Gate")

        # Connect the DAG
        flow.connect(user, orchestrator, label="prompt")
        flow.connect(orchestrator, code_agent, label="task A")
        flow.connect(orchestrator, search_agent, label="task B")
        flow.connect(code_agent, critic, label="code test")
        flow.connect(search_agent, critic, label="citations")

        # Automatically layout DAG in 4 clear stages with comfortable horizontal & vertical gaps
        flow.auto_layout_layers(
            [[user], [orchestrator], [code_agent, search_agent], [critic]], h_gap=1.20, v_gap=1.00
        )

        # Timeline Narrative
        flow.timeline.reveal_sequence(delay_per_item=0.25)
        flow.timeline.send_packet(user, orchestrator, duration=0.6)
        flow.timeline.highlight_node(orchestrator, status="active", duration=0.5)

        # Fork execution
        flow.timeline.send_packet(orchestrator, code_agent, duration=0.6)
        flow.timeline.send_packet(orchestrator, search_agent, duration=0.6)
        flow.timeline.highlight_node(code_agent, status="active", duration=0.5)
        flow.timeline.highlight_node(search_agent, status="active", duration=0.5)

        # Join to Critic
        flow.timeline.send_packet(code_agent, critic, duration=0.6)
        flow.timeline.send_packet(search_agent, critic, duration=0.6)
        flow.timeline.highlight_node(critic, status="success", duration=0.8)
        flow.timeline.wait(1.5)

        # Render
        flow.render_manim(self)
