from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class Theme:
    """Visual theme settings for nodes, edges and canvas."""

    name: str = "DarkTerminal"
    bg_color: str = "#0E1015"
    surface_color: str = "#161920"
    border_color: str = "#2C313C"
    text_color: str = "#FFFFFF"
    text_muted: str = "#8B949E"
    accent_color: str = "#F59E0B"
    alert_color: str = "#EF4444"
    success_color: str = "#10B981"
    font_mono: str = "monospace"
    font_sans: str = "sans-serif"
    node_corner_radius: float = 0.12
    edge_width: float = 2.5

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
