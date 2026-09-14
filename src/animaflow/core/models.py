from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
import uuid


class NodeShape(str, Enum):
    ROUNDED_RECT = "rounded_rect"
    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    DATABASE = "database"


class NodeStatus(str, Enum):
    DEFAULT = "default"
    ACTIVE = "active"
    ALERT = "alert"
    SUCCESS = "success"
    MUTED = "muted"


@dataclass
class Node:
    """Semantic representation of a flowchart node."""
    title: str
    subtitle: Optional[str] = None
    icon: Optional[str] = None
    shape: NodeShape = NodeShape.ROUNDED_RECT
    status: NodeStatus = NodeStatus.DEFAULT
    width: float = 1.6
    height: float = 1.3
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    metadata: Dict[str, Any] = field(default_factory=dict)

    def set_position(self, x: float, y: float, z: float = 0.0) -> "Node":
        self.position = (x, y, z)
        return self

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "icon": self.icon,
            "shape": self.shape.value,
            "status": self.status.value,
            "width": self.width,
            "height": self.height,
            "position": list(self.position),
            "metadata": self.metadata,
        }


class EdgeStyle(str, Enum):
    SOLID = "solid"
    DASHED = "dashed"
    CURVED = "curved"
    ORTHOGONAL = "orthogonal"


@dataclass
class Edge:
    """Directed connection between two nodes."""
    source_id: str
    target_id: str
    label: Optional[str] = None
    style: EdgeStyle = EdgeStyle.SOLID
    animated_packet: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "label": self.label,
            "style": self.style.value,
            "animated_packet": self.animated_packet,
            "metadata": self.metadata,
        }
