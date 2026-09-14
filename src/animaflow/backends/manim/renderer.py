from typing import Dict, Any, Optional
from ...core.flow import Flow
from ...core.models import Node, Edge
from ...core.timeline import ActionType


class ManimFlowRenderer:
    """Bridges animaflow declarative models into high-polish Manim animations."""

    def __init__(self, flow: Flow):
        self.flow = flow
        self.node_mobjects: Dict[str, Any] = {}
        self.edge_mobjects: Dict[str, Any] = {}

    def build_node_mobject(self, node: Node) -> Any:
        from manim import RoundedRectangle, Text, VGroup, DOWN

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
        title_txt = Text(
            node.title,
            font="IBM Plex Mono",
            font_size=15,
            color=t.text_color,
            weight="BOLD",
        )
        items.append(title_txt)

        if node.subtitle:
            sub_txt = Text(
                node.subtitle,
                font="IBM Plex Mono",
                font_size=11,
                color=t.text_muted,
            )
            items.append(sub_txt)

        content = VGroup(*items).arrange(DOWN, buff=0.10).move_to(rect.get_center())
        node_group = VGroup(rect, content)
        node_group.rect = rect
        node_group.content = content
        return node_group

    def build_edge_mobject(self, edge: Edge) -> Any:
        from manim import Arrow, CurvedArrow, Text, VGroup, UP, DOWN

        t = self.flow.theme
        src_mob = self.node_mobjects.get(edge.source_id)
        tgt_mob = self.node_mobjects.get(edge.target_id)

        if not src_mob or not tgt_mob:
            return None

        # Detect if target is immediately adjacent or jumping over a node
        src_pos = src_mob.rect.get_center()
        tgt_pos = tgt_mob.rect.get_center()
        dx = tgt_pos[0] - src_pos[0]
        dy = tgt_pos[1] - src_pos[1]

        # Standard direct arrow if adjacent
        if abs(dy) < 0.1 and abs(dx) < 2.5:
            arrow = Arrow(
                src_mob.rect.get_right(),
                tgt_mob.rect.get_left(),
                buff=0.08,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.22,
                color=t.border_color,
            )
            if edge.label:
                lbl = Text(
                    edge.label,
                    font="IBM Plex Mono",
                    font_size=10,
                    color=t.text_muted,
                ).next_to(arrow, UP, buff=0.08)
                group = VGroup(arrow, lbl)
                group.arrow = arrow
                group.path = arrow
                return group

            arrow.path = arrow
            return arrow

        # Curved arch if jumping over other nodes
        start_pt = src_mob.rect.get_top()
        end_pt = tgt_mob.rect.get_top()
        arrow = CurvedArrow(
            start_pt,
            end_pt,
            angle=-0.75,
            color=t.accent_color,
            stroke_width=2.5,
        )
        if edge.label:
            lbl = Text(
                edge.label,
                font="IBM Plex Mono",
                font_size=10,
                color=t.accent_color,
            ).next_to(arrow, UP, buff=0.08)
            group = VGroup(arrow, lbl)
            group.arrow = arrow
            group.path = arrow
            return group

        arrow.path = arrow
        return arrow

    def play_on_scene(self, scene: Any) -> None:
        """Executes the timeline on a Manim Scene with visual feedback."""
        from manim import (
            FadeIn,
            Create,
            Dot,
            Line,
            MoveAlongPath,
            Indicate,
            FadeOut,
            Flash,
            NumberPlane,
        )

        t = self.flow.theme

        # Background subtle tech grid
        grid = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-8, 8, 1],
            background_line_style={
                "stroke_color": t.border_color,
                "stroke_width": 1,
                "stroke_opacity": 0.25,
            },
            axis_config={"stroke_opacity": 0},
        )
        grid.set_z_index(-10)
        scene.add(grid)

        # 1. Build all node and edge mobjects
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
                src_mob = self.node_mobjects.get(action.target_id)
                tgt_mob = self.node_mobjects.get(action.secondary_id)
                if src_mob and tgt_mob:
                    # Find corresponding edge object to trace the path
                    edge_match = None
                    for edge in self.flow.edges:
                        if edge.source_id == action.target_id and edge.target_id == action.secondary_id:
                            edge_match = self.edge_mobjects.get(edge.id)
                            break

                    path_obj = getattr(edge_match, "path", None) if edge_match else None
                    if not path_obj:
                        path_obj = Line(src_mob.rect.get_center(), tgt_mob.rect.get_center())

                    dot = Dot(
                        radius=0.10,
                        color=t.accent_color,
                    )
                    scene.play(
                        FadeIn(dot, scale=0.5),
                        MoveAlongPath(dot, path_obj),
                        run_time=action.duration,
                    )
                    scene.play(FadeOut(dot, scale=1.5), run_time=0.15)

            elif action.action_type == ActionType.HIGHLIGHT_NODE:
                mob = self.node_mobjects.get(action.target_id)
                if mob:
                    status = action.params.get("status", "active")
                    color = t.accent_color
                    if status == "alert":
                        color = t.alert_color
                    elif status == "success":
                        color = t.success_color

                    scene.play(
                        mob.rect.animate.set_stroke(color=color, width=3.8),
                        Indicate(mob, color=color, scale_factor=1.06),
                        run_time=action.duration,
                    )
                    scene.play(
                        Flash(mob.rect, color=color, line_length=0.18, num_lines=8),
                        run_time=0.35,
                    )

            elif action.action_type == ActionType.WAIT:
                scene.wait(action.duration)
