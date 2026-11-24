"""Ícones personalizados da Eternity.

Todos os símbolos foram desenhados para conversar com a coroa oficial:
traço simples, cantos suaves e uma linguagem visual elegante.
"""
from __future__ import annotations

import html

_ICONS = {
    'crown': '''<path d="M6 20 21 31 32 7 43 31 58 20 52 44H12L6 20Z" fill="currentColor"/><rect x="12" y="47" width="40" height="7" rx="3.5" fill="currentColor"/>''',
    'copy': '''<rect x="14" y="14" width="26" height="26" rx="6" stroke="currentColor" stroke-width="4" fill="none"/><path d="M24 10h18a6 6 0 0 1 6 6v18" stroke="currentColor" stroke-width="4" stroke-linecap="round" fill="none"/>''',
    'sound': '''<path d="M18 24h8l10-8v32l-10-8h-8z" fill="currentColor"/><path d="M46 22a14 14 0 0 1 0 20" stroke="currentColor" stroke-width="4" stroke-linecap="round" fill="none"/>''',
    'bookmark': '''<path d="M18 10h28a4 4 0 0 1 4 4v40l-18-12-18 12V14a4 4 0 0 1 4-4z" fill="currentColor"/>''',
    'refresh': '''<path d="M48 20a20 20 0 1 0 4 22" stroke="currentColor" stroke-width="5" stroke-linecap="round" fill="none"/><path d="M52 8v16H36" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>''',
    'sparkle': '''<path d="M32 6l6 16 16 6-16 6-6 16-6-16-16-6 16-6z" fill="currentColor"/>''',
    'focus': '''<circle cx="32" cy="32" r="18" stroke="currentColor" stroke-width="4" fill="none"/><circle cx="32" cy="32" r="6" fill="currentColor"/><path d="M32 4v8M32 52v8M4 32h8M52 32h8" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>''',
    'chat': '''<path d="M12 14h40a6 6 0 0 1 6 6v20a6 6 0 0 1-6 6H30l-12 10v-10h-6a6 6 0 0 1-6-6V20a6 6 0 0 1 6-6z" fill="currentColor"/>''',
    'library': '''<path d="M10 12h12v40H10zM26 12h12v40H26zM44 16l10 34-10 3-10-34z" fill="currentColor"/>''',
    'memory': '''<path d="M32 8l6 12 14 2-10 10 2 14-12-6-12 6 2-14-10-10 14-2z" fill="currentColor"/>''',
    'files': '''<path d="M16 10h20l12 12v32a4 4 0 0 1-4 4H16a4 4 0 0 1-4-4V14a4 4 0 0 1 4-4z" fill="currentColor"/>''',
    'settings': '''<circle cx="32" cy="32" r="8" fill="currentColor"/><path d="M32 8v8M32 48v8M8 32h8M48 32h8M16 16l6 6M42 42l6 6M48 16l-6 6M22 42l-6 6" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>''',
    'send': '''<path d="M10 32 54 10 38 54l-8-16z" fill="currentColor"/>''',
    'image': '''<rect x="10" y="14" width="44" height="36" rx="6" stroke="currentColor" stroke-width="4" fill="none"/><circle cx="24" cy="28" r="5" fill="currentColor"/><path d="M14 46l12-12 8 8 8-10 10 14" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" fill="none"/>''',
    'web': '''<circle cx="32" cy="32" r="22" stroke="currentColor" stroke-width="4" fill="none"/><path d="M10 32h44M32 10c8 8 8 36 0 44M32 10c-8 8-8 36 0 44" stroke="currentColor" stroke-width="4" fill="none"/>''',
    'think': '''<path d="M22 12h20a8 8 0 0 1 8 8v12a8 8 0 0 1-8 8h-6l-8 8v-8h-6a8 8 0 0 1-8-8V20a8 8 0 0 1 8-8z" fill="currentColor"/><circle cx="28" cy="28" r="3" fill="#0b0c10"/><circle cx="36" cy="28" r="3" fill="#0b0c10"/>''',
    'pin': '''<path d="M24 10h16l-2 14 8 8H18l8-8z" fill="currentColor"/><path d="M32 32v20" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>''',
    'trash': '''<path d="M16 18h32l-3 30a4 4 0 0 1-4 4H23a4 4 0 0 1-4-4z" fill="currentColor"/><path d="M12 14h40" stroke="currentColor" stroke-width="4" stroke-linecap="round"/><path d="M26 14V10h12v4" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>''',
    'edit': '''<path d="M14 44l24-24 8 8-24 24H14z" fill="currentColor"/><path d="M40 14l6-6 8 8-6 6z" fill="currentColor"/>''',
}

def icon_svg(name: str, size: int = 18, cls: str = "", label: str = "") -> str:
    """Retorna um ícone SVG personalizado da Eternity."""
    body = _ICONS.get(name, _ICONS["crown"])
    label = label or f"Ícone {name} da Eternity"
    return (
        f'<svg class="{html.escape(cls)}" width="{size}" height="{size}" viewBox="0 0 64 64" '
        f'fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{html.escape(label)}">'
        f"{body}</svg>"
    )

def icon(name: str, size: int = 18, cls: str = "", label: str = "") -> str:
    """Atalho para icon_svg."""
    return icon_svg(name, size, cls, label)
