import sys
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import animaflow as af

# 1. Setup Architecture Flow
flow = af.Flow(title="LLM RAG Pipeline", theme=af.DarkTerminal)

user = flow.add_node("Client", subtitle="Browser / App", icon="user")
api = flow.add_node("API Gateway", subtitle="FastAPI", icon="server")
retriever = flow.add_node("Vector DB", subtitle="Qdrant / Milvus", icon="database")
llm = flow.add_node("LLM Engine", subtitle="Claude 3.5", icon="cpu")

# Connect nodes
flow.connect(user, api, label="Prompt")
flow.connect(api, retriever, label="Query Vector")
flow.connect(api, llm, label="Context + Prompt")

# Auto-calculate positions
flow.auto_layout(mode="horizontal", spacing=2.2)

# Define narrative timeline
flow.timeline.reveal_sequence(delay_per_item=0.4)
flow.timeline.send_packet(user, api, label="POST /ask")
flow.timeline.send_packet(api, retriever, label="search_knn()")
flow.timeline.highlight_node(retriever, status="active")
flow.timeline.send_packet(api, llm, label="stream_tokens()")
flow.timeline.highlight_node(llm, status="success")

# 2. Export Standalone Interactive HTML Canvas
output_html = Path(__file__).parent / "rag_pipeline.html"
flow.export_html(str(output_html))
print(f"Interactive Web Canvas exported to: {output_html}")
