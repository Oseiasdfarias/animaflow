from typing import List
from .models import Node, Edge


class LayoutEngine:
    """Calculates spatial positions for nodes in a flow."""

    @staticmethod
    def arrange_horizontal(nodes: List[Node], spacing: float = 2.2, y: float = 0.0) -> None:
        """Arranges nodes in a horizontal sequence centered at origin."""
        n = len(nodes)
        if n == 0:
            return
        total_width = (n - 1) * spacing
        start_x = -total_width / 2.0

        for i, node in enumerate(nodes):
            x = start_x + i * spacing
            node.set_position(x, y, 0.0)

    @staticmethod
    def arrange_vertical(nodes: List[Node], spacing: float = 1.8, x: float = 0.0) -> None:
        """Arranges nodes in a vertical sequence centered at origin."""
        n = len(nodes)
        if n == 0:
            return
        total_height = (n - 1) * spacing
        start_y = total_height / 2.0

        for i, node in enumerate(nodes):
            y = start_y - i * spacing
            node.set_position(x, y, 0.0)
