import html
import os
import re
import uuid
from datetime import datetime

import streamlit as st
from groq import APIError, Groq

st.set_page_config(
    page_title="Eternity Atelier",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Eternity's own visual language: warm graphite surfaces, aurora accents, and a quiet star mark.
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root {
      color-scheme: dark;
      --bg:#111210; --panel:#171815; --panel-hi:#20211d; --line:#2b2d27;
      --text:#f2f1e9; --muted:#a3a599; --accent:#c7e4bd; --accent-2:#a9c5e9;
    }
    html { scroll-behavior:smooth; }
    body, [class*="css"], button, textarea, input, select { font-family:'DM Sans',sans-serif !important; }
    .stApp { background:radial-gradient(850px 460px at 53% -13%,rgba(196,222,184,.09),transparent 65%),var(--bg); color:var(--text); }
    #MainMenu, footer, [data-testid="stDecoration"], [data-testid="stStatusWidget"] {display:none!important;}
    header[data-testid="stHeader"] {background:transparent;}
    .block-container {max-width:1120px;padding:1.6rem 2rem 8.5rem;}
    [data-testid="stSidebar"] {background:#141512;border-right:1px solid var(--line);}
    [data-testid="stSidebar"] > div:first-child {padding-top:1rem;}
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {gap:.35rem;}
    [data-testid="stSidebar"] .stButton button {width:100%;text-align:left;justify-content:flex-start;background:transparent;border:1px solid transparent;color:var(--text);border-radius:12px;min-height:40px;}
    [data-testid="stSidebar"] .stButton button:hover {background:var(--panel-hi);border-color:var(--line);}
    .atelier-brand {display:flex;align-items:center;gap:.65rem;padding:.3rem .35rem 1.1rem;}
    .atelier-mark {display:grid;place-items:center;width:34px;height:34px;border:1px solid #44483e;border-radius:12px;background:linear-gradient(145deg,#272b23,#171914);color:var(--accent);font-size:1.05rem;box-shadow:0 0 24px rgba(199,228,189,.08);}
    .atelier-wordmark {font:700 1.12rem Manrope,sans-serif;letter-spacing:-.04em;}
    .atelier-submark {color:var(--muted);font-size:.72rem;letter-spacing:.04em;}
    .eyebrow {color:#b9cbb0;font-size:.73rem;font-weight:700;letter-spacing:.16em;text-transform:uppercase;}
    .welcome {max-width:760px;margin:9vh auto 1.7rem;text-align:center;animation:rise .55s cubic-bezier(.2,.8,.2,1) both;}
    .welcome-mark {display:grid;place-items:center;margin:0 auto 1.2rem;width:64px;height:64px;border:1px solid #45483e;border-radius:22px;background:linear-gradient(145deg,#25291f,#171914);color:var(--accent);font-size:1.65rem;box-shadow:0 12px 50px #0005,0 0 36px #c7e4bd12;animation:float 5s ease-in-out infinite;}
    .welcome h1 {font:700 clamp(2.15rem,5vw,3.35rem) Manrope,sans-serif;letter-spacing:-.065em;margin:0;color:var(--text);}
    .welcome p {color:var(--muted);font-size:1.03rem;line-height:1.7;margin:.65rem auto 0;max-width:560px;}
    .welcome p strong {color:#d9e7d2;font-weight:600;}
    .section-label {color:var(--muted);font-size:.72rem;font-weight:700;letter-spacing:.13em;text-transform:uppercase;margin:.9rem 0 .4rem;}
    [class*="st-key-starter_"] button {min-height:72px!important;width:100%;white-space:normal!important;text-align:left!important;justify-content:flex-start!important;background:linear-gradient(140deg,#1d1f1a,#171815)!important;border:1px solid var(--line)!important;border-radius:16px!important;color:var(--text)!important;transition:transform .18s,border-color .18s,background .18s!important;}
    [class*="st-key-starter_"] button:hover {transform:translateY(-2px);border-color:#5a6250!important;background:#20221d!important;}
    [data-testid="stChatMessage"] {animation:rise .28s ease-out both;}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,[data-testid="stChatMessage"] li {line-height:1.78;font-size:1rem;}
    [data-testid="stChatMessage"] pre {border:1px solid var(--line);border-radius:14px;}
    [data-testid="stChatMessage"] code {font-size:.9em;}
    [data-testid="stChatInput"] {max-width:850px;margin:0 auto;border:1px solid #3b3e35!important;border-radius:22px!important;background:linear-gradient(145deg,#20211d,#191a17)!important;box-shadow:0 20px 60px #0006!important;transition:border-color .2s,box-shadow .2s;}
    [data-testid="stChatInput"]:focus-within {border-color:#83987a!important;box-shadow:0 0 0 3px #c7e4bd18,0 20px 60px #0006!important;}
    [data-testid="stChatInput"] textarea {color:var(--text)!important;line-height:1.6!important;}
    [data-testid="stChatInput"] textarea::placeholder {color:#8e9186!important;}
    [data-testid="stBottom"] {background:linear-gradient(0deg,var(--bg) 67%,transparent)!important;}
    [data-testid="stBottom"] [data-testid="stCaptionContainer"] {text-align:center;}
    .stButton button,.stDownloadButton button,[data-testid="stFormSubmitButton"] button {border-radius:12px;border-color:var(--line);background:var(--panel);color:var(--text);transition:transform .16s,border-color .16s,background .16s;}
    .stButton button:hover,.stDownloadButton button:hover {border-color:#59614f;background:var(--panel-hi);color:var(--text);}
    .stButton button:active {transform:scale(.985);}
    [data-baseweb="select"] > div,[data-testid="stTextInput"] input {background:var(--panel)!important;border-color:var(--line)!important;border-radius:11px!important;color:var(--text)!important;}
    [data-testid="stExpander"] {border-color:var(--line);border-radius:14px;background:#171815;}
    .approach {margin:.3rem 0 1.1rem;padding:.75rem .95rem;border:1px solid #32372e;border-radius:13px;background:linear-gradient(110deg,#1c211a,#181a17);color:#c6cabc;font-size:.85rem;line-height:1.6;}
    .approach b {color:#e0e9d8;font-weight:600;}
    .footnote {text-align:center;color:#85887e;font-size:.75rem;margin:.75rem auto 0;}
    .st-key-send_tools [data-testid="stHorizontalBlock"] {gap:.45rem;}
    @keyframes rise {from{opacity:0;transform:translateY(9px)}to{opacity:1;transform:translateY(0)}}
    @keyframes float {0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
    @media(max-width:720px){.block-container{padding:.8rem .75rem 8rem}.welcome{margin:5vh auto 1.2rem}.welcome-mark{width:54px;height:54px;border-radius:18px}.welcome p{font-size:.94rem}[data-testid="stChatInput"]{border-radius:18px!important}}
    @media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}
    </style>
    """,
    unsafe_allow_html=True,
)

MODELS = {
    "Eternity Equilíbrio": "qwen/qwen3.8-27b",
    "Eternity Núcleo": "openai/gpt-oss-120b",
    "Eternity Ágil": "openai/gpt-oss-20b",
    "Eternity Clássica": "llama-3.3-70b-versatile",
}
MODES = {
    "Conversa": "Responda de modo natural, claro e útil.",
    "Código": "Ajude com programação: explique a causa, proponha uma solução segura e mostre código legível quando útil. Não alegue ter executado código que não executou.",
    "Escrita": "Atue como parceiro de escrita. Preserve a intenção do usuário, melhore clareza e tom e ofereça alternativas quando fizer sentido.",
    "Estudo": "Ensine com paciência, exemplos concretos e etapas verificáveis. Faça perguntas de checagem apenas quando ajudarem o aprendizado.",
}


def new_conversation():
    return {"id": uuid.uuid4().hex[:12], "title": "Nova conversa", "messages": [], "created": datetime.now().strftime("%d/%m %H:%M")}


def ensure_state():
    st.session_state.setdefault("atelier_conversations", [new_conversation()])
    st.session_state.setdefault("atelier_active", st.session_state.atelier_conversations[0]["id"])
    st.session_state.setdefault("atelier_mode", "Conversa")
    st.session_state.setdefault("atelier_model", "Eternity Equilíbrio")


def active_conversation():
    return next((c for c in st.session_state.atelier_conversations if c["id"] == st.session_state.atelier_active), st.session_state.atelier_conversations[0])


def response_stream(client, conversation, model_id, mode, effort, progress):
    system = (
        "Você é Eternity, uma assistente original, acolhedora, precisa e direta. "
        "Não revele nem simule uma transcrição de raciocínio interno privado. "
        "Para tarefas complexas, apresente uma explicação breve e verificável: premissas relevantes, "
        "método em alto nível, resultado e limitações. Separe claramente fatos de incertezas. "
        "Use Markdown com títulos e listas apenas quando melhorarem a leitura. " + MODES[mode]
    )
    messages = [{"role": "system", "content": system}]
    messages.extend({"role": m["role"], "content": m["content"]} for m in conversation["messages"][-24:])
    kwargs = {"model": model_id, "messages": messages, "stream": True, "temperature": 0.6, "max_tokens": 8192}
    if model_id.startswith("openai/gpt-oss"):
        kwargs["reasoning_effort"] = "high" if effort == "Aprofundado" else "low"
    elif model_id == "qwen/qwen3.8-27b":
        kwargs["reasoning_effort"] = "high" if effort == "Aprofundado" else "none"
        kwargs["reasoning_format"] = "hidden"
    progress.update(label="Eternity está formulando uma resposta clara…", state="running")
    stream = client.chat.completions.create(**kwargs)
    for chunk in stream:
        if chunk.choices:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta


def render_message(message):
    with st.chat_message(message["role"], avatar="✦" if message["role"] == "assistant" else "●"):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            with st.expander("Como esta resposta foi estruturada", expanded=False):
                st.caption("Resumo explicativo, não uma transcrição de raciocínio privado: a resposta destaca as conclusões e, quando útil, as premissas e verificações relevantes.")


ensure_state()
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        api_key = None

with st.sidebar:
    st.markdown('<div class="atelier-brand"><div class="atelier-mark">✦</div><div><div class="atelier-wordmark">Eternity</div><div class="atelier-submark">ATELIER · SEU ESPAÇO DE IDEIAS</div></div></div>', unsafe_allow_html=True)
    if st.button("＋  Nova conversa", key="atelier_new", use_container_width=True):
        conversation = new_conversation()
        st.session_state.atelier_conversations.append(conversation)
        st.session_state.atelier_active = conversation["id"]
        st.rerun()
    st.markdown('<div class="section-label">Personalize a conversa</div>', unsafe_allow_html=True)
    st.selectbox("Modo", list(MODES), key="atelier_mode", label_visibility="collapsed")
    st.selectbox("Modelo Eternity", list(MODELS), key="atelier_model", label="Modelo")
    effort = st.radio("Esforço", ["Rápido", "Aprofundado"], horizontal=True, help="Ajusta o esforço do modelo quando compatível. Não mostra raciocínio privado.")
    st.markdown('<div class="section-label">Recentes</div>', unsafe_allow_html=True)
    for conversation in reversed(st.session_state.atelier_conversations[-12:]):
        title = conversation["title"][:30] or "Nova conversa"
        label = ("▸ " if conversation["id"] == st.session_state.atelier_active else "") + title
        if st.button(label, key=f"atelier_open_{conversation['id']}", help=conversation["created"]):
            st.session_state.atelier_active = conversation["id"]
            st.rerun()
    if st.button("Apagar conversa atual", key="atelier_delete", help="Remove esta conversa desta sessão."):
        current_id = st.session_state.atelier_active
        st.session_state.atelier_conversations = [c for c in st.session_state.atelier_conversations if c["id"] != current_id]
        if not st.session_state.atelier_conversations:
            st.session_state.atelier_conversations = [new_conversation()]
        st.session_state.atelier_active = st.session_state.atelier_conversations[0]["id"]
        st.rerun()
    st.markdown("---")
    st.caption("Conversas deste protótipo ficam na sessão atual. O app original não é alterado.")

conversation = active_conversation()
if not api_key:
    st.markdown('<div class="welcome"><div class="welcome-mark">✦</div><div class="eyebrow">Seu espaço de criação</div><h1>Eternity Atelier</h1><p>Configure <strong>GROQ_API_KEY</strong> em Streamlit Secrets para começar. Esta é uma nova experiência visual, mantendo a identidade própria da Eternity.</p></div>', unsafe_allow_html=True)
    st.stop()

client = Groq(api_key=api_key, timeout=180, max_retries=2)

if not conversation["messages"]:
    st.markdown('<div class="welcome"><div class="welcome-mark">✦</div><div class="eyebrow">Um espaço para pensar e criar</div><h1>O que vamos fazer hoje?</h1><p>Converse, aprenda, escreva ou resolva algo difícil — <strong>no seu ritmo</strong>.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Comece por uma ideia</div>', unsafe_allow_html=True)
    starters = [
        ("✎  Escrever melhor", "Ajude-me a melhorar um texto: deixe-o mais claro, natural e convincente."),
        ("⌘  Resolver com código", "Quero ajuda com código. Primeiro, pergunte o que você precisa saber e depois proponha uma solução."),
        ("◉  Aprender algo", "Explique um conceito difícil de forma simples, usando uma analogia e um exemplo prático."),
        ("✧  Organizar uma ideia", "Ajude-me a transformar uma ideia em um plano simples, com etapas e prioridades."),
    ]
    starter_cols = st.columns(2, gap="small")
    for index, (label, prompt_text) in enumerate(starters):
        with starter_cols[index % 2]:
            if st.button(label, key=f"starter_{index}", use_container_width=True):
                st.session_state["atelier_queued_prompt"] = prompt_text
                st.rerun()
else:
    st.markdown(f'<div class="eyebrow">{html.escape(conversation["title"])}</div>', unsafe_allow_html=True)
    for message in conversation["messages"]:
        render_message(message)

st.markdown('<div class="footnote">Respostas úteis, explicações claras e uma identidade própria da Eternity.</div>', unsafe_allow_html=True)
chat_value = st.chat_input("Pergunte, escreva ou cole algo para trabalhar…")
queued = st.session_state.pop("atelier_queued_prompt", None)
user_text = (chat_value or queued or "").strip()

if user_text:
    conversation["messages"].append({"role": "user", "content": user_text})
    if conversation["title"] == "Nova conversa":
        conversation["title"] = re.sub(r"\s+", " ", user_text)[:42] or "Nova conversa"
    with st.chat_message("user", avatar="●"):
        st.markdown(user_text)
    with st.chat_message("assistant", avatar="✦"):
        with st.status("Eternity está preparando sua resposta…", expanded=False) as progress:
            st.write("Entendendo o pedido")
            st.write("Organizando uma resposta útil")
            try:
                answer = st.write_stream(response_stream(
                    client, conversation, MODELS[st.session_state.atelier_model],
                    st.session_state.atelier_mode, effort, progress,
                ))
                progress.update(label="Resposta pronta", state="complete")
            except APIError as exc:
                progress.update(label="Não consegui concluir desta vez", state="error")
                st.error("A API de linguagem não respondeu. Verifique a chave GROQ_API_KEY e os modelos disponíveis para sua conta.")
                st.caption(str(exc)[:500])
                answer = ""
    if answer:
        conversation["messages"].append({"role": "assistant", "content": answer})
        st.rerun()
elif conversation["messages"]:
    transcript = "\n\n".join(
        f"## {'Você' if m['role'] == 'user' else 'Eternity'}\n\n{m['content']}"
        for m in conversation["messages"]
    )
    st.download_button("Baixar esta conversa (.md)", transcript, file_name="conversa-eternity.md", mime="text/markdown")
