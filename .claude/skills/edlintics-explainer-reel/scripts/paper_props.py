"""Paper-style versions of the flat text and graph props (18 Nov 2026; Hoang: "render a paper old format to test which one is better").

First used by assets/renders/explainer-reels/w47/paper-supply-demand/, the paper (hand-drawn) twin of flat-supply-demand: the same
script, so the same cards, sentences and graph, drawn in the old paper look. Each prop here draws its flat_* namesake and puts a paper
skin on the SVG: the soft drop shadow goes, every card and pill gets an ink outline (5 px cards, 3.5 px pills), solid shapes such as
arrows and the graph's arrow tips get an ink edge, and the graph's dots get an ink ring instead of a white one. The renderer's pencil
grain, line boil and ghost pass (every script without meta.style "flat") then make them hand-drawn like the rest of the scene library.
Texts stay Inter, as in every paper prop. The flat props themselves are untouched.

Installed into scene_lib by install(): paper_card (flat_card), paper_tag (flat_tag), paper_sentence (flat_sentence), paper_arrow
(flat_arrow), paper_icon (flat_icon), sd_graph (flat_sd_graph: axes, supply and demand lines that draw on, equilibrium points with P*/Q*, surplus and
shortage bands, the price-ceiling line, curve shifts with a dashed old curve, green and red arrows along the axes). Options, timing
keys and geometry are exactly those of the flat prop (see its docstring), so one generator can lay out both versions. Also tv: a
hand-drawn flat-screen TV (for "TVs keep getting cheaper").
"""
import re

INK = "#0F172A"
_SHADOW = re.compile(r'<rect [^>]*fill="#1E3A8A" opacity="0\.16"/>')
_FB = re.compile(r'<rect data-fb="1"([^>]*?)height="([\d.]+)"')
_SOLID = re.compile(r'<path (?![^>]*\bstroke=)([^>]*\bfill="(?!none)[^"]+"[^>]*)/>')


def paper_skin(svg):
    """flat SVG -> paper SVG: no drop shadow, ink outlines on cards, pills and solid shapes, ink rings on dots"""
    svg = _SHADOW.sub("", svg)
    svg = _FB.sub(lambda m: f'<rect data-fb="1" stroke="{INK}" stroke-width="{3.5 if float(m.group(2)) < 110 else 5}" stroke-linejoin="round"{m.group(1)}height="{m.group(2)}"', svg)
    svg = _SOLID.sub(lambda m: f'<path {m.group(1)} stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>', svg)
    return svg.replace('stroke="#FFFFFF" stroke-width="6"', f'stroke="{INK}" stroke-width="5"')


def install(G):
    """Register the paper props in scene_lib (G = its globals), after flat_props.install"""
    P = G["PRESETS"]
    pairs = {"paper_card": "flat_card", "paper_tag": "flat_tag", "paper_sentence": "flat_sentence", "paper_arrow": "flat_arrow", "paper_icon": "flat_icon", "sd_graph": "flat_sd_graph"}
    for new, old in pairs.items():
        fn, box = P[old]

        def draw(x, y, s=1.0, _fn=fn, **k):
            return paper_skin(_fn(x, y, s, **k))
        draw.__doc__ = f"Paper version of {old} (18 Nov 2026): the same options, with ink outlines and no shadow, so the pencil look applies. " + (fn.__doc__ or "").strip().split("\n")[0]
        P[new] = (draw, box)
        if old in G["HALF"]: G["HALF"][new] = G["HALF"][old]

    def tv(x, y, s=1.0, w=150, h=96, **_):
        """A flat-screen TV on two short feet, hand-drawn (no brand, no picture). (x, y) = centre of the screen; w, h = screen size."""
        f = G["_f"]; out = (f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" rx="9" fill="#222C3D" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                            f'<rect x="{-w / 2 + 12}" y="{-h / 2 + 11}" width="{w - 24}" height="{h - 22}" rx="4" fill="#3B5EA8"/>'
                            f'<path d="M{-w / 2 + 24} {h / 2 - 24} L{-w / 2 + 58} {-h / 2 + 22}" stroke="#9DB8E6" stroke-width="6" stroke-linecap="round"/>'
                            f'<path d="M{-w * 0.28:.1f} {h / 2} l-10 16 M{w * 0.28:.1f} {h / 2} l10 16" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>')
        return f'<g transform="translate({f(x)} {f(y)}) scale({s})">{out}</g>'

    P["tv"] = (tv, lambda x, y, s=1.0, w=150, h=96, **_: [x - w * s / 2 - 4, y - h * s / 2 - 4, w * s + 8, (h + 20) * s + 8])
