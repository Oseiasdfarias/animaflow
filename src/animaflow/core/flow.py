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
        width: Optional[float] = None,
        height: Optional[float] = None,
        min_width: float = 1.7,
        min_height: float = 1.25,
        padding: float = 0.50,
        id: Optional[str] = None,
    ) -> Node:
        node_id = id or str(uuid.uuid4())[:8]
        estimated_w = max(min_width, len(title) * 0.12 + padding * 2)
        if subtitle:
            estimated_w = max(estimated_w, len(subtitle) * 0.09 + padding * 2)

        node = Node(
            id=node_id,
            title=title,
            subtitle=subtitle,
            icon=icon,
            shape=shape,
            width=width if width is not None else estimated_w,
            height=height if height is not None else min_height,
            min_width=min_width,
            min_height=min_height,
            padding=padding,
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
        self,
        mode: str = "horizontal",
        gap: float = 0.85,
        offset: float = 0.0,
        spacing: Optional[float] = None,
        min_label_gap: bool = True,
    ) -> "Flow":
        nodes_list = list(self.nodes.values())
        if mode == "horizontal":
            LayoutEngine.arrange_horizontal(
                nodes_list,
                gap=gap,
                y=offset,
                spacing=spacing,
                edges=self.edges,
                min_label_gap=min_label_gap,
            )
        elif mode == "vertical":
            LayoutEngine.arrange_vertical(
                nodes_list,
                gap=gap,
                x=offset,
                spacing=spacing,
                edges=self.edges,
            )
        return self

    def auto_layout_layers(
        self,
        layers: List[List[Union[Node, str]]],
        h_gap: float = 1.20,
        v_gap: float = 0.90,
    ) -> "Flow":
        """Arranges nodes into columnar tiers/stages with clean vertical & horizontal intervals."""
        resolved_layers: List[List[Node]] = []
        for layer in layers:
            col = []
            for item in layer:
                node = self.nodes[item] if isinstance(item, str) else item
                col.append(node)
            resolved_layers.append(col)

        LayoutEngine.arrange_layers(resolved_layers, h_gap=h_gap, v_gap=v_gap)
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
