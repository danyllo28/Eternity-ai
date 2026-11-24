"""Recursos exclusivos da Eternity.

Este módulo concentra ações rápidas, leitura em voz alta, cópia, fixação de
conversas e ferramentas de estudo. Tudo foi desenhado para manter a identidade
própria da Eternity: simples, acolhedora e útil no dia a dia.
"""
from __future__ import annotations

import html
import json

import streamlit as st

from .icons import icon_svg


QUICK_ACTIONS = (
    ("Resumir", "Resuma a conversa e os pontos mais importantes de forma clara."),
    ("Explicar simples", "Explique a última resposta com palavras simples e um exemplo prático."),
    ("Continuar", "Continue a partir daqui, aprofundando o assunto sem repetir o que já foi dito."),
    ("Ideias", "Dê 5 ideias práticas e criativas relacionadas ao assunto atual."),
    ("Estudar", "Crie um plano de estudo curto, com tópicos, perguntas e um mini-teste."),
    ("Traduzir", "Traduza a última resposta para inglês, mantendo o sentido natural."),
    ("Regenerar", "Refaça a última resposta com mais clareza, precisão e um exemplo útil. Não repita o texto anterior."),
    ("Melhorar texto", "Melhore o último texto que eu enviei: deixe-o mais claro, natural e bem organizado, sem mudar o sentido."),
)


def message_actions(text: str, index: int) -> None:
    """Adiciona copiar e ouvir a qualquer resposta da Eternity."""
    cols = st.columns([0.16, 0.16, 0.68], gap="small", vertical_alignment="center")
    with cols[0]:
        if st.button("Copiar", icon=":material/content_copy:", key=f"et_copy_{index}",
                     help="Copiar esta resposta"):
            st.session_state["_et_copied"] = True
            components_copy(text, f"et_copy_target_{index}")
    with cols[1]:
        if st.button("Ouvir", icon=":material/volume_up:", key=f"et_speak_{index}",
                     help="Ler esta resposta em voz alta no navegador"):
            speak_text(text, f"et_speech_{index}")
    with cols[2]:
        if st.session_state.pop("_et_copied", False):
            st.caption("Resposta copiada.")


def components_copy(text: str, key: str) -> None:
    """Copia o texto usando a área de transferência do navegador."""
    import streamlit.components.v1 as components
    payload = json.dumps(str(text or ""))
    components.html(
        f"""
        <script>
        const data = {payload};
        navigator.clipboard.writeText(data).catch(() => {{}});
        </script>
        """,
        height=0,
    )


def speak_text(text: str, key: str) -> None:
    """Usa a voz do navegador para ler a resposta, sem depender de serviço externo."""
    import streamlit.components.v1 as components
    payload = json.dumps(str(text or ""))
    components.html(
        f"""
        <script>
        const text = {payload};
        if ('speechSynthesis' in window) {{
          window.speechSynthesis.cancel();
          const utterance = new SpeechSynthesisUtterance(text);
          utterance.lang = 'pt-BR';
          utterance.rate = 1;
          window.speechSynthesis.speak(utterance);
        }}
        </script>
        """,
        height=0,
    )


def render_quick_actions(scope: str) -> None:
    """Ações rápidas da Eternity, acima do campo de mensagem."""
    st.markdown(
        '<div class="et-quick-head">'
        f'{icon_svg("sparkle", 16, cls="et-quick-glyph")}'
        '<span>Ações rápidas da Eternity</span></div>',
        unsafe_allow_html=True,
    )
    with st.container(key=f"et_quick_actions_{scope}"):
        cols = st.columns(len(QUICK_ACTIONS), gap="small")
        for col, (label, prompt) in zip(cols, QUICK_ACTIONS):
            if col.button(label, key=f"et_quick_{scope}_{label}", width="stretch"):
                st.session_state["suggested_prompt"] = prompt
                st.rerun()


def toggle_pinned_conversation(mem: dict, conversation_id: str) -> bool:
    """Fixa ou desafixa uma conversa no histórico."""
    for conversation in mem.get("archived_conversations", []):
        if str(conversation.get("id")) == str(conversation_id):
            conversation["pinned"] = not bool(conversation.get("pinned"))
            return True
    return False


def sort_conversations(conversations: list[dict]) -> list[dict]:
    """Mostra conversas fixadas primeiro e depois as mais recentes."""
    def newest_first(items):
        return sorted(items, key=lambda c: str(c.get("created_at", "")), reverse=True)

    pinned = [c for c in conversations if c.get("pinned")]
    others = [c for c in conversations if not c.get("pinned")]
    return newest_first(pinned) + newest_first(others)
