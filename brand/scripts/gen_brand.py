#!/usr/bin/env python3
"""Gera o pacote oficial de identidade visual do animaflow com a paleta Nordic Sage & Carbon.

PALETA: 3. Nordic Sage & Carbon (Design Nórdico)
  - Dark Canvas (Carvão Mineral): #121619
  - Dark Surface / Card:          #1A2024
  - Dark Border:                  #242D33
  - Sage Claro (Nó Acento):       #9EC8B9
  - Jade Técnico (Linhas/Fluxo):  #5C9E89
  - Sage Gélido (Partículas):     #D7EBE3
  - Papel Claro (Light Theme):    #F2F6F4
  - Linha/Tinta (Light Theme):    #37594E / #162420
"""

import os
import sys
import math
import cairo
from text2path import text_to_path
from fontTools.ttLib import TTFont
from fontTools.pens.cairoPen import CairoPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG_DIR = os.path.join(ROOT, "svg")
PNG_DIR = os.path.join(ROOT, "png")
FONT_PATH = "/usr/share/fonts/truetype/ibm-plex/IBMPlexSans-SemiBold.ttf"

os.makedirs(SVG_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)

# Cores em Hex
HEX_DARK_BG = "#121619"
HEX_DARK_SURFACE = "#1A2024"
HEX_DARK_BORDER = "#242D33"
HEX_SAGE_LIGHT = "#9EC8B9"
HEX_SAGE_ICE = "#D7EBE3"
HEX_JADE = "#5C9E89"
HEX_LIGHT_BG = "#F2F6F4"
HEX_LIGHT_INK = "#162420"
HEX_LIGHT_STROKE = "#37594E"
HEX_LIGHT_ACCENT = "#4B7769"

# RGB Tuples
RGB_DARK_BG = (0.071, 0.086, 0.098)
RGB_DARK_SURFACE = (0.102, 0.125, 0.141)
RGB_DARK_BORDER = (0.141, 0.176, 0.200)
RGB_SAGE_LIGHT = (0.620, 0.784, 0.725)
RGB_SAGE_ICE = (0.843, 0.922, 0.890)
RGB_JADE = (0.361, 0.620, 0.537)
RGB_LIGHT_BG = (0.949, 0.965, 0.957)
RGB_LIGHT_INK = (0.086, 0.141, 0.125)
RGB_LIGHT_STROKE = (0.216, 0.349, 0.306)
RGB_LIGHT_ACCENT = (0.294, 0.467, 0.412)

LOOP_PATH_D = (
    "M 36 42 "
    "C 48 24, 72 24, 84 42 "
    "C 96 60, 80 84, 60 88 "
    "C 40 92, 24 60, 36 42 Z"
)

def get_symbol_svg(mode="dark"):
    """
    Retorna os elementos vetoriais SVG no viewBox 0 0 120 120.
    mode: 'dark' (para fundo escuro), 'light' (para fundo claro), 'mono' (currentColor)
    """
    if mode == "dark":
        stroke = HEX_JADE
        n_a = HEX_SAGE_LIGHT
        n_b = HEX_SAGE_ICE
        n_c = HEX_JADE
        core = HEX_DARK_BG
        p_color = HEX_SAGE_ICE
    elif mode == "light":
        stroke = HEX_LIGHT_STROKE
        n_a = HEX_LIGHT_INK
        n_b = HEX_LIGHT_ACCENT
        n_c = HEX_LIGHT_INK
        core = HEX_LIGHT_BG
        p_color = HEX_LIGHT_ACCENT
    elif mode == "mono":
        stroke = "currentColor"
        n_a = n_b = n_c = p_color = "currentColor"
        core = "rgba(0,0,0,0.1)"

    return f"""<g id="flow_symbol">
    <path d="{LOOP_PATH_D}" fill="none" stroke="{stroke}" stroke-width="7.2" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="60" cy="29.5" r="3.8" fill="{p_color}"/>
    <circle cx="78" cy="74" r="3.4" fill="{p_color}"/>
    <circle cx="37" cy="68" r="3.0" fill="{p_color}"/>
    <!-- Nó A (Esquerda-Topo) -->
    <circle cx="36" cy="42" r="10.5" fill="{n_a}"/>
    <circle cx="36" cy="42" r="4.5" fill="{core}"/>
    <!-- Nó B (Direita-Topo) -->
    <circle cx="84" cy="42" r="10.5" fill="{n_b}"/>
    <circle cx="84" cy="42" r="4.5" fill="{core}"/>
    <!-- Nó C (Base) -->
    <circle cx="60" cy="88" r="9.5" fill="{n_c}"/>
    <circle cx="60" cy="88" r="4.0" fill="{core}"/>
  </g>"""

def generate_svgs():
    print("-> Gerando arquivos SVG (Nordic Sage & Carbon)...")

    # 1. Ícones
    with open(os.path.join(SVG_DIR, "icone.svg"), "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120">\n  {get_symbol_svg("dark")}\n</svg>')

    with open(os.path.join(SVG_DIR, "icone-solido.svg"), "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120">\n  {get_symbol_svg("light")}\n</svg>')

    with open(os.path.join(SVG_DIR, "icone-mono.svg"), "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120">\n  {get_symbol_svg("mono")}\n</svg>')

    # 2. Favicon
    fav_dark = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <rect width="32" height="32" rx="7" fill="{HEX_DARK_BG}"/>
  <path d="M 10 11 C 13 6, 19 6, 22 11 C 25 16, 21 22, 16 23 C 11 24, 7 16, 10 11 Z" fill="none" stroke="{HEX_JADE}" stroke-width="2.6" stroke-linecap="round"/>
  <circle cx="10" cy="11" r="3.2" fill="{HEX_SAGE_LIGHT}"/>
  <circle cx="22" cy="11" r="3.2" fill="{HEX_SAGE_ICE}"/>
  <circle cx="16" cy="23" r="2.8" fill="{HEX_JADE}"/>
  <circle cx="16" cy="7.8" r="1.3" fill="{HEX_SAGE_ICE}"/>
</svg>"""
    with open(os.path.join(SVG_DIR, "favicon.svg"), "w") as f:
        f.write(fav_dark)

    fav_light = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32">
  <rect width="32" height="32" rx="7" fill="{HEX_LIGHT_BG}"/>
  <path d="M 10 11 C 13 6, 19 6, 22 11 C 25 16, 21 22, 16 23 C 11 24, 7 16, 10 11 Z" fill="none" stroke="{HEX_LIGHT_STROKE}" stroke-width="2.6" stroke-linecap="round"/>
  <circle cx="10" cy="11" r="3.2" fill="{HEX_LIGHT_INK}"/>
  <circle cx="22" cy="11" r="3.2" fill="{HEX_LIGHT_ACCENT}"/>
  <circle cx="16" cy="23" r="2.8" fill="{HEX_LIGHT_INK}"/>
</svg>"""
    with open(os.path.join(SVG_DIR, "favicon-branco.svg"), "w") as f:
        f.write(fav_light)

    # 3. Logos Horizontais
    font_size = 56.0
    d_text, text_w, text_asc, text_desc, cap_h = text_to_path(FONT_PATH, "animaflow", font_size)
    y_baseline = 60.0 + (cap_h / 2.0)
    total_w = 120.0 + 20.0 + text_w + 10.0

    with open(os.path.join(SVG_DIR, "logo-horizontal.svg"), "w") as f:
        f.write(f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w:.1f} 120" width="{total_w:.1f}" height="120">
  {get_symbol_svg("dark")}
  <g transform="translate(140, {y_baseline:.1f})" fill="{HEX_SAGE_ICE}">
    <path d="{d_text}" />
  </g>
</svg>""")

    with open(os.path.join(SVG_DIR, "logo-horizontal-solido.svg"), "w") as f:
        f.write(f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w:.1f} 120" width="{total_w:.1f}" height="120">
  {get_symbol_svg("light")}
  <g transform="translate(140, {y_baseline:.1f})" fill="{HEX_LIGHT_INK}">
    <path d="{d_text}" />
  </g>
</svg>""")

    with open(os.path.join(SVG_DIR, "logo-horizontal-mono.svg"), "w") as f:
        f.write(f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w:.1f} 120" width="{total_w:.1f}" height="120">
  {get_symbol_svg("mono")}
  <g transform="translate(140, {y_baseline:.1f})" fill="currentColor">
    <path d="{d_text}" />
  </g>
</svg>""")

    # 4. Logos Verticais
    v_total_w = max(160.0, text_w + 30.0)
    icon_offset_x = (v_total_w - 120.0) / 2.0
    text_offset_x = (v_total_w - text_w) / 2.0
    v_text_baseline = 120.0 + 18.0 + cap_h
    v_total_h = v_text_baseline + abs(text_desc) + 15.0

    with open(os.path.join(SVG_DIR, "logo-vertical.svg"), "w") as f:
        f.write(f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {v_total_w:.1f} {v_total_h:.1f}" width="{v_total_w:.1f}" height="{v_total_h:.1f}">
  <g transform="translate({icon_offset_x:.1f}, 0)">
    {get_symbol_svg("dark")}
  </g>
  <g transform="translate({text_offset_x:.1f}, {v_text_baseline:.1f})" fill="{HEX_SAGE_ICE}">
    <path d="{d_text}" />
  </g>
</svg>""")

    with open(os.path.join(SVG_DIR, "logo-vertical-solido.svg"), "w") as f:
        f.write(f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {v_total_w:.1f} {v_total_h:.1f}" width="{v_total_w:.1f}" height="{v_total_h:.1f}">
  <g transform="translate({icon_offset_x:.1f}, 0)">
    {get_symbol_svg("light")}
  </g>
  <g transform="translate({text_offset_x:.1f}, {v_text_baseline:.1f})" fill="{HEX_LIGHT_INK}">
    <path d="{d_text}" />
  </g>
</svg>""")

    # 5. Banner Hero SVG
    with open(os.path.join(SVG_DIR, "banner-hero.svg"), "w") as f:
        f.write(f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 640" width="1280" height="640">
  <rect width="1280" height="640" fill="{HEX_DARK_BG}"/>

  <!-- Grade técnica minimalista nórdica -->
  <g opacity="0.05" stroke="{HEX_SAGE_LIGHT}" stroke-width="1">
    <line x1="0" y1="80" x2="1280" y2="80"/>
    <line x1="0" y1="160" x2="1280" y2="160"/>
    <line x1="0" y1="240" x2="1280" y2="240"/>
    <line x1="0" y1="320" x2="1280" y2="320"/>
    <line x1="0" y1="400" x2="1280" y2="400"/>
    <line x1="0" y1="480" x2="1280" y2="480"/>
    <line x1="0" y1="560" x2="1280" y2="560"/>

    <line x1="160" y1="0" x2="160" y2="640"/>
    <line x1="320" y1="0" x2="320" y2="640"/>
    <line x1="480" y1="0" x2="480" y2="640"/>
    <line x1="640" y1="0" x2="640" y2="640"/>
    <line x1="800" y1="0" x2="800" y2="640"/>
    <line x1="960" y1="0" x2="960" y2="640"/>
    <line x1="1120" y1="0" x2="1120" y2="640"/>
  </g>

  <!-- Símbolo animaflow -->
  <g transform="translate(560, 95) scale(1.35)">
    {get_symbol_svg("dark")}
  </g>

  <!-- Tipografia: animaflow -->
  <g transform="translate({(1280 - text_w * 2.0)/2.0:.1f}, 390) scale(2.0)" fill="{HEX_SAGE_ICE}">
    <path d="{d_text}" />
  </g>

  <!-- Subtítulo -->
  <text x="640" y="450" text-anchor="middle" font-family="'IBM Plex Sans', sans-serif" font-size="22" font-weight="400" fill="{HEX_SAGE_LIGHT}" letter-spacing="1.2">
    Declarative Animated Architecture Diagrams &amp; Flowcharts in Python
  </text>

  <!-- Badges técnicos no rodapé -->
  <g transform="translate(420, 505)">
    <rect x="0" y="0" width="130" height="34" rx="6" fill="{HEX_DARK_SURFACE}" stroke="{HEX_DARK_BORDER}" stroke-width="1.2"/>
    <text x="65" y="22" text-anchor="middle" font-family="'IBM Plex Sans', sans-serif" font-size="13" font-weight="600" fill="{HEX_SAGE_LIGHT}">Manim CE</text>

    <rect x="150" y="0" width="140" height="34" rx="6" fill="{HEX_DARK_SURFACE}" stroke="{HEX_DARK_BORDER}" stroke-width="1.2"/>
    <text x="220" y="22" text-anchor="middle" font-family="'IBM Plex Sans', sans-serif" font-size="13" font-weight="600" fill="{HEX_SAGE_ICE}">HTML / SVG</text>

    <rect x="310" y="0" width="130" height="34" rx="6" fill="{HEX_DARK_SURFACE}" stroke="{HEX_DARK_BORDER}" stroke-width="1.2"/>
    <text x="375" y="22" text-anchor="middle" font-family="'IBM Plex Sans', sans-serif" font-size="13" font-weight="600" fill="{HEX_JADE}">Python 3.10+</text>
  </g>
</svg>""")

    print("✓ Todos os SVGs foram gerados!")

def draw_cairo_symbol(ctx, mode="dark", scale=1.0):
    ctx.save()
    ctx.scale(scale, scale)

    if mode == "dark":
        col_stroke = RGB_JADE
        col_nodes = [RGB_SAGE_LIGHT, RGB_SAGE_ICE, RGB_JADE]
        col_core = RGB_DARK_BG
        col_part = RGB_SAGE_ICE
    else:
        col_stroke = RGB_LIGHT_STROKE
        col_nodes = [RGB_LIGHT_INK, RGB_LIGHT_ACCENT, RGB_LIGHT_INK]
        col_core = RGB_LIGHT_BG
        col_part = RGB_LIGHT_ACCENT

    # Loop
    ctx.new_path()
    ctx.move_to(36, 42)
    ctx.curve_to(48, 24, 72, 24, 84, 42)
    ctx.curve_to(96, 60, 80, 84, 60, 88)
    ctx.curve_to(40, 92, 24, 60, 36, 42)
    ctx.close_path()
    ctx.set_line_width(7.2)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_source_rgb(*col_stroke)
    ctx.stroke()

    # Partículas
    for px, py, pr in [(60, 29.5, 3.8), (78, 74, 3.4), (37, 68, 3.0)]:
        ctx.new_path()
        ctx.arc(px, py, pr, 0, 2*math.pi)
        ctx.set_source_rgb(*col_part)
        ctx.fill()

    # 3 Nós
    nodes = [(36, 42, 10.5, 4.5), (84, 42, 10.5, 4.5), (60, 88, 9.5, 4.0)]
    for i, (nx, ny, ro, ri) in enumerate(nodes):
        ctx.new_path()
        ctx.arc(nx, ny, ro, 0, 2*math.pi)
        ctx.set_source_rgb(*col_nodes[i])
        ctx.fill()
        ctx.new_path()
        ctx.arc(nx, ny, ri, 0, 2*math.pi)
        ctx.set_source_rgb(*col_core)
        ctx.fill()

    ctx.restore()

def draw_cairo_text(ctx, text, x, y, size, color_rgb):
    font = TTFont(FONT_PATH)
    upem = font["head"].unitsPerEm
    scale = size / upem
    cmap = font.getBestCmap()
    glyphset = font.getGlyphSet()
    hmtx = font["hmtx"]

    cur_x = x
    ctx.save()
    ctx.set_source_rgb(*color_rgb)
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            cur_x += size * 0.3
            continue
        ctx.save()
        ctx.translate(cur_x, y)
        ctx.scale(scale, -scale)
        pen = CairoPen(glyphset, ctx)
        glyphset[gname].draw(pen)
        ctx.fill()
        ctx.restore()
        cur_x += hmtx[gname][0] * scale
    ctx.restore()

def rasterize_all_cairo():
    print("-> Rasterizando PNGs nórdicos de alta resolução com PyCairo...")

    # 1. Ícones (1024, 512, 256, 128, 64)
    for px in [1024, 512, 256, 128, 64]:
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, px, px)
        ctx = cairo.Context(surface)
        draw_cairo_symbol(ctx, "dark", scale=px/120.0)
        surface.write_to_png(os.path.join(PNG_DIR, f"icone-{px}.png"))
        print(f"  ✓ icone-{px}.png")

    # Ícone sólido escuro e sólido branco (512)
    for name, mode in [("icone-solido-512.png", "light"), ("icone-solido-branco-512.png", "dark")]:
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 512, 512)
        ctx = cairo.Context(surface)
        draw_cairo_symbol(ctx, mode, scale=512/120.0)
        surface.write_to_png(os.path.join(PNG_DIR, name))
        print(f"  ✓ {name}")

    # 2. Favicons (180, 64, 32, 16)
    for fsize in [180, 64, 32, 16]:
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, fsize, fsize)
        ctx = cairo.Context(surface)
        r = fsize * 0.22
        ctx.new_sub_path()
        ctx.arc(fsize - r, r, r, -math.pi/2, 0)
        ctx.arc(fsize - r, fsize - r, r, 0, math.pi/2)
        ctx.arc(r, fsize - r, r, math.pi/2, math.pi)
        ctx.arc(r, r, r, math.pi, 3*math.pi/2)
        ctx.close_path()
        ctx.set_source_rgb(*RGB_DARK_BG)
        ctx.fill()

        s = fsize / 32.0
        ctx.save()
        ctx.scale(s, s)
        ctx.move_to(10, 11)
        ctx.curve_to(13, 6, 19, 6, 22, 11)
        ctx.curve_to(25, 16, 21, 22, 16, 23)
        ctx.curve_to(11, 24, 7, 16, 10, 11)
        ctx.close_path()
        ctx.set_line_width(2.6)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgb(*RGB_JADE)
        ctx.stroke()

        ctx.arc(10, 11, 3.2, 0, 2*math.pi); ctx.set_source_rgb(*RGB_SAGE_LIGHT); ctx.fill()
        ctx.arc(22, 11, 3.2, 0, 2*math.pi); ctx.set_source_rgb(*RGB_SAGE_ICE); ctx.fill()
        ctx.arc(16, 23, 2.8, 0, 2*math.pi); ctx.set_source_rgb(*RGB_JADE); ctx.fill()
        ctx.arc(16, 7.8, 1.3, 0, 2*math.pi); ctx.set_source_rgb(*RGB_SAGE_ICE); ctx.fill()
        ctx.restore()

        surface.write_to_png(os.path.join(PNG_DIR, f"favicon-{fsize}.png"))
        print(f"  ✓ favicon-{fsize}.png")

    # 3. Logo Horizontal (1600 e 800)
    font_size = 56.0
    _, text_w, _, _, cap_h = text_to_path(FONT_PATH, "animaflow", font_size)
    base_w = 120.0 + 20.0 + text_w + 10.0
    base_h = 120.0
    y_baseline = 60.0 + (cap_h / 2.0)

    for target_w in [1600, 800]:
        scale = target_w / base_w
        target_h = int(base_h * scale)

        # Versão Dark (fundo transparente, tipografia Sage Ice)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, target_w, target_h)
        ctx = cairo.Context(surface)
        ctx.scale(scale, scale)
        draw_cairo_symbol(ctx, "dark", scale=1.0)
        draw_cairo_text(ctx, "animaflow", 140, y_baseline, font_size, RGB_SAGE_ICE)
        surface.write_to_png(os.path.join(PNG_DIR, f"logo-horizontal-{target_w}.png"))

        # Versão Light / Sólido (para fundos claros, tipografia Dark Ink)
        if target_w == 800:
            surface_s = cairo.ImageSurface(cairo.FORMAT_ARGB32, target_w, target_h)
            ctx_s = cairo.Context(surface_s)
            ctx_s.scale(scale, scale)
            draw_cairo_symbol(ctx_s, "light", scale=1.0)
            draw_cairo_text(ctx_s, "animaflow", 140, y_baseline, font_size, RGB_LIGHT_INK)
            surface_s.write_to_png(os.path.join(PNG_DIR, f"logo-horizontal-solido-{target_w}.png"))

        print(f"  ✓ logo-horizontal-{target_w}.png")

    # 4. Logo Vertical (800)
    v_total_w = max(160.0, text_w + 30.0)
    icon_offset_x = (v_total_w - 120.0) / 2.0
    text_offset_x = (v_total_w - text_w) / 2.0
    v_text_baseline = 120.0 + 18.0 + cap_h
    v_total_h = v_text_baseline + 20.0

    scale_v = 800.0 / v_total_w
    target_vh = int(v_total_h * scale_v)

    # Vertical Dark
    surface_v = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, target_vh)
    ctx_v = cairo.Context(surface_v)
    ctx_v.scale(scale_v, scale_v)
    ctx_v.save()
    ctx_v.translate(icon_offset_x, 0)
    draw_cairo_symbol(ctx_v, "dark", scale=1.0)
    ctx_v.restore()
    draw_cairo_text(ctx_v, "animaflow", text_offset_x, v_text_baseline, font_size, RGB_SAGE_ICE)
    surface_v.write_to_png(os.path.join(PNG_DIR, "logo-vertical-800.png"))
    print("  ✓ logo-vertical-800.png")

    # Vertical Light
    surface_vs = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, target_vh)
    ctx_vs = cairo.Context(surface_vs)
    ctx_vs.scale(scale_v, scale_v)
    ctx_vs.save()
    ctx_vs.translate(icon_offset_x, 0)
    draw_cairo_symbol(ctx_vs, "light", scale=1.0)
    ctx_vs.restore()
    draw_cairo_text(ctx_vs, "animaflow", text_offset_x, v_text_baseline, font_size, RGB_LIGHT_INK)
    surface_vs.write_to_png(os.path.join(PNG_DIR, "logo-vertical-solido-800.png"))
    print("  ✓ logo-vertical-solido-800.png")

    # 5. Banner Hero (1280x640)
    surface_b = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 640)
    ctx_b = cairo.Context(surface_b)
    
    # Fundo Sólido Nórdico Carvão
    ctx_b.set_source_rgb(*RGB_DARK_BG)
    ctx_b.rectangle(0, 0, 1280, 640)
    ctx_b.fill()

    # Grade técnica elegante
    ctx_b.set_source_rgba(RGB_SAGE_LIGHT[0], RGB_SAGE_LIGHT[1], RGB_SAGE_LIGHT[2], 0.05)
    ctx_b.set_line_width(1.0)
    for y in range(80, 640, 80):
        ctx_b.move_to(0, y); ctx_b.line_to(1280, y); ctx_b.stroke()
    for x in range(160, 1280, 160):
        ctx_b.move_to(x, 0); ctx_b.line_to(x, 640); ctx_b.stroke()

    # Símbolo no banner
    ctx_b.save()
    ctx_b.translate(560, 95)
    draw_cairo_symbol(ctx_b, "dark", scale=1.35)
    ctx_b.restore()

    # Tipografia: animaflow
    b_font_size = 112.0
    _, b_text_w, _, _, _ = text_to_path(FONT_PATH, "animaflow", b_font_size)
    b_text_x = (1280 - b_text_w) / 2.0
    draw_cairo_text(ctx_b, "animaflow", b_text_x, 385, b_font_size, RGB_SAGE_ICE)

    # Subtítulo (IBM Plex Sans)
    ctx_b.select_font_face("IBM Plex Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx_b.set_font_size(21.0)
    ctx_b.set_source_rgb(*RGB_SAGE_LIGHT)
    sub_text = "Declarative Animated Architecture Diagrams & Flowcharts in Python"
    extents = ctx_b.text_extents(sub_text)
    ctx_b.move_to((1280 - extents.width) / 2.0, 445)
    ctx_b.show_text(sub_text)

    # Badges
    badges = [
        ("Manim CE", RGB_SAGE_LIGHT),
        ("HTML / SVG", RGB_SAGE_ICE),
        ("Python 3.10+", RGB_JADE),
    ]
    start_bx = 415
    for i, (b_title, b_col) in enumerate(badges):
        bx = start_bx + i * 155
        by = 505
        bw, bh = 135, 34
        r = 6
        ctx_b.new_sub_path()
        ctx_b.arc(bx + bw - r, by + r, r, -math.pi/2, 0)
        ctx_b.arc(bx + bw - r, by + bh - r, r, 0, math.pi/2)
        ctx_b.arc(bx + r, by + bh - r, r, math.pi/2, math.pi)
        ctx_b.arc(bx + r, by + r, r, math.pi, 3*math.pi/2)
        ctx_b.close_path()
        ctx_b.set_source_rgb(*RGB_DARK_SURFACE)
        ctx_b.fill_preserve()
        ctx_b.set_source_rgb(*RGB_DARK_BORDER)
        ctx_b.set_line_width(1.2)
        ctx_b.stroke()

        ctx_b.select_font_face("IBM Plex Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx_b.set_font_size(13.0)
        ctx_b.set_source_rgb(*b_col)
        b_ext = ctx_b.text_extents(b_title)
        ctx_b.move_to(bx + (bw - b_ext.width)/2.0, by + 22)
        ctx_b.show_text(b_title)

    surface_b.write_to_png(os.path.join(PNG_DIR, "banner-hero-1280.png"))
    print("  ✓ banner-hero-1280.png")

if __name__ == "__main__":
    generate_svgs()
    rasterize_all_cairo()
