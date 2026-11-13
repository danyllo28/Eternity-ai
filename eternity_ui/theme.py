"""Design system da nova Eternity: um único conjunto de tokens e estilos.

Toda a interface usa o prefixo `et-` e os tokens `--et-*`. As regras antigas
foram substituídas por esta camada, não sobrepostas.
"""
from __future__ import annotations

import streamlit as st

_DARK = {
    "bg": "#090A0D",
    "sidebar": "#0D0F13",
    "surface": "#15171C",
    "surface2": "#1C1F25",
    "surface_hover": "#22262E",
    "border": "#292D34",
    "border_soft": "#1F232A",
    "border_strong": "#3B414B",
    "text": "#F3F4F6",
    "muted": "#A0A5AE",
    "nav": "#B7BCC5",
    "crown": "#FFFFFF",
    "user_bubble": "#1A1D23",
    "code": "#0E1015",
    "glow": "rgba(255,255,255,.05)",
    "shadow": "0 20px 55px rgba(0,0,0,.48)",
    "halo": "rgba(237,239,244,.18)",
    "halo_soft": "rgba(237,239,244,.045)",
    "danger": "#F87171",
    "ok": "#4ADE80",
}

_LIGHT = {
    "bg": "#F7F7F5",
    "sidebar": "#EFEFEC",
    "surface": "#FFFFFF",
    "surface2": "#F2F2EE",
    "surface_hover": "#E9E9E3",
    "border": "#DEDED6",
    "border_soft": "#EAEAE4",
    "border_strong": "#C7C7BD",
    "text": "#1B1C1F",
    "muted": "#6B6F76",
    "nav": "#4B4F57",
    "crown": "#17181B",
    "user_bubble": "#F1F1EC",
    "code": "#F2F2EE",
    "glow": "rgba(20,24,40,.035)",
    "shadow": "0 18px 45px rgba(20,24,40,.10)",
    "halo": "rgba(20,24,40,.10)",
    "halo_soft": "rgba(20,24,40,.03)",
    "danger": "#B42318",
    "ok": "#15803D",
}

_FONT_SIZES = {"Pequeno": "0.93rem", "Padrão": "1rem", "Grande": "1.13rem"}
_DENSITY = {"Compacto": "0.18rem", "Confortável": "0.4rem"}


def _tokens(t: dict, accent: str, contrast: str, font: str, density: str) -> str:
    return (
        f"--et-bg:{t['bg']};--et-sidebar:{t['sidebar']};--et-surface:{t['surface']};"
        f"--et-surface-2:{t['surface2']};--et-surface-hover:{t['surface_hover']};"
        f"--et-border:{t['border']};--et-border-soft:{t['border_soft']};"
        f"--et-border-strong:{t['border_strong']};--et-text:{t['text']};"
        f"--et-muted:{t['muted']};--et-nav:{t['nav']};--et-crown:{t['crown']};"
        f"--et-user-bubble:{t['user_bubble']};--et-code-bg:{t['code']};"
        f"--et-glow:{t['glow']};--et-shadow:{t['shadow']};"
        f"--et-halo:{t['halo']};--et-halo-soft:{t['halo_soft']};"
        f"--et-danger:{t['danger']};--et-ok:{t['ok']};"
        f"--et-accent:{accent};--et-accent-contrast:{contrast};"
        f"--et-text-size:{font};--et-density:{density};"
    )


_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;450;500;600;700&family=Instrument+Serif:ital@0;1&display=swap');

:root {
  __ROOT_TOKENS__
  --et-font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --et-serif: 'Instrument Serif', 'Iowan Old Style', Georgia, 'Times New Roman', serif;
  --et-mono: 'SFMono-Regular', ui-monospace, Menlo, Consolas, monospace;
  --et-ease: cubic-bezier(.22,.61,.36,1);
  --et-r-sm: 10px; --et-r-md: 14px; --et-r-lg: 20px; --et-r-xl: 26px;
  color-scheme: dark;
}
__LIGHT_MEDIA__
__EXTRA__

html { scrollbar-width: thin; scrollbar-color: var(--et-border) transparent; }
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-thumb { background: var(--et-border); border-radius: 99px; }
::-webkit-scrollbar-track { background: transparent; }
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
button, input, textarea, select, [class*="css"] {
  font-family: var(--et-font) !important;
}
.stApp {
  background:
    radial-gradient(1000px 560px at 50% -22%, var(--et-glow), transparent 68%),
    var(--et-bg);
  color: var(--et-text);
}
#MainMenu, footer, [data-testid="stDecoration"], [data-testid="stStatusWidget"] { display: none !important; }
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { background: transparent !important; }
[data-testid="stToolbar"] button { color: var(--et-muted) !important; }
[data-testid="stAppViewContainer"] { background: transparent; }
[data-testid="stMain"] { background: transparent; }

/* A navegação móvel nativa continua disponível. */
[data-testid="stSidebarCollapsedControl"] { display: flex !important; visibility: visible !important; z-index: 1000000; }
[data-testid="stSidebarCollapsedControl"] button {
  background: var(--et-surface) !important; color: var(--et-text) !important;
  border: 1px solid var(--et-border) !important; border-radius: 10px !important;
}

[data-testid="stMainBlockContainer"], .block-container {
  max-width: 880px !important;
  padding: 1.15rem 2rem 7.5rem !important;
}
[data-testid="stVerticalBlock"] { gap: .28rem; }

/* ── Barra lateral ─────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: var(--et-sidebar) !important;
  border-right: 1px solid var(--et-border);
  width: 288px !important;
  min-width: 288px !important;
}
[data-testid="stSidebarHeader"] { padding: .55rem .55rem .1rem !important; }
[data-testid="stSidebarContent"] { background: transparent !important; }
[data-testid="stSidebarUserContent"] { padding: .2rem .55rem 1rem !important; }
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: .05rem; }
[data-testid="stMarkdownContainer"] { margin-bottom: 0 !important; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] { margin-bottom: 0 !important; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: var(--et-text); }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p { color: var(--et-muted); font-size: .74rem; }
[data-testid="stSidebar"] .stButton > button {
  width: 100%; min-height: 34px; padding: .22rem .5rem !important;
  justify-content: flex-start; text-align: left; gap: .55rem;
  background: transparent !important; border: 1px solid transparent !important;
  color: var(--et-nav) !important; border-radius: 9px !important;
  font-size: .875rem; font-weight: 450; box-shadow: none !important;
  transition: background .14s, color .14s, border-color .14s;
}
[data-testid="stSidebar"] .stButton > button > div { width: 100%; justify-content: flex-start !important; }
[data-testid="stSidebar"] .stButton > button p {
  font-size: .875rem; font-weight: 450; text-align: left !important;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%;
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: var(--et-surface-2) !important; color: var(--et-text) !important;
  border-color: transparent !important;
}
[data-testid="stSidebar"] button[kind="primary"] {
  background: var(--et-surface-2) !important; color: var(--et-text) !important;
  border-color: transparent !important;
}
[data-testid="stSidebar"] button[kind="primary"] p { font-weight: 550; }
[data-testid="stSidebar"] [data-testid="stIconMaterial"] { font-size: 18px; color: currentColor; opacity: .9; }

.st-key-et_nav_new button {
  border: 1px solid var(--et-border) !important;
  background: var(--et-surface) !important;
  min-height: 36px !important;
  margin-bottom: .3rem;
}
.st-key-et_nav_new button:hover { background: var(--et-surface-2) !important; }

[class*="st-key-et_conv_open_"] button { min-height: 31px !important; color: var(--et-muted) !important; font-size: .84rem !important; }
[class*="st-key-et_conv_open_"] button p { color: var(--et-muted) !important; font-weight: 400 !important; }
[class*="st-key-et_conv_open_"] button:hover p { color: var(--et-text) !important; }
[class*="st-key-et_conv_open_"] button:hover { color: var(--et-text) !important; }
[class*="st-key-et_conv_menu_"] [data-testid="stPopoverButton"] {
  min-height: 26px !important; height: 26px; width: 26px; padding: 0 !important;
  justify-content: center; border-radius: 7px !important; font-size: .9rem;
  background: transparent !important; border: 1px solid transparent !important;
  color: var(--et-muted) !important;
}
[class*="st-key-et_conv_menu_"] [data-testid="stPopoverButton"]:hover {
  background: var(--et-surface-2) !important; color: var(--et-text) !important;
}

.et-brand { display: flex; align-items: center; gap: .5rem; padding: .15rem .45rem .55rem; }
.et-brand-crown { display: inline-flex; color: var(--et-crown); }
.et-brand-glyph { filter: drop-shadow(0 1px 3px rgba(0,0,0,.45)); }
.et-brand-name { font-size: 1.02rem; font-weight: 600; letter-spacing: -.015em; color: var(--et-text); }
.et-side-label {
  font-size: .7rem; font-weight: 600; color: var(--et-muted);
  padding: .1rem .5rem; margin: .85rem 0 .2rem;
}
.et-side-rule { height: 1px; background: var(--et-border); margin: .65rem .2rem; }
.et-side-note { color: var(--et-muted); font-size: .74rem; padding: .2rem .5rem; }

[class*="st-key-et_recents"] { max-height: 44vh; overflow-y: auto; overflow-x: hidden; padding-right: 2px; scrollbar-width: thin; }
[class*="st-key-et_recents"]::-webkit-scrollbar { width: 6px; }
[class*="st-key-et_recents"]::-webkit-scrollbar-thumb { background: var(--et-border); border-radius: 99px; }

[data-testid="stSidebar"] [data-testid="stTextInput"] { margin: .85rem 0 .35rem !important; }
[data-testid="stSidebar"] [data-baseweb="input"] {
  background: var(--et-surface) !important; border: 1px solid transparent !important;
  border-radius: 9px !important; min-height: 32px;
}
[data-testid="stSidebar"] [data-baseweb="input"]:focus-within { border-color: var(--et-border-strong) !important; }
[data-testid="stSidebar"] input { font-size: .82rem !important; color: var(--et-text) !important; }
[data-testid="stSidebar"] input::placeholder { color: var(--et-muted) !important; }

.st-key-et_account [data-testid="stPopoverButton"] {
  width: 100%; justify-content: flex-start; gap: .5rem;
  background: var(--et-surface) !important; border: 1px solid var(--et-border) !important;
  border-radius: 11px !important; min-height: 38px; color: var(--et-text) !important;
  font-size: .85rem !important; font-weight: 500;
}
.st-key-et_account [data-testid="stPopoverButton"] p {
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
[class*="st-key-et_account_note"] { margin-top: .1rem; }
.et-account-note { display: flex; align-items: center; gap: .35rem; color: var(--et-muted); font-size: .72rem; padding: .15rem .45rem; }
.et-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--et-ok); display: inline-block; }
.et-dot.warn { background: #FBBF24; }
.et-dot.error { background: var(--et-danger); }

/* ── Botões, campos e menus ───────────────────────────────────── */
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button {
  border-radius: var(--et-r-sm) !important; min-height: 36px;
  background: var(--et-surface) !important; color: var(--et-text) !important;
  border: 1px solid var(--et-border) !important; box-shadow: none !important;
  font-size: .87rem; font-weight: 500;
  transition: background .14s, border-color .14s, color .14s;
}
.stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
  background: var(--et-surface-2) !important; border-color: var(--et-border-strong) !important; color: var(--et-text) !important;
}
.stButton > button[kind="primary"], [data-testid="stBaseButton-primary"], [data-testid="stFormSubmitButton"] > button[kind="primary"] {
  background: var(--et-accent) !important; color: var(--et-accent-contrast) !important;
  border-color: var(--et-accent) !important; font-weight: 600;
}
.stButton > button[kind="primary"]:hover { filter: brightness(.94); color: var(--et-accent-contrast) !important; }
.stButton > button[kind="primary"] p, [data-testid="stBaseButton-primary"] p, [data-testid="stFormSubmitButton"] > button[kind="primary"] p { color: var(--et-accent-contrast) !important; }
.stButton > button[kind="tertiary"] { background: transparent !important; border-color: transparent !important; color: var(--et-muted) !important; }
.stButton > button:disabled, .stDownloadButton > button:disabled { opacity: .45; }
button:focus-visible, textarea:focus-visible, input:focus-visible, [role="tab"]:focus-visible {
  outline: 2px solid var(--et-accent) !important; outline-offset: 2px !important; box-shadow: none !important;
}

[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea, [data-testid="stNumberInput"] input,
[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div {
  background: var(--et-surface) !important; color: var(--et-text) !important;
  border-color: var(--et-border) !important; border-radius: var(--et-r-sm) !important;
}
[data-testid="stTextInput"] input::placeholder, [data-testid="stTextArea"] textarea::placeholder { color: var(--et-muted) !important; }
[data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label { color: var(--et-muted) !important; font-size: .8rem !important; }
[data-baseweb="select"] [data-testid="stMarkdownContainer"] p { color: var(--et-text); font-size: .87rem; }
[data-baseweb="popover"], [data-baseweb="menu"] { background: var(--et-surface) !important; }
[data-baseweb="popover"] li, [data-baseweb="menu"] li { background: var(--et-surface) !important; color: var(--et-text) !important; }
[data-baseweb="popover"] li:hover, [data-baseweb="menu"] li:hover { background: var(--et-surface-2) !important; }
[data-baseweb="popover"] [aria-selected="true"] { background: var(--et-surface-2) !important; color: var(--et-text) !important; }

[data-testid="stPopoverButton"] {
  border-radius: 999px !important; border: 1px solid var(--et-border) !important;
  background: var(--et-surface) !important; color: var(--et-text) !important;
  min-height: 32px; font-size: .82rem !important; box-shadow: none !important;
  transition: background .14s, border-color .14s;
}
[data-testid="stPopoverButton"]:hover { background: var(--et-surface-2) !important; border-color: var(--et-border-strong) !important; }
[data-testid="stPopoverButton"] p { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: .82rem !important; }
[data-testid="stPopoverBody"] {
  background: var(--et-surface) !important; border: 1px solid var(--et-border) !important;
  border-radius: var(--et-r-md) !important; box-shadow: 0 22px 60px rgba(0,0,0,.5) !important;
}
[data-testid="stPopoverBody"] .stButton > button {
  justify-content: flex-start; text-align: left; white-space: normal;
  background: transparent !important; border-color: transparent !important; min-height: 32px;
}
[data-testid="stPopoverBody"] .stButton > button > div { justify-content: flex-start !important; }
[data-testid="stPopoverBody"] .stButton > button p { white-space: normal; text-align: left !important; line-height: 1.35; font-size: .83rem; }
[data-testid="stPopoverBody"] .stButton > button[kind="primary"] {
  background: var(--et-surface-2) !important; color: var(--et-text) !important;
  border-color: var(--et-border) !important;
}
.et-menu-title { font-size: .68rem; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--et-muted); margin: .2rem .1rem .35rem; }
.et-menu-note { color: var(--et-muted); font-size: .74rem; line-height: 1.5; margin: .35rem .1rem .1rem; }

[data-testid="stSidebar"] hr, hr { border-color: var(--et-border) !important; }
[data-testid="stExpander"] { border: 1px solid var(--et-border) !important; border-radius: var(--et-r-md) !important; background: var(--et-surface); }
[data-testid="stExpander"] summary { color: var(--et-text) !important; }
[data-testid="stAlert"] { border-radius: var(--et-r-md); border: 1px solid var(--et-border); }
[data-testid="stAlertContainer"] {
  background: var(--et-surface) !important; border: 1px solid var(--et-border) !important;
  border-radius: var(--et-r-md) !important;
}
[data-testid^="stAlertContent"] { background: transparent !important; }
[data-testid^="stAlertContent"] p, [data-testid="stAlert"] p {
  font-size: .84rem !important; line-height: 1.5 !important; color: var(--et-text) !important;
}
[data-testid="stSelectbox"] [role="group"] {
  background: var(--et-surface) !important; border: 1px solid var(--et-border) !important;
  border-radius: var(--et-r-sm) !important; color: var(--et-text) !important;
}
[data-testid="stSelectbox"] [role="combobox"], [data-testid="stSelectbox"] input { color: var(--et-text) !important; }
[role="listbox"] { background: var(--et-surface) !important; color: var(--et-text) !important; border: 1px solid var(--et-border) !important; }
[role="option"] { color: var(--et-text) !important; }
[role="option"]:hover, [role="option"][data-selected="true"] { background: var(--et-surface-2) !important; }
[data-testid="stImage"] img { border-radius: var(--et-r-md); }
[data-testid="stFileUploaderDropzone"] {
  background: var(--et-surface) !important; border: 1px dashed var(--et-border-strong) !important;
  border-radius: var(--et-r-md) !important; color: var(--et-muted) !important;
}
[data-testid="stFileUploaderDropzone"]:hover { border-color: var(--et-accent) !important; }
[data-testid="stFileUploaderDropzone"] button { background: var(--et-surface-2) !important; color: var(--et-text) !important; border: 1px solid var(--et-border) !important; }
[data-testid="stCameraInput"] video, [data-testid="stCameraInput"] img { border-radius: var(--et-r-md); }

[role="tablist"], [data-baseweb="tab-list"] {
  gap: .15rem; border-bottom: 1px solid var(--et-border) !important;
  background: transparent !important; padding: 0 !important;
}
[data-testid="stTab"], [data-baseweb="tab"] {
  background: transparent !important; color: var(--et-muted) !important;
  font-size: .85rem !important; font-weight: 500; padding: .45rem .15rem !important;
  margin-right: 1.1rem; min-height: 32px; border-radius: 0 !important;
  cursor: pointer; box-shadow: none;
}
[data-testid="stTab"]:hover, [data-baseweb="tab"]:hover { color: var(--et-text) !important; }
[data-testid="stTab"][aria-selected="true"], [data-baseweb="tab"][aria-selected="true"] {
  color: var(--et-text) !important; box-shadow: inset 0 -2px 0 var(--et-text);
}
[role="tabpanel"], [data-baseweb="tab-panel"] { padding: .9rem 0 0 !important; }

/* ── Tipografia e Markdown ────────────────────────────────────── */
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li {
  color: var(--et-text); font-size: var(--et-text-size); line-height: 1.72;
}
[data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3, [data-testid="stMarkdownContainer"] h4 {
  color: var(--et-text); letter-spacing: -.02em; line-height: 1.3; margin-top: 1.35em;
}
[data-testid="stMarkdownContainer"] h1 { font-size: 1.5rem; }
[data-testid="stMarkdownContainer"] h2 { font-size: 1.28rem; }
[data-testid="stMarkdownContainer"] h3 { font-size: 1.1rem; }
[data-testid="stMarkdownContainer"] a { color: var(--et-accent); text-decoration: underline; text-underline-offset: 2px; }
[data-testid="stMarkdownContainer"] strong { color: var(--et-text); font-weight: 600; }
[data-testid="stMarkdownContainer"] code {
  font-family: var(--et-mono); font-size: .85em; background: var(--et-code-bg);
  border: 1px solid var(--et-border-soft); padding: .1em .34em; border-radius: 5px;
}
[data-testid="stMarkdownContainer"] pre, [data-testid="stCode"] pre {
  background: var(--et-code-bg) !important; border: 1px solid var(--et-border) !important;
  border-radius: var(--et-r-md) !important;
}
[data-testid="stMarkdownContainer"] pre code { background: transparent !important; border: 0 !important; padding: 0 !important; }
[data-testid="stMarkdownContainer"] table { display: block; overflow-x: auto; border-collapse: collapse; }
[data-testid="stMarkdownContainer"] th, [data-testid="stMarkdownContainer"] td { border-color: var(--et-border) !important; }
[data-testid="stMarkdownContainer"] blockquote {
  border-left: 2px solid var(--et-border-strong); color: var(--et-muted);
  margin-left: 0; padding-left: .9rem;
}
[data-testid="stCaptionContainer"] p { color: var(--et-muted) !important; font-size: .76rem; line-height: 1.5; }

/* ── Cabeçalho e página ───────────────────────────────────────── */
.et-chat-title {
  font-size: .95rem; font-weight: 500; color: var(--et-text);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding: .3rem 0;
}

.et-page-head { padding: .3rem 0 1.15rem; border-bottom: 1px solid var(--et-border-soft); margin-bottom: 1.1rem; }
.et-page-eyebrow {
  display: flex; align-items: center; gap: .4rem; color: var(--et-muted);
  font-size: .7rem; font-weight: 600; letter-spacing: .07em; text-transform: uppercase;
}
.et-page-glyph { color: var(--et-crown); opacity: .9; }
.et-page-title { font-size: 1.5rem; font-weight: 600; letter-spacing: -.025em; margin: .35rem 0 .2rem; }
.et-page-sub { color: var(--et-muted); font-size: .89rem; line-height: 1.55; max-width: 62ch; }

.et-empty {
  border: 1px dashed var(--et-border); border-radius: var(--et-r-md);
  padding: 1.3rem 1rem; text-align: center; background: var(--et-surface);
}
.et-empty-title { font-size: .9rem; font-weight: 600; color: var(--et-text); }
.et-empty-text { color: var(--et-muted); font-size: .82rem; margin-top: .25rem; line-height: 1.5; }

[class*="st-key-et_card_"] {
  border: 1px solid var(--et-border); border-radius: var(--et-r-md);
  background: var(--et-surface); padding: .85rem 1rem; margin-bottom: .55rem;
}
.et-card-title { font-size: .93rem; font-weight: 550; color: var(--et-text); display: flex; align-items: center; gap: .45rem; }
.et-card-text { color: var(--et-muted); font-size: .82rem; line-height: 1.55; margin-top: .15rem; }
.et-card-meta { color: var(--et-muted); font-size: .73rem; margin-top: .3rem; display: flex; flex-wrap: wrap; gap: .55rem; }
.et-badge {
  display: inline-flex; align-items: center; gap: .25rem; font-size: .68rem; font-weight: 600;
  color: var(--et-text); background: var(--et-surface-2); border: 1px solid var(--et-border);
  padding: .08rem .4rem; border-radius: 999px;
}
.et-section-label { font-size: .7rem; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--et-muted); margin: 1.15rem 0 .3rem; }
.et-list-row { padding: .5rem 0; border-bottom: 1px solid var(--et-border-soft); }
.et-list-row:last-child { border-bottom: 0; }
.et-list-text { font-size: .85rem; color: var(--et-text); line-height: 1.55; overflow-wrap: anywhere; }
.et-danger-zone { border: 1px solid var(--et-border); border-radius: var(--et-r-md); padding: .8rem .9rem; background: var(--et-surface); margin-top: .6rem; }

/* ── Mensagens ────────────────────────────────────────────────── */
[class*="st-key-et_msg_"] { margin: .15rem 0 .9rem; }
.et-msg-user { display: flex; justify-content: flex-end; margin: 1.1rem 0 .1rem; }
.et-msg-user-bubble {
  max-width: min(78%, 620px); background: var(--et-user-bubble);
  border: 1px solid var(--et-border-soft); border-radius: 18px 18px 6px 18px;
  padding: .62rem .9rem; color: var(--et-text); font-size: var(--et-text-size);
  line-height: 1.66; overflow-wrap: anywhere;
}
.et-msg-user-bubble img { display: block; max-width: 200px; width: 100%; border-radius: 10px; margin: 0 0 .45rem; }
.et-msg-note { color: var(--et-muted); font-size: .72rem; margin-bottom: .3rem; }

/* ── Boas-vindas ──────────────────────────────────────────────── */
.et-welcome {
  text-align: center; padding: clamp(2.4rem, 11vh, 6.2rem) 0 1.15rem;
  animation: et-fade-in .45s var(--et-ease) both;
}
.et-welcome-mark { position: relative; display: inline-grid; place-items: center; width: 78px; height: 78px; }
.et-welcome-halo {
  position: absolute; inset: -12px; border-radius: 50%;
  background: radial-gradient(closest-side, var(--et-halo), transparent 72%);
  filter: blur(5px); animation: et-halo 5s ease-in-out infinite;
}
.et-welcome-glyph {
  position: relative; color: var(--et-crown); display: block;
  filter: drop-shadow(0 6px 22px var(--et-halo));
  animation: et-welcome-crown .6s var(--et-ease) both;
}
.et-welcome h1 {
  font-family: var(--et-serif); font-weight: 400; font-style: normal;
  font-size: clamp(2.05rem, 1.5rem + 2vw, 2.9rem); line-height: 1.08;
  letter-spacing: -.015em; color: var(--et-text); margin: .85rem 0 .3rem;
  animation: et-rise .55s .08s var(--et-ease) both;
}
.et-welcome p {
  color: var(--et-muted); font-size: .98rem; margin: 0;
  animation: et-rise .55s .16s var(--et-ease) both;
}
.et-disclaimer { text-align: center; color: var(--et-muted); font-size: .72rem; margin: .45rem 0 0; }

[class*="st-key-et_suggestions"] {
  max-width: 600px; margin: 1.35rem auto 0;
  animation: et-rise .5s .28s var(--et-ease) both;
}
[class*="st-key-et_suggestions"] .stButton > button {
  min-height: 44px !important; justify-content: flex-start; text-align: left;
  background: transparent !important; border: 1px solid var(--et-border) !important;
  border-radius: 11px !important; color: var(--et-muted) !important;
  padding: .5rem .8rem !important; font-size: .86rem; font-weight: 450;
}
[class*="st-key-et_suggestions"] .stButton > button > div { justify-content: flex-start !important; }
[class*="st-key-et_suggestions"] .stButton > button p { text-align: left !important; font-size: .86rem; }
[class*="st-key-et_suggestions"] .stButton > button:hover {
  background: var(--et-surface) !important; color: var(--et-text) !important;
  border-color: var(--et-border-strong) !important;
}

/* ── Compositor ───────────────────────────────────────────────── */
[class*="st-key-et_composer"] {
  max-width: 820px; margin: 0 auto; background: var(--et-surface);
  border: 1px solid var(--et-border); border-radius: var(--et-r-xl);
  padding: .55rem .55rem .38rem; box-shadow: var(--et-shadow);
  transition: border-color .16s, box-shadow .16s;
}
[class*="st-key-et_composer"]:focus-within {
  border-color: var(--et-border-strong);
  box-shadow: 0 0 0 3px var(--et-halo-soft), var(--et-shadow);
}
[class*="st-key-et_composer"] [data-testid="stChatInput"] {
  background: transparent !important; border: 0 !important; border-radius: 18px !important;
  box-shadow: none !important; padding: 0 !important; max-width: 100% !important; margin: 0 !important;
}
[class*="st-key-et_composer"] [data-testid="stChatInput"] > div { background: transparent !important; border: 0 !important; }
[class*="st-key-et_composer"] [data-testid="stChatInput"] textarea {
  background: transparent !important; color: var(--et-text) !important;
  font-size: .97rem !important; line-height: 1.55 !important;
  padding: .42rem .35rem !important; min-height: 30px !important;
}
[class*="st-key-et_composer"] [data-testid="stChatInput"] textarea::placeholder { color: var(--et-muted) !important; }
[class*="st-key-et_composer"] [data-testid="stChatInput"] button {
  background: transparent !important; border: 0 !important; color: var(--et-muted) !important;
  min-width: 32px; min-height: 32px;
}
[class*="st-key-et_composer"] [data-testid="stChatInputSubmitButton"] {
  background: var(--et-accent) !important; color: var(--et-accent-contrast) !important;
  border-radius: 999px !important; width: 32px !important; height: 32px !important; min-height: 32px !important;
}
[class*="st-key-et_composer"] [data-testid="stChatInputSubmitButton"]:disabled {
  background: var(--et-surface-2) !important; color: var(--et-muted) !important;
}
[class*="st-key-et_composer_controls"] { padding: .1rem .1rem 0 !important; }
[class*="st-key-et_composer_controls"] [data-testid="stPopoverButton"] {
  width: 100%; justify-content: flex-start; min-height: 28px; padding: .1rem .45rem !important;
  background: transparent !important; border: 1px solid transparent !important;
  color: var(--et-muted) !important; border-radius: 8px !important; font-size: .78rem !important;
}
[class*="st-key-et_composer_controls"] [data-testid="stPopoverButton"]:hover {
  background: var(--et-surface-2) !important; color: var(--et-text) !important;
}
[class*="st-key-et_composer_controls"] [data-testid="stIconMaterial"] { font-size: 17px; }
.et-active-tools { display: flex; gap: .5rem; padding: .1rem .55rem .15rem; flex-wrap: wrap; }
.et-tool-chip { font-size: .68rem; color: var(--et-text); background: var(--et-surface-2); border: 1px solid var(--et-border); border-radius: 999px; padding: .05rem .45rem; }
.et-attach-chips { display: flex; gap: .35rem; flex-wrap: wrap; padding: .1rem .55rem .35rem; }
.et-attach-chip { max-width: 230px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: .68rem; color: var(--et-muted); border: 1px dashed var(--et-border); border-radius: 999px; padding: .05rem .45rem; }
.et-model-static { display: flex; justify-content: flex-end; align-items: baseline; gap: .35rem; padding-right: .3rem; }
.et-model-name { color: var(--et-text); font-size: .76rem; font-weight: 600; }
.et-model-sub { color: var(--et-muted); font-size: .68rem; }
[class*="st-key-et_think_more_"] button[kind="primary"] { background: var(--et-accent) !important; color: var(--et-accent-contrast) !important; }
.et-sources { display: flex; flex-wrap: wrap; gap: .25rem .55rem; align-items: baseline; margin: .5rem 0 .1rem; font-size: .72rem; color: var(--et-muted); }
.et-sources-label { font-weight: 600; letter-spacing: .02em; }
.et-sources a { color: var(--et-muted); text-decoration: none; border-bottom: 1px solid var(--et-border); }
.et-sources a:hover { color: var(--et-text); border-color: var(--et-text); }

[data-testid="stBottom"] {
  background: linear-gradient(to top, var(--et-bg) 62%, color-mix(in srgb, var(--et-bg) 55%, transparent) 88%, transparent) !important;
}
[data-testid="stBottom"] > div, [data-testid="stBottomBlockContainer"] { background: transparent !important; }
[data-testid="stBottomBlockContainer"] {
  max-width: 880px !important; margin: 0 auto !important;
  padding: .2rem 2rem max(.65rem, env(safe-area-inset-bottom)) !important;
}

/* ── Animação oficial de pensamento ───────────────────────────── */
.et-think {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  height: 188px; margin: .35rem 0 .1rem; overflow: hidden;
  animation: et-fade-in .25s var(--et-ease) both;
}
.et-think-stage { position: relative; width: 280px; height: 132px; display: grid; place-items: center; }
.et-think-halo {
  position: absolute; inset: 4% 2%; border-radius: 50%;
  background: radial-gradient(closest-side, var(--et-halo), var(--et-halo-soft) 55%, transparent 76%);
  filter: blur(7px); animation: et-halo 4.6s ease-in-out infinite;
}
.et-think-crown {
  position: relative; z-index: 6; display: grid; place-items: center;
  color: var(--et-crown); filter: drop-shadow(0 0 16px var(--et-halo));
  animation: et-crown-pulse 3.8s ease-in-out infinite;
}
.et-crown-glyph { display: block; }
.et-orbit { position: absolute; left: 50%; top: 50%; width: 0; height: 0; z-index: 1; }
.et-orbit-plane { position: absolute; left: 0; top: 0; width: 0; height: 0; }
.et-orbit.o1 .et-orbit-plane { transform: rotate(-15deg); }
.et-orbit.o2 .et-orbit-plane { transform: rotate(9deg); }
.et-orbit.o3 .et-orbit-plane { transform: rotate(24deg); z-index: 7; }
.et-orbit-ring {
  position: absolute; left: 0; top: 0; transform: translate(-50%, -50%);
  border-radius: 50%; border: 1px solid color-mix(in srgb, var(--et-crown) 18%, transparent);
  animation: et-ring-breathe 5.2s ease-in-out infinite;
}
.et-orbit.o1 .et-orbit-ring { width: 250px; height: 110px; }
.et-orbit.o2 .et-orbit-ring {
  width: 214px; height: 120px; border-style: dashed;
  border-color: color-mix(in srgb, var(--et-crown) 13%, transparent);
}
.et-orbit.o3 .et-orbit-ring { width: 268px; height: 92px; opacity: .8; }
.et-particle {
  position: absolute; left: 0; top: 0; width: 11px; height: 11px;
  margin: -5.5px 0 0 -5.5px; border-radius: 50%;
}
.et-orbit.o2 .et-particle { width: 8px; height: 8px; margin: -4px 0 0 -4px; }
.et-orbit.o3 .et-particle { width: 6px; height: 6px; margin: -3px 0 0 -3px; }
.et-orbit.o1 .et-particle { animation: et-path-a 16s linear infinite; animation-delay: -3s; }
.et-orbit.o2 .et-particle { animation: et-path-b 23s linear infinite reverse; animation-delay: -11s; }
.et-orbit.o3 .et-particle { animation: et-path-c 31s linear infinite; animation-delay: -21s; }
.et-particle b {
  display: block; width: 100%; height: 100%; border-radius: 50%; background: var(--et-crown);
  box-shadow: 0 0 8px color-mix(in srgb, var(--et-crown) 90%, transparent),
              0 0 22px color-mix(in srgb, var(--et-crown) 40%, transparent);
  animation: et-particle-pulse 3s ease-in-out infinite;
}
.et-orbit.o2 .et-particle b { animation-delay: -1.1s; animation-duration: 3.7s; }
.et-orbit.o3 .et-particle b { animation-delay: -2.2s; animation-duration: 4.4s; }
.et-think-label {
  display: flex; align-items: baseline; gap: .3rem; margin-top: .3rem;
  color: var(--et-muted); font-size: .85rem;
}
.et-think-label strong { color: var(--et-text); font-weight: 600; }
.et-search-pulse { width: 6px; height: 6px; border-radius: 50%; align-self: center; margin-right: .1rem; background: var(--et-crown); animation: et-search-ping 1.6s ease-out infinite; }
.et-think.is-searching .et-think-halo { filter: blur(10px); }
.et-think.is-searching .et-orbit.o1 .et-particle { animation-duration: 9s; }
.et-think.is-searching .et-orbit.o2 .et-particle { animation-duration: 13s; }
.et-think.is-searching .et-orbit.o3 .et-particle { animation-duration: 18s; }
.et-think-ellipsis { display: inline-flex; gap: 3px; margin-left: 1px; align-self: center; }
.et-think-ellipsis i {
  width: 3px; height: 3px; border-radius: 50%; background: currentColor;
  animation: et-dot 1.4s ease-in-out infinite;
}
.et-think-ellipsis i:nth-child(2) { animation-delay: .18s; }
.et-think-ellipsis i:nth-child(3) { animation-delay: .36s; }
.et-think.is-ending { animation: et-think-collapse .5s var(--et-ease) forwards; }
.et-think.is-ending .et-orbit { animation: et-fade-out .3s ease forwards; }
.et-think.is-ending .et-think-crown { animation: et-fade-out .34s ease forwards; }
.et-think.is-ending .et-think-halo { animation: et-fade-out .3s ease forwards; }

@keyframes et-search-ping {
  0% { box-shadow: 0 0 0 0 color-mix(in srgb, var(--et-crown) 40%, transparent); }
  100% { box-shadow: 0 0 0 9px transparent; }
}

@keyframes et-path-a {
  0% { transform: translate(125.00px, 0.00px); }
  6.25% { transform: translate(115.48px, 21.05px); }
  12.5% { transform: translate(88.39px, 38.89px); }
  18.75% { transform: translate(47.84px, 50.81px); }
  25% { transform: translate(0.00px, 55.00px); }
  31.25% { transform: translate(-47.84px, 50.81px); }
  37.5% { transform: translate(-88.39px, 38.89px); }
  43.75% { transform: translate(-115.48px, 21.05px); }
  50% { transform: translate(-125.00px, 0.00px); }
  56.25% { transform: translate(-115.48px, -21.05px); }
  62.5% { transform: translate(-88.39px, -38.89px); }
  68.75% { transform: translate(-47.84px, -50.81px); }
  75% { transform: translate(-0.00px, -55.00px); }
  81.25% { transform: translate(47.84px, -50.81px); }
  87.5% { transform: translate(88.39px, -38.89px); }
  93.75% { transform: translate(115.48px, -21.05px); }
  100% { transform: translate(125.00px, -0.00px); }
}
@keyframes et-path-b {
  0% { transform: translate(107.00px, 0.00px); }
  6.25% { transform: translate(98.86px, 22.96px); }
  12.5% { transform: translate(75.66px, 42.43px); }
  18.75% { transform: translate(40.95px, 55.43px); }
  25% { transform: translate(0.00px, 60.00px); }
  31.25% { transform: translate(-40.95px, 55.43px); }
  37.5% { transform: translate(-75.66px, 42.43px); }
  43.75% { transform: translate(-98.86px, 22.96px); }
  50% { transform: translate(-107.00px, 0.00px); }
  56.25% { transform: translate(-98.86px, -22.96px); }
  62.5% { transform: translate(-75.66px, -42.43px); }
  68.75% { transform: translate(-40.95px, -55.43px); }
  75% { transform: translate(-0.00px, -60.00px); }
  81.25% { transform: translate(40.95px, -55.43px); }
  87.5% { transform: translate(75.66px, -42.43px); }
  93.75% { transform: translate(98.86px, -22.96px); }
  100% { transform: translate(107.00px, -0.00px); }
}
@keyframes et-path-c {
  0% { transform: translate(134.00px, 0.00px); }
  6.25% { transform: translate(123.80px, 17.60px); }
  12.5% { transform: translate(94.75px, 32.53px); }
  18.75% { transform: translate(51.28px, 42.50px); }
  25% { transform: translate(0.00px, 46.00px); }
  31.25% { transform: translate(-51.28px, 42.50px); }
  37.5% { transform: translate(-94.75px, 32.53px); }
  43.75% { transform: translate(-123.80px, 17.60px); }
  50% { transform: translate(-134.00px, 0.00px); }
  56.25% { transform: translate(-123.80px, -17.60px); }
  62.5% { transform: translate(-94.75px, -32.53px); }
  68.75% { transform: translate(-51.28px, -42.50px); }
  75% { transform: translate(-0.00px, -46.00px); }
  81.25% { transform: translate(51.28px, -42.50px); }
  87.5% { transform: translate(94.75px, -32.53px); }
  93.75% { transform: translate(123.80px, -17.60px); }
  100% { transform: translate(134.00px, -0.00px); }
}

@keyframes et-fade-in { from { opacity: 0 } to { opacity: 1 } }
@keyframes et-fade-out { to { opacity: 0 } }
@keyframes et-rise { from { opacity: 0; transform: translateY(6px) } to { opacity: 1; transform: none } }
@keyframes et-welcome-crown { from { opacity: 0; transform: translateY(4px) scale(.94) } to { opacity: 1; transform: none } }
@keyframes et-halo { 0%,100% { opacity: .55; transform: scale(.97) } 50% { opacity: 1; transform: scale(1.05) } }
@keyframes et-crown-pulse { 0%,100% { transform: scale(1); opacity: .94 } 50% { transform: scale(1.035); opacity: 1 } }
@keyframes et-ring-breathe { 0%,100% { opacity: .55 } 50% { opacity: 1 } }
@keyframes et-particle-pulse { 0%,100% { opacity: .55; transform: scale(.82) } 50% { opacity: 1; transform: scale(1.12) } }
@keyframes et-dot { 0%,100% { opacity: .25 } 40% { opacity: 1 } }
@keyframes et-think-collapse { to { height: 0; opacity: 0; margin: 0; } }

/* ── Autenticação ─────────────────────────────────────────────── *//* ── Autenticação ─────────────────────────────────────────────── */
.et-auth-hero { text-align: center; padding: clamp(1.4rem, 8vh, 4.6rem) 0 1.4rem; }
.et-auth-crown { display: inline-flex; color: var(--et-crown); filter: drop-shadow(0 6px 24px var(--et-halo)); }
.et-auth-name { font-family: var(--et-serif); font-size: 2.15rem; letter-spacing: -.01em; margin-top: .5rem; color: var(--et-text); }
.et-auth-slogan { color: var(--et-text); font-size: .93rem; margin: .2rem 0 0; }
.et-auth-sub { color: var(--et-muted); font-size: .82rem; margin: .2rem 0 0; }
[class*="st-key-et_auth_card"] {
  max-width: 404px; margin: 0 auto; background: var(--et-surface);
  border: 1px solid var(--et-border); border-radius: var(--et-r-lg);
  padding: 1rem .95rem .55rem; box-shadow: var(--et-shadow);
}
[class*="st-key-et_auth_card"] [data-baseweb="tab-list"] { justify-content: center; border-bottom: 1px solid var(--et-border) !important; }
[class*="st-key-et_auth_card"] [data-baseweb="tab"] { margin: 0 .8rem; }
[class*="st-key-et_auth_warning"] { max-width: 404px; margin: 0 auto .75rem; }
.et-auth-note { text-align: center; color: var(--et-muted); font-size: .72rem; max-width: 404px; margin: .7rem auto 0; line-height: 1.5; }
.et-setup { max-width: 560px; margin: 0 auto; text-align: center; }
.et-setup-card {
  border: 1px solid var(--et-border); border-radius: var(--et-r-lg);
  background: var(--et-surface); padding: 1.1rem 1.15rem; text-align: left; margin-top: 1rem;
}
.et-setup-card p { color: var(--et-muted); font-size: .86rem; line-height: 1.6; margin: 0; }
.et-setup-card code { color: var(--et-text); }

/* ── Responsivo ───────────────────────────────────────────────── */
/* Reforço de estado ativo da navegação (vem depois dos botões globais). */
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
  background: var(--et-surface-2) !important;
  color: var(--et-text) !important;
  border-color: transparent !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] p { color: var(--et-text) !important; }
[data-testid="stSidebar"] .stButton > button[kind="primary"] { background-image: none !important; opacity: 1 !important; }
[data-testid="stSidebar"] .stButton > button[kind="primary"] * { color: var(--et-text) !important; }
[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover { background: var(--et-surface-hover) !important; }
[data-baseweb="tab"][aria-selected="true"] { box-shadow: inset 0 -2px 0 var(--et-text); }
[data-baseweb="tab-highlight"], [data-testid="stTabHighlight"] { display: none !important; }
[data-testid="stTabBorder"], [data-baseweb="tab-border"] { display: none !important; }

@media (max-width: 1024px) {
  [data-testid="stMainBlockContainer"], .block-container { padding: 1rem 1.25rem 7.2rem !important; }
  [data-testid="stBottomBlockContainer"] { padding-left: 1.25rem !important; padding-right: 1.25rem !important; }
}
@media (max-width: 900px) {
  [data-testid="stSidebar"] { width: min(88vw, 312px) !important; min-width: min(88vw, 312px) !important; }
  [data-testid="stMainBlockContainer"], .block-container { padding: 2.4rem 1rem 7rem !important; }
  [data-testid="stBottomBlockContainer"] { padding-left: 1rem !important; padding-right: 1rem !important; }
  .et-welcome { padding-top: 2.2rem; }
  .et-welcome h1 { font-size: 1.95rem; }
  [class*="st-key-et_recents"] { max-height: 38vh; }
}
@media (max-width: 640px) {
  [data-testid="stMainBlockContainer"], .block-container { padding: .75rem .8rem 6.6rem !important; }
  [data-testid="stBottomBlockContainer"] { padding-left: .8rem !important; padding-right: .8rem !important; }
  [class*="st-key-et_composer"] { border-radius: 20px; padding: .4rem .4rem .28rem; }
  [class*="st-key-et_composer"] [data-testid="stChatInput"] textarea { font-size: .95rem !important; }
  .et-welcome h1 { font-size: 1.72rem; }
  .et-welcome p { font-size: .92rem; }
  .et-welcome-mark { width: 64px; height: 64px; }
  .et-welcome-glyph { width: 34px; height: 31px; }
  .et-msg-user-bubble { max-width: 92%; font-size: .95rem; }
  .et-page-title { font-size: 1.28rem; }
  .et-think { height: 176px; }
  .et-think-stage { transform: scale(.88); }
  .et-think-halo { inset: 8% 0; }
  [class*="st-key-et_composer_controls"] [data-testid="stPopoverButton"] { font-size: .74rem !important; padding: .1rem .25rem !important; }
  [class*="st-key-et_composer_controls"] [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: .25rem !important; }
  [class*="st-key-et_composer_controls"] [data-testid="stColumn"] { width: auto !important; flex: 1 1 33% !important; min-width: 0 !important; }
  [data-baseweb="tab"] { margin-right: .8rem; font-size: .8rem !important; }
  [data-testid="stPopoverBody"] { max-width: calc(100vw - 1.6rem); }
}
@media (max-width: 380px) {
  [data-testid="stMainBlockContainer"], .block-container { padding-left: .6rem !important; padding-right: .6rem !important; }
  .et-welcome h1 { font-size: 1.58rem; }
  .et-welcome p { font-size: .88rem; }
  .et-think-stage { transform: scale(.8); }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .001ms !important; animation-iteration-count: 1 !important;
    transition-duration: .001ms !important; scroll-behavior: auto !important;
  }
  .et-think .et-orbit { display: none !important; }
}
"""


def apply_theme(
    *,
    theme: str,
    accent_name: str,
    accent_hex: str,
    font_size: str,
    density: str,
    high_contrast: bool,
    reduce_motion: bool,
) -> None:
    """Aplica a nova camada visual. Substitui integralmente o CSS antigo."""
    font = _FONT_SIZES.get(font_size, "1rem")
    pad = _DENSITY.get(density, "0.4rem")
    neutral = accent_name in ("Branco", "Prata")
    dark_accent = accent_hex if not neutral else "#EDEFF4"
    light_accent = "#1B1C1F" if neutral else accent_hex
    dark_contrast = "#0A0B0E"
    light_contrast = "#FFFFFF" if neutral else ("#0A0B0E" if accent_name in ("Ciano", "Verde", "Rosa", "Laranja") else "#FFFFFF")

    dark_root = _tokens(_DARK, dark_accent, dark_contrast, font, pad)
    light_root = _tokens(_LIGHT, light_accent, light_contrast, font, pad)

    if theme == "Claro":
        root_tokens = light_root
        scheme = "light"
        light_media = ""
    elif theme == "Automático":
        root_tokens = dark_root
        scheme = "light dark"
        light_media = "@media (prefers-color-scheme: light) { :root { " + light_root + " } }"
    else:
        root_tokens = dark_root
        scheme = "dark"
        light_media = ""

    extra = ""
    if high_contrast:
        extra += (
            ":root { --et-border:#7C8492; --et-border-soft:#5C6472; --et-muted:#D2D7DF; }"
            "[data-testid=\"stMarkdownContainer\"] p, [data-testid=\"stMarkdownContainer\"] li { color:var(--et-text); }"
        )
    if reduce_motion:
        extra += (
            ".et-think .et-orbit { display:none !important; }"
            ".et-think, .et-think *, .et-welcome, .et-welcome *, [class*=\"st-key-et_suggestions\"] {"
            " animation:none !important; transition:none !important; }"
            ".et-think { height:150px; }"
        )

    css = (
        _CSS.replace("__ROOT_TOKENS__", root_tokens + f"--et-color-scheme:{scheme};")
        .replace("__LIGHT_MEDIA__", light_media)
        .replace("__EXTRA__", extra)
    )
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
