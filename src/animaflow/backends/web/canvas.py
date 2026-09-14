import json
from ...core.flow import Flow


class WebCanvasExporter:
    """Exports an animaflow diagram into a standalone, interactive HTML5 Canvas/SVG page."""

    @staticmethod
    def to_html(flow: Flow, output_path: str) -> str:
        data_json = json.dumps(flow.to_dict(), indent=2)
        t = flow.theme

        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{flow.title or "animaflow.io - Interactive Flow"}</title>
  <style>
    body {{
      margin: 0;
      padding: 0;
      background: {t.bg_color};
      color: {t.text_color};
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      overflow: hidden;
    }}
    .header {{
      margin-bottom: 20px;
      text-align: center;
    }}
    .header h1 {{
      font-size: 20px;
      margin: 0;
      font-weight: 600;
    }}
    .badge {{
      display: inline-block;
      margin-top: 6px;
      padding: 3px 10px;
      background: {t.surface_color};
      border: 1px solid {t.border_color};
      border-radius: 12px;
      font-size: 11px;
      color: {t.accent_color};
      font-family: monospace;
    }}
    #canvas-container {{
      position: relative;
      width: 900px;
      height: 500px;
      background: {t.surface_color};
      border: 1px solid {t.border_color};
      border-radius: 16px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.5);
      overflow: hidden;
    }}
    svg {{
      width: 100%;
      height: 100%;
    }}
    .node-rect {{
      fill: {t.bg_color};
      stroke: {t.border_color};
      stroke-width: 2;
      rx: 12px;
      transition: all 0.3s ease;
    }}
    .node-rect:hover {{
      stroke: {t.accent_color};
      transform: translateY(-2px);
    }}
    .controls {{
      margin-top: 20px;
      display: flex;
      gap: 12px;
    }}
    button {{
      background: {t.accent_color};
      color: {t.bg_color};
      border: none;
      padding: 8px 18px;
      border-radius: 8px;
      font-weight: 600;
      cursor: pointer;
      font-size: 13px;
      transition: opacity 0.2s;
    }}
    button:hover {{
      opacity: 0.9;
    }}
  </style>
</head>
<body>
  <div class="header">
    <h1>{flow.title or "animaflow Diagram"}</h1>
    <div class="badge">animaflow.io &bull; Interactive Web Canvas</div>
  </div>

  <div id="canvas-container">
    <svg id="flow-svg"></svg>
  </div>

  <div class="controls">
    <button onclick="playAnimation()">▶ Play Animation</button>
    <button onclick="resetFlow()">↺ Reset</button>
  </div>

  <script>
    const flowData = {data_json};
    const svg = document.getElementById("flow-svg");
    const W = 900;
    const H = 500;

    function renderDiagram() {{
      svg.innerHTML = `
        <defs>
          <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="{t.border_color}" />
          </marker>
        </defs>
      `;

      // Render Edges
      flowData.edges.forEach(edge => {{
        const src = flowData.nodes.find(n => n.id === edge.source_id);
        const tgt = flowData.nodes.find(n => n.id === edge.target_id);
        if (src && tgt) {{
          const x1 = W/2 + src.position[0] * 120 + 80;
          const y1 = H/2 - src.position[1] * 120;
          const x2 = W/2 + tgt.position[0] * 120 - 80;
          const y2 = H/2 - tgt.position[1] * 120;

          const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
          line.setAttribute("x1", x1);
          line.setAttribute("y1", y1);
          line.setAttribute("x2", x2);
          line.setAttribute("y2", y2);
          line.setAttribute("stroke", "{t.border_color}");
          line.setAttribute("stroke-width", "2");
          line.setAttribute("marker-end", "url(#arrow)");
          svg.appendChild(line);
        }}
      }});

      // Render Nodes
      flowData.nodes.forEach(node => {{
        const cx = W/2 + node.position[0] * 120;
        const cy = H/2 - node.position[1] * 120;
        const nw = 140;
        const nh = 80;

        const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        g.setAttribute("id", "node-" + node.id);

        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("x", cx - nw/2);
        rect.setAttribute("y", cy - nh/2);
        rect.setAttribute("width", nw);
        rect.setAttribute("height", nh);
        rect.setAttribute("class", "node-rect");
        g.appendChild(rect);

        const title = document.createElementNS("http://www.w3.org/2000/svg", "text");
        title.setAttribute("x", cx);
        title.setAttribute("y", cy - 5);
        title.setAttribute("text-anchor", "middle");
        title.setAttribute("fill", "{t.text_color}");
        title.setAttribute("font-size", "14");
        title.setAttribute("font-weight", "600");
        title.textContent = node.title;
        g.appendChild(title);

        if (node.subtitle) {{
          const sub = document.createElementNS("http://www.w3.org/2000/svg", "text");
          sub.setAttribute("x", cx);
          sub.setAttribute("y", cy + 16);
          sub.setAttribute("text-anchor", "middle");
          sub.setAttribute("fill", "{t.text_muted}");
          sub.setAttribute("font-size", "11");
          sub.textContent = node.subtitle;
          g.appendChild(sub);
        }}

        svg.appendChild(g);
      }});
    }}

    function playAnimation() {{
      // Packet animation example along edges
      flowData.edges.forEach((edge, idx) => {{
        const src = flowData.nodes.find(n => n.id === edge.source_id);
        const tgt = flowData.nodes.find(n => n.id === edge.target_id);
        if (src && tgt) {{
          const x1 = W/2 + src.position[0] * 120 + 70;
          const y1 = H/2 - src.position[1] * 120;
          const x2 = W/2 + tgt.position[0] * 120 - 70;
          const y2 = H/2 - tgt.position[1] * 120;

          const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
          circle.setAttribute("r", "5");
          circle.setAttribute("fill", "{t.accent_color}");
          circle.setAttribute("cx", x1);
          circle.setAttribute("cy", y1);
          svg.appendChild(circle);

          const anim = circle.animate([
            {{ cx: x1, cy: y1, opacity: 0 }},
            {{ opacity: 1, offset: 0.1 }},
            {{ cx: x2, cy: y2, opacity: 1, offset: 0.9 }},
            {{ cx: x2, cy: y2, opacity: 0 }}
          ], {{
            duration: 1200,
            delay: idx * 800,
            fill: "forwards"
          }});

          anim.onfinish = () => circle.remove();
        }}
      }});
    }}

    function resetFlow() {{
      renderDiagram();
    }}

    renderDiagram();
  </script>
</body>
</html>
"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_template)
        return output_path
