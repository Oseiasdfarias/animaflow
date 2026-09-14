"""Converte texto em path SVG usando fontTools (sem dependência de fonte no cliente/destino)."""

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform


def text_to_path(font_path, text, size, letter_spacing=0.0):
    """Retorna (path_d, largura_total, ascender, descender, cap_height) em unidades de 'size'."""
    font = TTFont(font_path)
    upem = font["head"].unitsPerEm
    scale = size / upem
    cmap = font.getBestCmap()
    glyphset = font.getGlyphSet()
    hmtx = font["hmtx"]

    pen_out = SVGPathPen(glyphset, ntos=lambda v: f"{v:.2f}")
    x = 0.0
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            x += size * 0.3
            continue
        # y-flip + escala + posição horizontal
        t = Transform(scale, 0, 0, -scale, x, 0)
        tpen = TransformPen(pen_out, t)
        glyphset[gname].draw(tpen)
        adv = hmtx[gname][0]
        x += adv * scale + letter_spacing

    if text:
        x -= letter_spacing

    asc = font["hhea"].ascender * scale
    desc = font["hhea"].descender * scale
    # Altura de caixa alta real da fonte para alinhamento vertical preciso
    cap = getattr(font["OS/2"], "sCapHeight", None)
    cap = (cap if cap else 0.70 * upem) * scale
    return pen_out.getCommands(), x, asc, desc, cap


if __name__ == "__main__":
    import sys, json

    fp = sys.argv[1]
    txt = sys.argv[2]
    size = float(sys.argv[3])
    ls = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
    d, w, a, de, cap = text_to_path(fp, txt, size, ls)
    print(
        json.dumps(
            {
                "d": d,
                "width": round(w, 2),
                "asc": round(a, 2),
                "desc": round(de, 2),
                "cap": round(cap, 2),
            }
        )
    )
