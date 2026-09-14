from typing import List, Optional, Dict
from .models import Node, Edge


class LayoutEngine:
    """Calculates spatial positions for nodes in a flow with collision-free gap spacing."""

    @staticmethod
    def calculate_label_aware_gap(
        nodes: List[Node],
        edges: List[Edge],
        min_gap: float = 0.85,
        min_label_padding: float = 0.40,
    ) -> float:
        """Determines the minimum gap needed so that edge labels/pill badges never collide with boxes."""
        max_label_len = 0
        for edge in edges:
            if edge.label:
                max_label_len = max(max_label_len, len(edge.label))

        if max_label_len == 0:
            return min_gap

        # Estimate label width: ~0.10 per mono char + badge margins
        estimated_label_width = (max_label_len * 0.10) + 0.20
        # Required gap is label width + breathing room on both sides
        required_gap = estimated_label_width + (min_label_padding * 2)
        return max(min_gap, required_gap)

    @staticmethod
    def arrange_horizontal(
        nodes: List[Node],
        gap: float = 0.85,
        y: float = 0.0,
        spacing: float = None,
        edges: Optional[List[Edge]] = None,
        min_label_gap: bool = True,
    ) -> float:
        """Arranges nodes horizontally with an exact minimum gap between adjacent borders."""
        n = len(nodes)
        if n == 0:
            return gap

        # Calculate label-aware gap if edges are provided
        effective_gap = gap
        if edges and min_label_gap:
            effective_gap = LayoutEngine.calculate_label_aware_gap(nodes, edges, min_gap=gap)

        if spacing is not None and gap == 0.85:
            total_width = (n - 1) * spacing
            start_x = -total_width / 2.0
            for i, node in enumerate(nodes):
                x = start_x + i * spacing
                node.set_position(x, y, 0.0)
            return effective_gap

        # Dynamic spacing: sum(widths) + (n-1)*effective_gap
        total_width = sum(node.width for node in nodes) + (n - 1) * effective_gap
        current_x = -total_width / 2.0

        for node in nodes:
            center_x = current_x + (node.width / 2.0)
            node.set_position(center_x, y, 0.0)
            current_x += node.width + effective_gap

        return effective_gap

    @staticmethod
    def arrange_vertical(
        nodes: List[Node],
        gap: float = 0.70,
        x: float = 0.0,
        spacing: float = None,
        edges: Optional[List[Edge]] = None,
    ) -> float:
        """Arranges nodes vertically with an exact minimum gap between adjacent borders."""
        n = len(nodes)
        if n == 0:
            return gap

        if spacing is not None and gap == 0.70:
            total_height = (n - 1) * spacing
            start_y = total_height / 2.0
            for i, node in enumerate(nodes):
                y = start_y - i * spacing
                node.set_position(x, y, 0.0)
            return gap

        total_height = sum(node.height for node in nodes) + (n - 1) * gap
        current_y = total_height / 2.0

        for node in nodes:
            center_y = current_y - (node.height / 2.0)
            node.set_position(x, center_y, 0.0)
            current_y -= node.height + gap

        return gap

    @staticmethod
    def arrange_layers(
        layers: List[List[Node]],
        h_gap: float = 1.10,
        v_gap: float = 0.90,
    ) -> None:
        """Arranges nodes in distinct horizontal stages/layers (DAG layout).
        Each column represents a stage, centered along X and each column centered along Y.
        """
        if not layers:
            return

        num_layers = len(layers)
        layer_max_widths = [max((node.width for node in layer), default=1.5) for layer in layers]

        # Calculate total width across layers with h_gap
        total_width = sum(layer_max_widths) + (num_layers - 1) * h_gap
        current_x = -total_width / 2.0

        for layer, max_w in zip(layers, layer_max_widths):
            center_x = current_x + (max_w / 2.0)
            # Arrange nodes in this layer vertically
            LayoutEngine.arrange_vertical(layer, gap=v_gap, x=center_x)
            current_x += max_w + h_gap
