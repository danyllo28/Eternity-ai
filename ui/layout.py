"""Reusable page primitives for Eternity's Streamlit interface."""

from __future__ import annotations

import html

import streamlit as st

from ui.animations import CROWN_SVG


def brand(subtitle: str | None = None) -> None:
    """Render the official crown and Eternity name as a compact wordmark."""
    sub = f'<span class="et-new-brand-sub">{html.escape(subtitle)}</span>' if subtitle else ""
    st.markdown(
        '<div class="et-new-brand">'
        f'<span aria-hidden="true">{CROWN_SVG}</span>'
        '<span class="et-new-brand-name">Eternity</span>'
        f'{sub}</div>',
        unsafe_allow_html=True,
    )


def page_heading(title: str, description: str = "") -> None:
    """Render a consistent heading for models, library, memory, files, and settings."""
    subtitle = f"<p>{html.escape(description)}</p>" if description else ""
    st.markdown(
        '<header class="et-new-page-heading">'
        f'<h1>{html.escape(title)}</h1>{subtitle}</header>',
        unsafe_allow_html=True,
    )


def welcome(username: str, greeting: str) -> None:
    """Render the welcome composition; chat input remains a native Streamlit widget."""
    st.markdown(
        '<section class="et-new-welcome">'
        f'<span class="et-new-welcome-crown" aria-hidden="true">{CROWN_SVG}</span>'
        f'<h1>{html.escape(greeting)}, {html.escape(username)}.</h1>'
        '<p>O que vamos criar hoje?</p></section>',
        unsafe_allow_html=True,
    )


def chat_input(key: str = "et_new_chat_input"):
    """Keep Streamlit's native chat input and its attachment pipeline."""
    return st.chat_input(
        "Pergunte à Eternity…",
        key=key,
        accept_file="multiple",
        file_type=["png", "jpg", "jpeg", "webp", "pdf", "txt", "md", "csv", "json"],
    )
