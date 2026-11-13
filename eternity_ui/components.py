"""Pequenos construtores de HTML reutilizados pelas páginas."""
from __future__ import annotations

import html

from .brand import crown_svg


def page_head_html(eyebrow: str, title: str, subtitle: str = "") -> str:
    return (
        '<div class="et-page-head">'
        f'<div class="et-page-eyebrow">{crown_svg(14, cls="et-page-glyph")}'
        f"<span>{html.escape(eyebrow)}</span></div>"
        f'<div class="et-page-title">{html.escape(title)}</div>'
        f'<div class="et-page-sub">{html.escape(subtitle)}</div>'
        "</div>"
    )


def user_message_html(text: str, thumbs=(), note: str = "") -> str:
    images = "".join(
        f'<img src="data:image/jpeg;base64,{html.escape(str(b64))}" alt="Imagem anexada">'
        for b64 in thumbs or ()
    )
    note_html = (
        f'<div class="et-msg-note">{html.escape(str(note))}</div>'
        if note and not images
        else ""
    )
    body = (
        html.escape(str(text or ""))
        .replace("$", "&#36;")
        .replace("\n", "<br>")
    )
    return (
        '<div class="et-msg-user"><div class="et-msg-user-bubble">'
        f"{images}{note_html}{body}</div></div>"
    )


def empty_state_html(title: str, text: str) -> str:
    return (
        '<div class="et-empty">'
        f'<div class="et-empty-title">{html.escape(title)}</div>'
        f'<div class="et-empty-text">{html.escape(text)}</div>'
        "</div>"
    )
