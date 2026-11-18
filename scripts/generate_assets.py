#!/usr/bin/env python3
"""
Generates every custom SVG used by the profile README.

GitHub strips CSS/JS from README markup, so all visual design lives in
self-contained SVGs (rendered via <img>, where CSS animations still run).

Edit the data blocks below (SKILL_GROUPS, PROJECTS) and re-run:

    python3 scripts/generate_assets.py

Output goes to ./assets relative to the repo root.
"""
from __future__ import annotations

import math
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

# --------------------------------------------------------------------------
# Design tokens
# --------------------------------------------------------------------------
T = {
    "bg": "#0A0E14",
    "panel": "#0D1117",
    "panel_hi": "#111823",
    "border": "#1F2A37",
    "track": "#1A2330",
    "text": "#E6EDF3",
    "muted": "#7D8A9C",
    "faint": "#3B4757",
    "mint": "#00F58D",   # brand accent (kept from the original profile)
    "cyan": "#00D1FF",
    "violet": "#8B5CF6",
}
SANS = "'Inter','Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','Fira Code','SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

REDUCED_MOTION = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"

# --------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------
SKILL_GROUPS = [
    {
        "slug": "genai",
        "file": "intelligence.py",
        "title": "Generative & Agentic AI",
        "accent": T["mint"],
        "items": [
            "Generative AI",
            "Agentic AI",
            "Multi-Agent Systems",
            "LLMs",
            "RAG",
        ],
    },
    {
        "slug": "frameworks",
        "file": "retrieval.py",
        "title": "Frameworks & Retrieval",
        "accent": T["cyan"],
        "items": [
            "LangChain",
            "LangGraph",
            "Embeddings",
            "Vector Databases",
            "PostgreSQL",
        ],
    },
    {
        "slug": "engineering",
        "file": "stack.ts",
        "title": "Languages & Full Stack",
        "accent": T["violet"],
        "items": [
            "Python",
            "React",
            "TypeScript",
            "FastAPI",
        ],
    },
    {
        "slug": "devops",
        "file": "ship.yaml",
        "title": "Cloud, DevOps & Tools",
        "accent": T["mint"],
        "items": [
            "Docker",
            "Postman",
            "Git",
            "GCP",
        ],
    },
]

PROJECTS = [
    {
        "slug": "aperture",
        "name": "Aperture",
        "url": "https://github.com/VARIKUNTLASAIMANOJ/Aperture",
        "lines": ["AI HR onboarding: payroll,", "offer letters & voice", "follow-ups, human-approved"],
        "tags": ["LangGraph", "Next.js"],
        "accent": T["mint"],
        "glyph": "aperture",
    },
    {
        "slug": "tejoraj",
        "name": "Tejoraj",
        "url": "https://github.com/VARIKUNTLASAIMANOJ/Tejoraj",
        "lines": ["AI space research platform:", "paper generation, chat,", "NASA & arXiv data"],
        "tags": ["LangChain", "React"],
        "accent": T["cyan"],
        "glyph": "orbit",
    },
    {
        "slug": "shopscribe",
        "name": "ShopScribe",
        "url": "https://github.com/VARIKUNTLASAIMANOJ/ShopScribe",
        "lines": ["Scrapes Amazon, Flipkart &", "Myntra reviews and charts", "sentiment trends"],
        "tags": ["Gemini", "Streamlit"],
        "accent": T["violet"],
        "glyph": "chart",
    },
]


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def svg(width: int, height: int, body: str, style: str = "", title: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">'
        f"<title>{escape(title)}</title>"
        f"<style>{style}{REDUCED_MOTION}</style>{body}</svg>\n"
    )


def window_chrome(width: int, label: str, right: str = "") -> str:
    dots = "".join(
        f'<circle cx="{22 + i * 16}" cy="22" r="5" fill="{c}"/>'
        for i, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"])
    )
    right_txt = (
        f'<text x="{width - 20}" y="26" text-anchor="end" class="mono muted" font-size="11" '
        f'letter-spacing="1.5">{escape(right)}</text>'
        if right
        else ""
    )
    return (
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="43" rx="13.5" fill="{T["panel_hi"]}"/>'
        f'<rect x="0.5" y="30" width="{width - 1}" height="14" fill="{T["panel_hi"]}"/>'
        f'<line x1="1" y1="44" x2="{width - 1}" y2="44" stroke="{T["border"]}"/>'
        f"{dots}"
        f'<text x="78" y="26" class="mono muted" font-size="12">{escape(label)}</text>'
        f"{right_txt}"
    )


def write(name: str, content: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(content, encoding="utf-8")
    print(f"  ✓ assets/{name}")


BASE_STYLE = (
    f".sans{{font-family:{SANS}}}.mono{{font-family:{MONO}}}"
    f".muted{{fill:{T['muted']}}}.text{{fill:{T['text']}}}"
)


# --------------------------------------------------------------------------
# Header / hero
# --------------------------------------------------------------------------
def build_header() -> str:
    W, H = 1200, 420
    # Neural network on the right
    layers = [(770, 3), (880, 5), (990, 5), (1100, 2)]
    nodes = []
    for x, n in layers:
        span = 64 * (n - 1)
        top = 215 - span / 2
        nodes.append([(x, top + i * 64) for i in range(n)])

    edges, pulses = [], []
    k = 0
    for li in range(len(nodes) - 1):
        for a in nodes[li]:
            for b in nodes[li + 1]:
                d = f"M{a[0]},{a[1]:.0f} L{b[0]},{b[1]:.0f}"
                edges.append(f'<path d="{d}" class="edge"/>')
                if (k * 7) % 5 == 0:  # deterministic subset carries signal pulses
                    length = math.dist(a, b)
                    delay = (k * 0.37) % 3.2
                    pulses.append(
                        f'<path d="{d}" class="pulse" stroke-dasharray="14 {length:.0f}" '
                        f'stroke-dashoffset="14" style="--len:-{length:.0f};animation-delay:{delay:.2f}s"/>'
                    )
                k += 1

    node_svg = []
    for li, layer in enumerate(nodes):
        color = [T["mint"], T["cyan"], T["cyan"], T["violet"]][li]
        for i, (x, y) in enumerate(layer):
            delay = (li * 0.45 + i * 0.3) % 3
            node_svg.append(
                f'<circle cx="{x}" cy="{y:.0f}" r="13" fill="{color}" opacity=".12" class="halo" '
                f'style="animation-delay:{delay:.2f}s"/>'
                f'<circle cx="{x}" cy="{y:.0f}" r="6" fill="{T["panel"]}" stroke="{color}" stroke-width="2"/>'
            )

    chips = ["Generative AI", "AI Agents", "RAG · LLMs", "Full Stack"]
    chip_svg, cx = [], 64
    for c in chips:
        w = 22 + len(c) * 8.6
        chip_svg.append(
            f'<g transform="translate({cx:.0f},318)">'
            f'<rect width="{w:.0f}" height="34" rx="17" fill="{T["panel_hi"]}" stroke="{T["border"]}"/>'
            f'<text x="{w / 2:.0f}" y="22" text-anchor="middle" class="mono text" font-size="13.5">{escape(c)}</text></g>'
        )
        cx += w + 10

    style = BASE_STYLE + (
        f".edge{{stroke:{T['border']};stroke-width:1.2;fill:none}}"
        f".pulse{{stroke:url(#signal);stroke-width:2.4;fill:none;stroke-linecap:round;"
        f"animation:flow 3.2s linear infinite}}"
        "@keyframes flow{to{stroke-dashoffset:var(--len)}}"
        ".halo{animation:breathe 3s ease-in-out infinite;transform-box:fill-box;transform-origin:center}"
        "@keyframes breathe{0%,100%{opacity:.08;transform:scale(.8)}50%{opacity:.35;transform:scale(1.25)}}"
        ".cursor{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
        ".rise{animation:rise .9s cubic-bezier(.2,.7,.2,1) backwards}"
        "@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}"
        ".live{animation:live 2s ease-in-out infinite}@keyframes live{50%{opacity:.35}}"
    )

    body = f"""
<defs>
  <linearGradient id="name" x1="0" x2="1"><stop offset="0" stop-color="{T['text']}"/><stop offset="1" stop-color="#B8C4D3"/></linearGradient>
  <linearGradient id="role" x1="0" x2="1"><stop offset="0" stop-color="{T['mint']}"/><stop offset=".55" stop-color="{T['cyan']}"/><stop offset="1" stop-color="{T['violet']}"/></linearGradient>
  <linearGradient id="signal" x1="0" x2="1"><stop offset="0" stop-color="{T['mint']}"/><stop offset="1" stop-color="{T['cyan']}"/></linearGradient>
  <radialGradient id="glowA" cx="0.82" cy="0.45" r="0.45"><stop offset="0" stop-color="{T['cyan']}" stop-opacity=".16"/><stop offset="1" stop-color="{T['cyan']}" stop-opacity="0"/></radialGradient>
  <radialGradient id="glowB" cx="0.08" cy="0.05" r="0.5"><stop offset="0" stop-color="{T['mint']}" stop-opacity=".12"/><stop offset="1" stop-color="{T['mint']}" stop-opacity="0"/></radialGradient>
  <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{T['faint']}" opacity=".45"/></pattern>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="22"/></clipPath>
</defs>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="{T['bg']}"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <rect width="{W}" height="{H}" fill="url(#glowA)"/>
  <rect width="{W}" height="{H}" fill="url(#glowB)"/>
  <g>{''.join(edges)}{''.join(pulses)}{''.join(node_svg)}</g>
  <text x="770" y="388" class="mono muted" font-size="11.5" letter-spacing="1">input → hidden → hidden → output</text>
</g>
<rect x="0.75" y="0.75" width="{W - 1.5}" height="{H - 1.5}" rx="21.5" fill="none" stroke="{T['border']}" stroke-width="1.5"/>

<g class="rise" style="animation-delay:.05s">
  <text x="64" y="84" class="mono" font-size="16"><tspan fill="{T['mint']}">❯</tspan><tspan fill="{T['muted']}"> whoami</tspan><tspan class="cursor" fill="{T['mint']}"> ▍</tspan></text>
</g>
<g class="rise" style="animation-delay:.2s">
  <text x="62" y="160" class="sans" font-size="64" font-weight="800" fill="url(#name)" letter-spacing="-1.5">Varikuntla</text>
  <text x="62" y="228" class="sans" font-size="64" font-weight="800" fill="url(#name)" letter-spacing="-1.5">Sai Manoj<tspan fill="{T['mint']}">.</tspan></text>
</g>
<g class="rise" style="animation-delay:.4s">
  <text x="64" y="280" class="sans" font-size="25" font-weight="600" fill="url(#role)">AI Engineer  ·  Full Stack Developer</text>
</g>
<g class="rise" style="animation-delay:.6s">{''.join(chip_svg)}</g>

<g transform="translate(944,36)">
  <rect width="222" height="30" rx="15" fill="{T['panel_hi']}" stroke="{T['border']}"/>
  <circle cx="18" cy="15" r="4.5" fill="{T['mint']}" class="live"/>
  <text x="32" y="20" class="mono text" font-size="12">building intelligent systems</text>
</g>
"""
    return svg(W, H, body, style, "Varikuntla Sai Manoj — AI Engineer and Full Stack Developer")


# --------------------------------------------------------------------------
# Skill cards (Known Technologies)
# --------------------------------------------------------------------------
def build_skill_card(group: dict, rows: int) -> str:
    """Code-editor card listing technologies as a two-column grid of chips."""
    W = 390
    COLS, CHIP_H, GAP, TOP = 2, 40, 10, 96
    chip_w = (W - 40 - GAP) / COLS
    H = TOP + rows * CHIP_H + (rows - 1) * GAP + 22
    acc = group["accent"]

    body = [
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="{T["panel"]}" stroke="{T["border"]}"/>',
        window_chrome(W, group["file"]),
        f'<rect x="20" y="62" width="3" height="18" rx="1.5" fill="{acc}"/>',
        f'<text x="32" y="76" class="sans text" font-size="15" font-weight="700">{escape(group["title"])}</text>',
    ]
    for i, name in enumerate(group["items"]):
        x = 20 + (i % COLS) * (chip_w + GAP)
        y = TOP + (i // COLS) * (CHIP_H + GAP)
        body.append(
            f'<g class="chip" style="animation-delay:{0.1 + i * 0.08:.2f}s">'
            f'<rect x="{x:.1f}" y="{y}" width="{chip_w:.1f}" height="{CHIP_H}" rx="9" fill="{T["panel_hi"]}" stroke="{T["border"]}"/>'
            f'<circle cx="{x + 16:.1f}" cy="{y + CHIP_H / 2}" r="3.5" fill="{acc}"/>'
            f'<text x="{x + 30:.1f}" y="{y + CHIP_H / 2 + 4.5}" class="sans text" font-size="13.5" font-weight="500">{escape(name)}</text></g>'
        )

    style = BASE_STYLE + (
        ".chip{animation:pop .5s ease-out backwards}"
        "@keyframes pop{from{opacity:0}to{opacity:1}}"
    )
    return svg(W, H, "".join(body), style, f"{group['title']}: " + ", ".join(group["items"]))


# --------------------------------------------------------------------------
# Project cards
# --------------------------------------------------------------------------
GLYPHS = {
    "aperture": lambda c: (
        f'<circle r="15" fill="none" stroke="{c}" stroke-width="2"/>'
        + "".join(
            f'<line x1="{15 * math.cos(math.radians(k * 60)):.1f}" y1="{15 * math.sin(math.radians(k * 60)):.1f}" '
            f'x2="{6 * math.cos(math.radians(k * 60 + 120)):.1f}" y2="{6 * math.sin(math.radians(k * 60 + 120)):.1f}" '
            f'stroke="{c}" stroke-width="1.8" stroke-linecap="round"/>'
            for k in range(6)
        )
    ),
    "chart": lambda c: (
        f'<rect x="-14" y="-14" width="28" height="28" rx="7" fill="none" stroke="{c}" stroke-width="2"/>'
        f'<path d="M-8,6 L-3,0 L2,3 L8,-6" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="8" cy="-6" r="1.8" fill="{c}"/>'
    ),
    "quiz": lambda c: (
        f'<rect x="-14" y="-14" width="28" height="28" rx="7" fill="none" stroke="{c}" stroke-width="2"/>'
        f'<path d="M-5,-3 a5,5 0 1 1 6,4.9 v3" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round"/>'
        f'<circle cx="1" cy="9" r="1.6" fill="{c}"/>'
    ),
    "spark": lambda c: (
        f'<path d="M0,-15 C2,-4 4,-2 15,0 C4,2 2,4 0,15 C-2,4 -4,2 -15,0 C-4,-2 -2,-4 0,-15Z" '
        f'fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>'
    ),
    "orbit": lambda c: (
        f'<circle r="6" fill="none" stroke="{c}" stroke-width="2"/>'
        f'<ellipse rx="16" ry="7" fill="none" stroke="{c}" stroke-width="1.6" transform="rotate(-25)"/>'
        f'<circle cx="13" cy="-6" r="2.2" fill="{c}"/>'
    ),
}


def build_project_card(i: int, p: dict) -> str:
    W, H = 258, 214
    acc = p["accent"]
    lines = "".join(
        f'<text x="22" y="{116 + j * 20}" class="sans" font-size="13.5" fill="#AAB6C5">{escape(t)}</text>'
        for j, t in enumerate(p["lines"])
    )
    tags, tx = [], 22
    for t in p["tags"]:
        w = 16 + len(t) * 7.4
        tags.append(
            f'<g transform="translate({tx:.0f},176)"><rect width="{w:.0f}" height="22" rx="6" fill="{acc}" fill-opacity=".1" '
            f'stroke="{acc}" stroke-opacity=".35"/><text x="{w / 2:.0f}" y="15" text-anchor="middle" class="mono" '
            f'font-size="11" fill="{acc}">{escape(t)}</text></g>'
        )
        tx += w + 8

    body = f"""
<defs><linearGradient id="top" x1="0" x2="1"><stop offset="0" stop-color="{acc}"/><stop offset="1" stop-color="{acc}" stop-opacity="0"/></linearGradient>
<radialGradient id="g" cx="1" cy="0" r="0.9"><stop offset="0" stop-color="{acc}" stop-opacity=".14"/><stop offset="1" stop-color="{acc}" stop-opacity="0"/></radialGradient></defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="{T['panel']}" stroke="{T['border']}"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="url(#g)"/>
<rect x="22" y="0" width="120" height="2" fill="url(#top)" class="scan"/>
<g transform="translate(40,44)"><g class="glyph">{GLYPHS[p['glyph']](acc)}</g></g>
<text x="{W - 22}" y="50" text-anchor="end" class="mono" font-size="12" fill="{T['faint']}">{i + 1:02d} ↗</text>
<text x="22" y="90" class="sans text" font-size="19" font-weight="700" letter-spacing="-.3">{escape(p['name'])}</text>
{lines}
{''.join(tags)}
"""
    style = BASE_STYLE + (
        ".glyph{animation:float 4s ease-in-out infinite}"
        "@keyframes float{50%{transform:translateY(-4px)}}"
        ".scan{animation:scan 5s ease-in-out infinite}"
        f"@keyframes scan{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX({W - 164}px)}}}}"
    )
    return svg(W, H, body, style, f"{p['name']} — {' '.join(p['lines'])}")


# --------------------------------------------------------------------------
# Footer
# --------------------------------------------------------------------------
def build_footer() -> str:
    W, H = 1200, 150
    bars = []
    for i in range(60):
        x = 20 + i * 19.4
        h = 10 + 26 * abs(math.sin(i * 0.37)) * abs(math.cos(i * 0.11))
        bars.append(
            f'<rect x="{x:.1f}" y="{H - 12 - h:.1f}" width="9" height="{h:.1f}" rx="2" fill="url(#eq)" '
            f'class="b" style="animation-delay:{(i % 12) * 0.12:.2f}s"/>'
        )
    style = BASE_STYLE + (
        ".b{opacity:.22;transform-box:fill-box;transform-origin:bottom;animation:eq 2.4s ease-in-out infinite}"
        "@keyframes eq{50%{transform:scaleY(.45);opacity:.4}}"
    )
    body = f"""
<defs><linearGradient id="eq" x1="0" x2="1"><stop offset="0" stop-color="{T['mint']}"/><stop offset=".5" stop-color="{T['cyan']}"/><stop offset="1" stop-color="{T['violet']}"/></linearGradient>
<clipPath id="c"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs>
<g clip-path="url(#c)"><rect width="{W}" height="{H}" fill="{T['bg']}"/>{''.join(bars)}</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="17.5" fill="none" stroke="{T['border']}" stroke-width="1.5"/>
<text x="{W / 2}" y="66" text-anchor="middle" class="sans text" font-size="30" font-weight="700" font-style="italic" letter-spacing="-.3">“Keep Building. Keep Learning. Stay Curious.”</text>
"""
    return svg(W, H, body, style, "Keep Building. Keep Learning. Stay Curious.")


# --------------------------------------------------------------------------
def main() -> None:
    print("Generating assets…")
    write("header.svg", build_header())

    # Cards placed side-by-side share a height so rows line up perfectly.
    for a, b in zip(SKILL_GROUPS[0::2], SKILL_GROUPS[1::2]):
        rows = math.ceil(max(len(a["items"]), len(b["items"])) / 2)
        write(f"tech-{a['slug']}.svg", build_skill_card(a, rows))
        write(f"tech-{b['slug']}.svg", build_skill_card(b, rows))

    for i, p in enumerate(PROJECTS):
        write(f"project-{p['slug']}.svg", build_project_card(i, p))

    write("footer.svg", build_footer())


if __name__ == "__main__":
    main()
