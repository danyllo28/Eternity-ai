"""Eternity brand SVG and thinking indicator markup."""

CROWN_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 42" role="img" aria-label="Coroa branca da Eternity"><path d="M5 11.5 14.7 20 23.8 4.5 33.2 20 43 11.5 38.8 31H9.2L5 11.5Z" fill="#FFFFFF"/><path d="M10 35.5H38" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round"/><path d="M8.5 31H39.5" stroke="#C9CDD4" stroke-width="1.7" stroke-linecap="round"/></svg>'''


def thinking_indicator(label="Eternity está pensando…"):
    """Return accessible HTML for the crown-and-particles thinking animation."""
    safe_label = str(label).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    return (
        '<div class="et-new-loader" role="status" aria-live="polite">'
        '<span class="et-new-thinking" aria-hidden="true">'
        + CROWN_SVG
        + '<i class="et-new-particle"></i><i class="et-new-particle"></i>'
        '<i class="et-new-particle"></i></span>'
        f'<span>{safe_label}</span></div>'
    )
