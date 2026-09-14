from typing import Any, Dict, List, Optional, Union
import uuid
from .models import Edge, EdgeStyle, Node, NodeShape, NodeStatus
from .timeline import Timeline
from .layout import LayoutEngine
from ..themes.base import Theme
from ..themes import DarkTerminal


class Flow:
    """The central diagram abstraction that coordinates nodes, edges and animation."""

    def __init__(
        self,
        title: Optional[str] = None,
        theme: Theme = DarkTerminal,
    ):
        self.title = title
        self.theme = theme
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.timeline = Timeline()

    def add_node(
        self,
        title: str,
        subtitle: Optional[str] = None,
        icon: Optional[str] = None,
        shape: NodeShape = NodeShape.ROUNDED_RECT,
        width: float = 1.6,
        height: float = 1.3,
        id: Optional[str] = None,
    ) -> Node:
        node_id = id or str(uuid.uuid4())[:8]
        node = Node(
            id=node_id,
            title=title,
            subtitle=subtitle,
            icon=icon,
            shape=shape,
            width=width,
            height=height,
        )
        self.nodes[node.id] = node
        return node

    def connect(
        self,
        source: Union[Node, str],
        target: Union[Node, str],
        label: Optional[str] = None,
        style: EdgeStyle = EdgeStyle.SOLID,
    ) -> Edge:
        s_id = source.id if isinstance(source, Node) else str(source)
        t_id = target.id if isinstance(target, Node) else str(target)
        edge = Edge(
            source_id=s_id,
            target_id=t_id,
            label=label,
            style=style,
        )
        self.edges.append(edge)
        return edge

    def auto_layout(
        self, mode: str = "horizontal", spacing: float = 2.2, offset: float = 0.0
    ) -> "Flow":
        nodes_list = list(self.nodes.values())
        if mode == "horizontal":
            LayoutEngine.arrange_horizontal(nodes_list, spacing=spacing, y=offset)
        elif mode == "vertical":
            LayoutEngine.arrange_vertical(nodes_list, spacing=spacing, x=offset)
        return self

    def render_manim(self, scene: Any) -> Any:
        """Helper to render this flow into an active Manim scene."""
        from ..backends.manim.renderer import ManimFlowRenderer

        renderer = ManimFlowRenderer(self)
        return renderer.play_on_scene(scene)

    def export_html(self, output_path: str) -> str:
        """Helper to export this flow to an interactive HTML Canvas/SVG file."""
        from ..backends.web.canvas import WebCanvasExporter

        return WebCanvasExporter.to_html(self, output_path)

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the diagram and timeline to a JSON-compatible dict."""
        return {
            "title": self.title,
            "theme": self.theme.to_dict(),
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges],
            "timeline": self.timeline.to_dict(),
        }
