# Galeria: Pipeline de RAG & LLMs

Demonstração de uma arquitetura completa de Recuperação Aumentada por Geração (*Retrieval-Augmented Generation*), conectando clientes, vetores, modelos e bancos relacionais.

---

## 📸 Demonstração Visual

<p align="center">
  <img src="../../assets/rag_pipeline.png" width="750" alt="RAG Architecture">
</p>

---

## 💻 Código de Demonstração

Disponível em [`examples/rag_pipeline_manim.py`](https://github.com/Oseiasdfarias/animaflow/blob/main/examples/rag_pipeline_manim.py):

```python
from manim import Scene
import animaflow as af

class RAGFlowAnimation(Scene):
    def construct(self):
        flow = af.Flow(title="Production RAG System Architecture")

        user = flow.add_node("User Query", subtitle="Prompt / Context")
        embed = flow.add_node("Embedding Engine", subtitle="text-embedding-3")
        vdb = flow.add_node("Vector Database", subtitle="Qdrant / Milvus")
        llm = flow.add_node("LLM Inference", subtitle="Claude / GPT-4")
        resp = flow.add_node("Response Output", subtitle="Streaming Token")

        flow.auto_layout_layers(
            layers=[[user], [embed], [vdb], [llm], [resp]],
            h_gap=1.5
        )

        flow.connect(user, embed, label="embed_query()")
        flow.connect(embed, vdb, label="similarity_search()")
        flow.connect(vdb, llm, label="inject_context()")
        flow.connect(llm, resp, label="stream_response()")

        flow.timeline.reveal_sequence(delay=0.2)
        flow.timeline.send_packet(from_node=user, to_node=embed)
        flow.timeline.send_packet(from_node=embed, to_node=vdb)
        flow.timeline.highlight_node(vdb)
        flow.timeline.send_packet(from_node=vdb, to_node=llm)
        flow.timeline.stream_packets(from_node=llm, to_node=resp, count=6, duration=2.5)

        flow.render_manim(self)
```

---

## 🚀 Como Executar

```bash
manim -qm examples/rag_pipeline_manim.py RAGFlowAnimation
```
