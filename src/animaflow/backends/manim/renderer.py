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

    def prepare_and_measure_nodes(self) -> None:
        """Measures exact text bounds and adjusts node widths, edge label sizes and layout before rendering."""
        from manim import Text, VGroup, DOWN

        t = self.flow.theme

        # 1. Calibrate each node width and height based on actual text
        for node in self.flow.nodes.values():
            items = []
            title_txt = Text(
                node.title,
                font="IBM Plex Mono",
                font_size=14,
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

            content = VGroup(*items).arrange(DOWN, buff=0.10)

            padding_h = max(node.padding, 0.45)
            padding_v = max(node.padding * 0.7, 0.35)
            node.width = max(node.min_width, content.width + padding_h * 2)
            node.height = max(node.min_height, content.height + padding_v * 2)

        # 2. Check if nodes already have custom/2D positions or need auto layout
        has_custom_positions = any(n.position != (0.0, 0.0, 0.0) for n in self.flow.nodes.values())
        if not has_custom_positions:
            max_adj_label_width = 0.0
            for edge in self.flow.edges:
                if edge.label:
                    lbl = Text(edge.label, font="IBM Plex Mono", font_size=10)
                    pill_w = lbl.width + 0.20
                    max_adj_label_width = max(max_adj_label_width, pill_w)

            required_gap = max(0.95, max_adj_label_width + 0.35)
            self.flow.auto_layout(mode="horizontal", gap=required_gap, min_label_gap=False)

    def build_node_mobject(self, node: Node) -> Any:
        from manim import RoundedRectangle, Text, VGroup, DOWN

        t = self.flow.theme

        items = []
        title_txt = Text(
            node.title,
            font="IBM Plex Mono",
            font_size=14,
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

        content = VGroup(*items).arrange(DOWN, buff=0.10)

        rect = RoundedRectangle(
            corner_radius=t.node_corner_radius,
            width=node.width,
            height=node.height,
            color=t.border_color,
            stroke_width=2.5,
            fill_color=t.surface_color,
            fill_opacity=1.0,
        ).move_to(node.position)

        content.move_to(rect.get_center())

        node_group = VGroup(rect, content)
        node_group.rect = rect
        node_group.content = content
        return node_group

    def build_edge_mobject(self, edge: Edge) -> Any:
        from manim import Arrow, CurvedArrow, Text, VGroup, UP, DOWN, LEFT, RIGHT, RoundedRectangle

        t = self.flow.theme
        src_mob = self.node_mobjects.get(edge.source_id)
        tgt_mob = self.node_mobjects.get(edge.target_id)

        if not src_mob or not tgt_mob:
            return None

        src_pos = src_mob.rect.get_center()
        tgt_pos = tgt_mob.rect.get_center()
        dx = tgt_pos[0] - src_pos[0]
        dy = tgt_pos[1] - src_pos[1]

        # Case 1: Pure horizontal adjacent
        if abs(dy) < 0.2 and abs(dx) < 3.8:
            start_p = src_mob.rect.get_right() if dx > 0 else src_mob.rect.get_left()
            end_p = tgt_mob.rect.get_left() if dx > 0 else tgt_mob.rect.get_right()
            arrow = Arrow(
                start_p,
                end_p,
                buff=0.08,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.22,
                color=t.border_color,
            )
            return self._wrap_edge_label(arrow, edge.label, t, UP, 0.10)

        # Case 2: Pure vertical connection
        if abs(dx) < 0.2:
            start_p = src_mob.rect.get_bottom() if dy < 0 else src_mob.rect.get_top()
            end_p = tgt_mob.rect.get_top() if dy < 0 else tgt_mob.rect.get_bottom()
            arrow = Arrow(
                start_p,
                end_p,
                buff=0.08,
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.22,
                color=t.border_color,
            )
            return self._wrap_edge_label(arrow, edge.label, t, RIGHT, 0.10)

        # Case 3: Horizontal jump over intermediate node (e.g. Gateway -> LLM)
        if abs(dy) < 0.2 and abs(dx) >= 3.8:
            start_pt = src_mob.rect.get_top()
            end_pt = tgt_mob.rect.get_top()
            arrow = CurvedArrow(
                start_pt,
                end_pt,
                angle=-0.80,
                color=t.accent_color,
                stroke_width=2.5,
            )
            return self._wrap_edge_label(
                arrow, edge.label, t, UP, 0.12, is_accent=True, use_proportion=True
            )

        # Case 4: Diagonal / Branch connection (e.g., Orchestrator -> Code / Search)
        import numpy as np

        start_p = src_mob.rect.get_right() if dx > 0 else src_mob.rect.get_left()
        end_p = tgt_mob.rect.get_left() if dx > 0 else tgt_mob.rect.get_right()

        arrow = Arrow(
            start_p,
            end_p,
            buff=0.08,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.22,
            color=t.border_color,
        )

        # Compute normal vector to arrow direction for label offset
        vec = np.array([end_p[0] - start_p[0], end_p[1] - start_p[1], 0.0])
        norm = np.linalg.norm(vec)
        if norm > 1e-4:
            unit_vec = vec / norm
            # Normal vector pointing outward (+Y if going right & up, -Y if going right & down)
            if dy > 0:
                perp = np.array([-unit_vec[1], unit_vec[0], 0.0])
                if perp[1] < 0:
                    perp = -perp
            else:
                perp = np.array([unit_vec[1], -unit_vec[0], 0.0])
                if perp[1] > 0:
                    perp = -perp
        else:
            perp = np.array([0.0, 1.0, 0.0])

        return self._wrap_edge_label(arrow, edge.label, t, perp, 0.18, use_proportion=True)

    def _wrap_edge_label(
        self,
        arrow: Any,
        label_text: Optional[str],
        theme: Any,
        direction: Any,
        buff: float,
        is_accent: bool = False,
        use_proportion: bool = False,
    ) -> Any:
        from manim import Text, VGroup, RoundedRectangle

        if not label_text:
            arrow.path = arrow
            return arrow

        color = theme.accent_color if is_accent else theme.text_muted
        border_col = theme.accent_color if is_accent else theme.border_color

        lbl_txt = Text(
            label_text,
            font="IBM Plex Mono",
            font_size=10,
            color=color,
        )
        pill = RoundedRectangle(
            corner_radius=0.06,
            width=lbl_txt.width + 0.18,
            height=lbl_txt.height + 0.10,
            fill_color=theme.bg_color,
            fill_opacity=0.95,
            stroke_color=border_col,
            stroke_width=1.0 if not is_accent else 1.2,
        )

        if use_proportion:
            pill.move_to(arrow.point_from_proportion(0.50)).shift(direction * buff)
        else:
            pill.next_to(arrow, direction, buff=buff)

        lbl_txt.move_to(pill.get_center())
        lbl_group = VGroup(pill, lbl_txt)

        group = VGroup(arrow, lbl_group)
        group.arrow = arrow
        group.path = arrow
        group.label = lbl_group
        return group

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
            VGroup,
        )

        t = self.flow.theme

        # 0. Measure exact text bounds and recalibrate positions
        self.prepare_and_measure_nodes()

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
                    edge_match = None
                    for edge in self.flow.edges:
                        if (
                            edge.source_id == action.target_id
                            and edge.target_id == action.secondary_id
                        ):
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

            elif action.action_type == ActionType.STREAM_PACKETS:
                import numpy as np

                # Determine paths to animate (single edge or all edges)
                target_paths = []
                if action.target_id and action.secondary_id:
                    for edge in self.flow.edges:
                        if (
                            edge.source_id == action.target_id
                            and edge.target_id == action.secondary_id
                        ):
                            edge_match = self.edge_mobjects.get(edge.id)
                            p = getattr(edge_match, "path", None) if edge_match else None
                            if p:
                                target_paths.append(p)
                            break
                    if not target_paths:
                        src_mob = self.node_mobjects.get(action.target_id)
                        tgt_mob = self.node_mobjects.get(action.secondary_id)
                        if src_mob and tgt_mob:
                            target_paths.append(Line(src_mob.rect.get_center(), tgt_mob.rect.get_center()))
                else:
                    # Animate all edges in the diagram simultaneously
                    for edge in self.flow.edges:
                        edge_match = self.edge_mobjects.get(edge.id)
                        p = getattr(edge_match, "path", None) if edge_match else None
                        if p:
                            target_paths.append(p)

                if target_paths:
                    count = int(action.params.get("count", 5))
                    speed = float(action.params.get("speed", 0.65))
                    color = action.params.get("color") or t.accent_color

                    all_particles = []

                    def make_group_updater(stream_list):

                        def updater(mob, dt):
                            for p_obj, dots in stream_list:
                                for d in dots:
                                    d.phase = (d.phase + dt * speed) % 1.0
                                    d.move_to(p_obj.point_from_proportion(d.phase))
                                    # Smooth bell-curve fade in at start, fade out at end
                                    d.set_opacity(max(0.0, np.sin(d.phase * np.pi)))
                        return updater

                    streams = []
                    for path_obj in target_paths:
                        path_dots = []
                        for i in range(count):
                            d = Dot(radius=0.08, color=color)
                            d.phase = i / count
                            d.move_to(path_obj.point_from_proportion(d.phase))
                            d.set_opacity(np.sin(d.phase * np.pi))
                            path_dots.append(d)
                            all_particles.append(d)
                        streams.append((path_obj, path_dots))

                    particle_group = VGroup(*all_particles)
                    group_updater = make_group_updater(streams)
                    particle_group.add_updater(group_updater)
                    scene.add(particle_group)

                    scene.wait(action.duration)

                    particle_group.clear_updaters()
                    scene.play(FadeOut(particle_group), run_time=0.20)
                    scene.remove(particle_group)



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
