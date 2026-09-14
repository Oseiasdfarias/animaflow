from typing import Dict, Any
from ...core.flow import Flow
from ...core.models import Node, Edge
from ...core.timeline import ActionType


class ManimFlowRenderer:
    """Bridges animaflow declarative models into concrete Manim animations."""

    def __init__(self, flow: Flow):
        self.flow = flow
        self.node_mobjects: Dict[str, Any] = {}
        self.edge_mobjects: Dict[str, Any] = {}

    def build_node_mobject(self, node: Node) -> Any:
        from manim import RoundedRectangle, Text, VGroup, DOWN, DARK_GRAY

        t = self.flow.theme
        rect = RoundedRectangle(
            corner_radius=t.node_corner_radius,
            width=node.width,
            height=node.height,
            color=t.border_color,
            stroke_width=2.5,
            fill_color=t.surface_color,
            fill_opacity=1.0,
        ).move_to(node.position)

        items = []
        title_txt = Text(node.title, font_size=15, color=t.text_color)
        items.append(title_txt)

        if node.subtitle:
            sub_txt = Text(node.subtitle, font_size=11, color=t.text_muted)
            items.append(sub_txt)

        content = VGroup(*items).arrange(DOWN, buff=0.12).move_to(rect.get_center())
        node_group = VGroup(rect, content)
        node_group.rect = rect
        node_group.content = content
        return node_group

    def build_edge_mobject(self, edge: Edge) -> Any:
        from manim import Arrow

        t = self.flow.theme
        src_mob = self.node_mobjects.get(edge.source_id)
        tgt_mob = self.node_mobjects.get(edge.target_id)

        if not src_mob or not tgt_mob:
            return None

        arrow = Arrow(
            src_mob.rect.get_right(),
            tgt_mob.rect.get_left(),
            buff=0.08,
            stroke_width=t.edge_width,
            max_tip_length_to_length_ratio=0.25,
            color=t.border_color,
        )
        return arrow

    def play_on_scene(self, scene: Any) -> None:
        """Executes the timeline on a Manim Scene."""
        from manim import (
            FadeIn,
            Create,
            Dot,
            MoveAlongPath,
            Indicate,
            FadeOut,
        )

        # 1. Build all objects
        for n_id, node in self.flow.nodes.items():
            self.node_mobjects[n_id] = self.build_node_mobject(node)

        for edge in self.flow.edges:
            edge_mob = self.build_edge_mobject(edge)
            if edge_mob:
                self.edge_mobjects[edge.id] = edge_mob

        # 2. Execute timeline
        for action in self.flow.timeline.actions:
            if action.action_type == ActionType.REVEAL_ALL:
                mobs = list(self.node_mobjects.values()) + list(self.edge_mobjects.values())
                scene.play(*[FadeIn(m) for m in mobs], run_time=action.duration)

            elif action.action_type == ActionType.REVEAL_SEQUENCE:
                for node_id in self.flow.nodes:
                    mob = self.node_mobjects[node_id]
                    scene.play(FadeIn(mob), run_time=action.duration)

                for edge_id, edge_mob in self.edge_mobjects.items():
                    scene.play(Create(edge_mob), run_time=action.duration)

            elif action.action_type == ActionType.SEND_PACKET:
                # Find edge connecting source and secondary
                src_mob = self.node_mobjects.get(action.target_id)
                tgt_mob = self.node_mobjects.get(action.secondary_id)
                if src_mob and tgt_mob:
                    t = self.flow.theme
                    dot = Dot(
                        point=src_mob.rect.get_center(),
                        radius=0.08,
                        color=t.accent_color,
                    )
                    from manim import Line
                    path = Line(src_mob.rect.get_right(), tgt_mob.rect.get_left())
                    scene.play(
                        FadeIn(dot),
                        MoveAlongPath(dot, path),
                        run_time=action.duration,
                    )
                    scene.play(FadeOut(dot), run_time=0.2)

            elif action.action_type == ActionType.HIGHLIGHT_NODE:
                mob = self.node_mobjects.get(action.target_id)
                if mob:
                    status = action.params.get("status", "active")
                    color = self.flow.theme.accent_color
                    if status == "alert":
                        color = self.flow.theme.alert_color
                    elif status == "success":
                        color = self.flow.theme.success_color
                    scene.play(Indicate(mob, color=color, scale_factor=1.08), run_time=action.duration)

            elif action.action_type == ActionType.WAIT:
                scene.wait(action.duration)
