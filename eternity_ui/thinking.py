"""Animação oficial de pensamento da Eternity (HTML + SVG + CSS)."""
from __future__ import annotations

import html

from .brand import crown_svg

# cada órbita: (classe, tamanho, inclinação, achatamento, contra-escala, velocidade, atraso, tracejada)
_ORBITS = (
    ("o1", False),
    ("o2", True),
    ("o3", False),
)


def _orbit_markup(cls: str, dashed: bool) -> str:
    dash = " et-orbit-dashed" if dashed else ""
    return (
        f'<span class="et-orbit {cls}{dash}">'
        '<span class="et-orbit-plane">'
        '<span class="et-orbit-ring"></span>'
        '<i class="et-particle"><b></b></i>'
        "</span></span>"
    )


def thinking_html(caption: str = "está pensando", *, ending: bool = False, searching: bool = False) -> str:
    """Coroa no centro, três partículas em órbitas elípticas e halo pulsante.

    `ending=True` reproduz o fade-out usado no instante em que a resposta começa.
    """
    orbits = "".join(_orbit_markup(cls, dashed) for cls, dashed in _ORBITS)
    state = " is-ending" if ending else ""
    if searching:
        state += " is-searching"
    search_badge = '<span class="et-search-pulse" aria-hidden="true"></span>' if searching else ""
    safe_caption = html.escape(caption)
    return (
        f'<div class="et-think{state}" role="status" aria-live="polite">'
        '<div class="et-think-stage" aria-hidden="true">'
        '<span class="et-think-halo"></span>'
        f"{orbits}"
        f'<span class="et-think-crown">{crown_svg(46, cls="et-crown-glyph")}</span>'
        "</div>"
        '<div class="et-think-label">' + search_badge + '<strong>Eternity</strong>'
        f"<span>{safe_caption}</span>"
        '<span class="et-think-ellipsis" aria-hidden="true"><i></i><i></i><i></i></span>'
        "</div>"
        "</div>"
    )


def image_loading_html(pct: int = 0, remaining: int | None = None, caption: str = "criando sua imagem") -> str:
    """Coroa em movimento + barra e porcentagem enquanto a imagem é gerada."""
    pct = max(0, min(100, int(pct)))
    orbits = "".join(_orbit_markup(cls, dashed) for cls, dashed in _ORBITS)
    if pct >= 100:
        eta = '<span class="et-image-eta">pronto</span>'
    elif remaining is not None:
        eta = f'<span class="et-image-eta">~{max(1, int(remaining))}s restantes</span>'
    else:
        eta = ""
    safe_caption = html.escape(caption)
    return (
        '<div class="et-image-load" role="status" aria-live="polite">'
        '<div class="et-think-stage et-image-stage" aria-hidden="true">'
        '<span class="et-think-halo"></span>'
        f"{orbits}"
        f'<span class="et-think-crown">{crown_svg(42, cls="et-crown-glyph")}</span>'
        "</div>"
        '<div class="et-image-meter" aria-hidden="true">'
        f'<span style="width:{pct}%"></span>'
        "</div>"
        '<div class="et-image-status">'
        f"<strong>{pct}%</strong><span>{safe_caption}</span>{eta}"
        "</div>"
        "</div>"
    )
