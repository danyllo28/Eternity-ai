"""Identidade da Eternity: a coroa branca é o símbolo oficial."""
from __future__ import annotations

import html

_CROWN = (
    '<svg class="{cls}" width="{w}" height="{h}" viewBox="0 0 64 58" fill="none" '
    'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">'
    '<path d="M6 20 21 31 32 7 43 31 58 20 52 44H12L6 20Z" fill="currentColor"/>'
    '<rect x="12" y="47" width="40" height="7" rx="3.5" fill="currentColor"/>'
    "</svg>"
)


def crown_svg(size: int = 24, cls: str = "", label: str = "Coroa da Eternity") -> str:
    """Coroa oficial, redesenhada em SVG sem perder as proporções originais."""
    width = int(size)
    height = int(round(size * 58 / 64))
    return _CROWN.format(w=width, h=height, cls=html.escape(cls), label=html.escape(label))


# Compatibilidade: o restante da aplicação pode usar o SVG pronto.
CROWN_SVG = crown_svg(34)


def brand_mark_html() -> str:
    return (
        '<div class="et-brand">'
        f'<span class="et-brand-crown">{crown_svg(22, cls="et-brand-glyph")}</span>'
        '<span class="et-brand-name">Eternity</span>'
        "</div>"
    )


def welcome_html(username: str, greeting: str) -> str:
    """Composição central de boas-vindas, no espírito do Claude, com a coroa."""
    name = html.escape(str(username or "você"))
    return (
        '<div class="et-welcome">'
        '<div class="et-welcome-mark">'
        '<span class="et-welcome-halo" aria-hidden="true"></span>'
        f"{crown_svg(40, cls='et-welcome-glyph')}"
        "</div>"
        f"<h1>{html.escape(greeting)}, {name}.</h1>"
        "<p>O que vamos criar hoje?</p>"
        "</div>"
    )


def auth_hero_html() -> str:
    return (
        '<div class="et-auth-hero">'
        f'<span class="et-auth-crown">{crown_svg(42)}</span>'
        '<div class="et-auth-name">Eternity</div>'
        '<p class="et-auth-slogan">Sua IA pessoal, do seu jeito.</p>'
        '<p class="et-auth-sub">Entre ou crie sua conta para continuar.</p>'
        "</div>"
    )
