from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


class ActionType(str, Enum):
    REVEAL_ALL = "reveal_all"
    REVEAL_SEQUENCE = "reveal_sequence"
    SEND_PACKET = "send_packet"
    HIGHLIGHT_NODE = "highlight_node"
    TRANSITION_NODE = "transition_node"
    WAIT = "wait"


@dataclass
class TimelineAction:
    action_type: ActionType
    target_id: Optional[str] = None
    secondary_id: Optional[str] = None
    duration: float = 1.0
    payload: Optional[str] = None
    params: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_type": self.action_type.value,
            "target_id": self.target_id,
            "secondary_id": self.secondary_id,
            "duration": self.duration,
            "payload": self.payload,
            "params": self.params,
        }


@dataclass
class Timeline:
    """Sequence of animated actions describing the narrative."""

    actions: List[TimelineAction] = field(default_factory=list)

    def reveal_sequence(self, delay_per_item: float = 0.3) -> "Timeline":
        self.actions.append(
            TimelineAction(
                action_type=ActionType.REVEAL_SEQUENCE,
                duration=delay_per_item,
            )
        )
        return self

    def reveal_all(self, duration: float = 0.8) -> "Timeline":
        self.actions.append(
            TimelineAction(
                action_type=ActionType.REVEAL_ALL,
                duration=duration,
            )
        )
        return self

    def send_packet(
        self,
        from_node: Any,
        to_node: Any,
        label: Optional[str] = None,
        duration: float = 1.0,
    ) -> "Timeline":
        src_id = from_node.id if hasattr(from_node, "id") else str(from_node)
        tgt_id = to_node.id if hasattr(to_node, "id") else str(to_node)
        self.actions.append(
            TimelineAction(
                action_type=ActionType.SEND_PACKET,
                target_id=src_id,
                secondary_id=tgt_id,
                payload=label,
                duration=duration,
            )
        )
        return self

    def highlight_node(
        self,
        node: Any,
        status: str = "active",
        duration: float = 0.8,
    ) -> "Timeline":
        n_id = node.id if hasattr(node, "id") else str(node)
        self.actions.append(
            TimelineAction(
                action_type=ActionType.HIGHLIGHT_NODE,
                target_id=n_id,
                duration=duration,
                params={"status": status},
            )
        )
        return self

    def wait(self, seconds: float = 1.0) -> "Timeline":
        self.actions.append(
            TimelineAction(
                action_type=ActionType.WAIT,
                duration=seconds,
            )
        )
        return self

    def to_dict(self) -> Dict[str, Any]:
        return {
            "actions": [a.to_dict() for a in self.actions],
        }
