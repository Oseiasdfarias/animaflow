import unittest
import sys
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from animaflow import Flow, DarkTerminal, NodeShape


class TestAnimaflowCore(unittest.TestCase):
    def test_create_flow(self):
        flow = Flow(title="Test Pipeline", theme=DarkTerminal)
        n1 = flow.add_node("API", subtitle="FastAPI")
        n2 = flow.add_node("Worker", subtitle="Celery")
        edge = flow.connect(n1, n2, label="enqueue")

        self.assertEqual(len(flow.nodes), 2)
        self.assertEqual(len(flow.edges), 1)
        self.assertEqual(edge.source_id, n1.id)
        self.assertEqual(edge.target_id, n2.id)

    def test_auto_layout(self):
        flow = Flow(title="Layout Test")
        n1 = flow.add_node("A")
        n2 = flow.add_node("B")
        n3 = flow.add_node("C")
        flow.auto_layout(mode="horizontal", spacing=2.0)

        # Centered: n1 at -2.0, n2 at 0.0, n3 at 2.0
        self.assertEqual(n1.position[0], -2.0)
        self.assertEqual(n2.position[0], 0.0)
        self.assertEqual(n3.position[0], 2.0)

    def test_timeline_actions(self):
        flow = Flow(title="Timeline Test")
        n1 = flow.add_node("User")
        n2 = flow.add_node("Server")
        flow.timeline.reveal_sequence(delay_per_item=0.5)
        flow.timeline.send_packet(n1, n2, label="HTTP GET")
        flow.timeline.highlight_node(n2, status="alert")

        actions = flow.timeline.actions
        self.assertEqual(len(actions), 3)
        self.assertEqual(actions[0].action_type.value, "reveal_sequence")
        self.assertEqual(actions[1].action_type.value, "send_packet")
        self.assertEqual(actions[2].action_type.value, "highlight_node")

    def test_to_dict_serialization(self):
        flow = Flow(title="Serialization Test")
        n1 = flow.add_node("Input")
        n2 = flow.add_node("Output")
        flow.connect(n1, n2)
        d = flow.to_dict()

        self.assertEqual(d["title"], "Serialization Test")
        self.assertEqual(len(d["nodes"]), 2)
        self.assertEqual(len(d["edges"]), 1)
        self.assertIn("theme", d)


if __name__ == "__main__":
    unittest.main()
