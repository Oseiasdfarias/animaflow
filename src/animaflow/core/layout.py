from typing import List
from .models import Node, Edge


class LayoutEngine:
    """Calculates spatial positions for nodes in a flow with collision-free gap spacing."""

    @staticmethod
    def arrange_horizontal(
        nodes: List[Node],
        gap: float = 0.85,
        y: float = 0.0,
        spacing: float = None,
    ) -> None:
        """Arranges nodes horizontally with an exact minimum gap between adjacent borders."""
        n = len(nodes)
        if n == 0:
            return

        # If user explicitly set old spacing, support it
        if spacing is not None and gap == 0.85:
            total_width = (n - 1) * spacing
            start_x = -total_width / 2.0
            for i, node in enumerate(nodes):
                x = start_x + i * spacing
                node.set_position(x, y, 0.0)
            return

        # Dynamic spacing: sum(widths) + (n-1)*gap
        total_width = sum(node.width for node in nodes) + (n - 1) * gap
        current_x = -total_width / 2.0

        for node in nodes:
            center_x = current_x + (node.width / 2.0)
            node.set_position(center_x, y, 0.0)
            current_x += node.width + gap

    @staticmethod
    def arrange_vertical(
        nodes: List[Node],
        gap: float = 0.70,
        x: float = 0.0,
        spacing: float = None,
    ) -> None:
        """Arranges nodes vertically with an exact minimum gap between adjacent borders."""
        n = len(nodes)
        if n == 0:
            return

        if spacing is not None and gap == 0.70:
            total_height = (n - 1) * spacing
            start_y = total_height / 2.0
            for i, node in enumerate(nodes):
                y = start_y - i * spacing
                node.set_position(x, y, 0.0)
            return

        total_height = sum(node.height for node in nodes) + (n - 1) * gap
        current_y = total_height / 2.0

        for node in nodes:
            center_y = current_y - (node.height / 2.0)
            node.set_position(x, center_y, 0.0)
            current_y -= node.height + gap
