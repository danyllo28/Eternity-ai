import html
import os
import re
import uuid
from datetime import datetime

import streamlit as st
from groq import APIError, Groq

st.set_page_config(page_title="Eternity", page_icon="✦", layout="wide", initial_sidebar_state="expanded")

# A distinct Eternity identity with the calm, spacious organization people expect from a modern chat app.
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root{color-scheme:dark;--bg:#10110f;--side:#151613;--surface:#1b1c19;--surface2:#22241f;--line:#30322c;--text:#f2f1e9;--muted:#a1a397;--accent:#c6dfb8;--accent2:#99bce3}
    html{scroll-behavior:smooth}body,[class*="css"],button,textarea,input,select{font-family:'DM Sans',sans-serif!important}
    .stApp{background:radial-gradient(850px 460px at 52% -18%,rgba(198,223,184,.07),transparent 66%),var(--bg);color:var(--text)}
    #MainMenu,footer,[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important}header[data-testid="stHeader"]{background:transparent}
    .block-container{max-width:1080px;padding:1.15rem 2rem 8.5rem}
    [data-testid="stSidebar"]{background:var(--side);border-right:1px solid #282923}[data-testid="stSidebar"]>div:first-child{padding:1rem .75rem .8rem}
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"]{gap:.24rem}
    [data-testid="stSidebar"] .stButton>button{width:100%;min-height:38px;justify-content:flex-start;text-align:left;background:transparent!important;color:#dedfd6!important;border:1px solid transparent!important;border-radius:10px!important;box-shadow:none!important;padding:.35rem .6rem!important;font-size:.88rem}
    [data-testid="stSidebar"] .stButton>button:hover{background:#24251f!important;border-color:#32342c!important}
    .brand{display:flex;align-items:center;gap:.62rem;padding:.1rem .35rem 1rem}.brand-mark{display:grid;place-items:center;width:34px;height:34px;border-radius:12px;border:1px solid #49513e;background:linear-gradient(145deg,#293022,#191b16);color:var(--accent);font-size:1.12rem;box-shadow:0 0 24px #c6dfb810}.brand-name{font:700 1.08rem Manrope,sans-serif;letter-spacing:-.04em}.brand-sub{font-size:.68rem;color:var(--muted);letter-spacing:.07em}
    .side-heading{font-size:.68rem;text-transform:uppercase;letter-spacing:.13em;color:#898c80;font-weight:700;margin:.72rem .3rem .28rem}
    .hero{text-align:center;max-width:740px;margin:9vh auto 1.2rem;animation:rise .45s ease-out both}.hero-mark{display:grid;place-items:center;width:58px;height:58px;margin:0 auto 1rem;border-radius:20px;border:1px solid #454a3d;background:linear-gradient(145deg,#25291f,#171914);color:var(--accent);font-size:1.5rem;box-shadow:0 12px 45px #0005;animation:float 5s ease-in-out infinite}.hero .eyebrow{font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:#b9c9ad;font-weight:700}.hero h1{font:700 clamp(2rem,4.7vw,3rem) Manrope,sans-serif;letter-spacing:-.065em;margin:.45rem 0;color:var(--text)}.hero p{max-width:560px;margin:0 auto;color:var(--muted);line-height:1.7;font-size:.98rem}
    .starter-title{max-width:790px;margin:1.6rem auto .55rem;color:#92958a;font-size:.71rem;font-weight:700;letter-spacing:.13em;text-transform:uppercase}
    [class*="st-key-start_" ] button{width:100%;min-height:65px!important;justify-content:flex-start!important;text-align:left!important;white-space:normal!important;border-radius:14px!important;background:linear-gradient(140deg,#1d1f1a,#181916)!important;border:1px solid #30322c!important;color:#e8e8df!important;transition:transform .17s,border-color .17s,background .17s!important}
    [class*="st-key-start_" ] button:hover{transform:translateY(-2px);border-color:#5a6451!important;background:#22241e!important}
    .topline{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #282923;padding:.1rem 0 .72rem;margin-bottom:1rem}.topline-title{font:600 .92rem Manrope,sans-serif;color:#dfe0d7;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.topline-meta{font-size:.76rem;color:#898c81}
    [data-testid="stChatMessage"]{animation:rise .23s ease-out both}[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,[data-testid="stChatMessage"] li{font-size:1rem;line-height:1.78}[data-testid="stChatMessage"] pre{border:1px solid var(--line);border-radius:13px}
    [data-testid="stChatInput"]{max-width:820px;margin:.45rem auto 0;border:1px solid #3a3d34!important;border-radius:20px!important;background:linear-gradient(145deg,#22231f,#191a17)!important;box-shadow:0 18px 55px #0005!important;transition:border-color .18s,box-shadow .18s}
    [data-testid="stChatInput"]:focus-within{border-color:#7c9272!important;box-shadow:0 0 0 3px #c6dfb815,0 18px 55px #0005!important}[data-testid="stChatInput"] textarea{color:var(--text)!important;line-height:1.6!important}[data-testid="stChatInput"] textarea::placeholder{color:#8f9187!important}
    [data-testid="stBottom"]{background:linear-gradient(0deg,var(--bg) 67%,transparent)!important}[data-testid="stBottom"] [data-testid="stCaptionContainer"]{text-align:center}
    .stButton>button,.stDownloadButton>button,[data-testid="stFormSubmitButton"]>button{border-radius:11px!important;background:var(--surface)!important;color:var(--text)!important;border:1px solid var(--line)!important;box-shadow:none!important;transition:transform .15s,border-color .15s,background .15s}.stButton>button:hover,.stDownloadButton>button:hover{border-color:#59614f!important;background:var(--surface2)!important}.stButton>button:active{transform:scale(.985)}
    [data-baseweb="select"]>div,[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea{background:var(--surface)!important;border-color:var(--line)!important;border-radius:10px!important;color:var(--text)!important}
    [data-baseweb="popover"] li,[data-baseweb="menu"] li{background:var(--surface)!important;color:var(--text)!important}
    [data-testid="stExpander"]{border-color:var(--line)!important;border-radius:13px!important;background:#171815!important}
    .model-card{padding:.75rem .85rem;margin:.38rem 0;border:1px solid var(--line);border-radius:13px;background:linear-gradient(140deg,#1e201b,#181916)}.model-card.active{border-color:#758469;background:linear-gradient(140deg,#242a20,#191b17)}.model-title{font-size:.89rem;font-weight:650;color:#eeeee6}.model-desc{font-size:.75rem;color:#9da093;margin-top:.17rem;line-height:1.5}.model-tag{font-size:.65rem;color:#c7d9bb;letter-spacing:.05em;text-transform:uppercase;margin-top:.35rem}
    .composer-tools{max-width:820px;margin:.7rem auto 0}.composer-caption{max-width:820px;margin:.45rem auto 0;text-align:center;color:#85887e;font-size:.73rem}
    .approach{margin:.5rem 0 .9rem;padding:.78rem .95rem;border:1px solid #34382f;border-radius:13px;background:linear-gradient(110deg,#1c211a,#181a17);color:#c4c9bb;font-size:.84rem;line-height:1.62}.approach b{color:#e0e9d8}
    .account-row{display:flex;align-items:center;gap:.55rem;padding:.65rem .3rem;color:#d9dad1;font-size:.82rem}.account-dot{width:27px;height:27px;border-radius:50%;display:grid;place-items:center;background:#394132;color:#d5e6c9;font-weight:700}
    @keyframes rise{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}}@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
    @media(max-width:720px){.block-container{padding:.7rem .7rem 8rem}.hero{margin:5vh auto 1rem}.hero-mark{width:52px;height:52px}.topline{margin-bottom:.55rem}[data-testid="stChatInput"]{border-radius:17px!important}}
    @media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}
    </style>
    """,
    unsafe_allow_html=True,
)

MODEL_CATALOG = {
    "Automático": ("", "A Eternity escolhe uma opção disponível conforme sua tarefa.", "Recomendado"),
    "Eternity Equilíbrio": ("qwen/qwen3.8-27b", "Versátil para conversas, escrita, análise e tarefas multimodais.", "Versátil"),
    "Eternity Núcleo": ("openai/gpt-oss-120b", "Maior capacidade para análises e problemas complexos.", "Aprofundado"),
    "Eternity Ágil": ("openai/gpt-oss-20b", "Respostas rápidas para tarefas do dia a dia.", "Rápido"),
    "Eternity Clássica": ("llama-3.3-70b-versatile", "Boa opção para conversas longas e criação de texto.", "Criativo"),
    "Eternity Relâmpago": ("llama-3.1-8b-instant", "Prioriza velocidade em perguntas simples.", "Instantâneo"),
}
MODES = {
    "Conversa": "Responda de modo natural, claro e útil.",
    "Código": "Ajude com programação: explique a causa, proponha uma solução segura e mostre código legível quando útil. Não diga que executou código se não executou.",
    "Escrita": "Atue como parceiro de escrita. Preserve a intenção do usuário, melhore clareza e tom e ofereça alternativas quando fizer sentido.",
    "Estudo": "Ensine com paciência, exemplos concretos e etapas verificáveis. Faça perguntas de checagem apenas quando ajudarem o aprendizado.",
}
MODEL_ORDER = ["qwen/qwen3.8-27b", "openai/gpt-oss-120b", "openai/gpt-oss-20b", "llama-3.3-70b-versatile", "llama-3.1-8b-instant"]


def new_conversation():
    return {"id": uuid.uuid4().hex[:12], "title": "Nova conversa", "messages": [], "created": datetime.now().strftime("%d/%m · %H:%M")}


def setup_state():
    st.session_state.setdefault("et_chats", [new_conversation()])
    st.session_state.setdefault("et_active_chat", st.session_state.et_chats[0]["id"])
    st.session_state.setdefault("et_mode", "Conversa")
    st.session_state.setdefault("et_model", "Automático")
    st.session_state.setdefault("et_effort", "Automático")


def current_chat():
    return next((chat for chat in st.session_state.et_chats if chat["id"] == st.session_state.et_active_chat), st.session_state.et_chats[0])


def get_secret(name):
    value = os.environ.get(name)
    if value:
        return value
    try:
        return st.secrets.get(name)
    except Exception:
        return None


def pick_model_ids(preferred, has_image=False):
    # This lightweight entry point uses text chat; automatic mode follows the existing Eternity preference order.
    preferred_id = MODEL_CATALOG.get(preferred, ("", "", ""))[0]
    result = ([preferred_id] if preferred_id else []) + [model for model in MODEL_ORDER if model != preferred_id]
    return result


def api_stream(client, chat, model_ids, mode, effort, status):
    system = (
        "Você é Eternity, uma assistente original, acolhedora, precisa e direta. "
        "Não revele nem simule uma transcrição de raciocínio interno privado. Para tarefas difíceis, "
        "apresente uma explicação breve e verificável: premissas relevantes, método em alto nível, "
        "resultado e limitações. Separe fatos de incertezas. Use Markdown somente quando ajudar. " + MODES[mode]
    )
    messages = [{"role": "system", "content": system}]
    messages.extend({"role": item["role"], "content": item["content"]} for item in chat["messages"][-24:])
    last_error = None
    for model_id in model_ids:
        params = {}
        if model_id.startswith("openai/gpt-oss"):
            params["reasoning_effort"] = "high" if effort == "Aprofundado" else "low"
        elif model_id == "qwen/qwen3.8-27b":
            params.update(reasoning_effort="high" if effort == "Aprofundado" else "none", reasoning_format="hidden")
        try:
            status.update(label="Preparando uma resposta clara…", state="running")
            stream = client.chat.completions.create(
                model=model_id, messages=messages, stream=True, temperature=.6, max_tokens=8192, **params,
            )
            for chunk in stream:
                if chunk.choices:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        yield delta
            return
        except APIError as exc:
            last_error = exc
            continue
    if last_error:
        raise last_error


def show_message(item):
    role = item["role"]
    with st.chat_message(role, avatar="✦" if role == "assistant" else "●"):
        st.markdown(item["content"])
        if role == "assistant":
            with st.expander("Resumo da abordagem", expanded=False):
                st.markdown('<div class="approach"><b>Explicação resumida:</b> a Eternity apresenta a conclusão e, quando relevante, as premissas e verificações úteis — não uma transcrição de pensamento privado.</div>', unsafe_allow_html=True)


setup_state()
chat = current_chat()
api_key = get_secret("GROQ_API_KEY")

with st.sidebar:
    st.markdown('<div class="brand"><div class="brand-mark">✦</div><div><div class="brand-name">Eternity</div><div class="brand-sub">UM ESPAÇO PARA PENSAR E CRIAR</div></div></div>', unsafe_allow_html=True)
    if st.button("＋  Nova conversa", key="et_new_chat", use_container_width=True):
        fresh = new_conversation()
        st.session_state.et_chats.append(fresh)
        st.session_state.et_active_chat = fresh["id"]
        st.rerun()
    st.text_input("Buscar conversas", key="et_chat_filter", placeholder="⌕  Procurar no histórico")
    st.markdown('<div class="side-heading">Modelos da Eternity</div>', unsafe_allow_html=True)
    with st.expander(f"✦  {st.session_state.et_model}  ·  Alterar", expanded=False):
        for model_name, (_, description, badge) in MODEL_CATALOG.items():
            active = model_name == st.session_state.et_model
            st.markdown(
                f'<div class="model-card{" active" if active else ""}"><div class="model-title">{html.escape(model_name)}</div>'
                f'<div class="model-desc">{html.escape(description)}</div><div class="model-tag">{html.escape(badge)}</div></div>',
                unsafe_allow_html=True,
            )
            if not active and st.button(f"Usar {model_name}", key=f"use_model_{model_name}", use_container_width=True):
                st.session_state.et_model = model_name
                st.rerun()
    st.markdown('<div class="side-heading">Modo de conversa</div>', unsafe_allow_html=True)
    st.selectbox("Modo", list(MODES), key="et_mode", label_visibility="collapsed")
    st.markdown('<div class="side-heading">Recentes</div>', unsafe_allow_html=True)
    filter_text = st.session_state.et_chat_filter.strip().casefold()
    visible_chats = list(reversed(st.session_state.et_chats[-30:]))
    for item in visible_chats:
        searchable = (item["title"] + " " + " ".join(m["content"] for m in item["messages"])).casefold()
        if filter_text and filter_text not in searchable:
            continue
        active = item["id"] == st.session_state.et_active_chat
        label = ("●  " if active else "   ") + (item["title"][:29] or "Nova conversa")
        if st.button(label, key=f"open_chat_{item['id']}", help=item["created"], use_container_width=True):
            st.session_state.et_active_chat = item["id"]
            st.rerun()
    st.markdown('<div class="side-heading">Conta</div><div class="account-row"><span class="account-dot">E</span><span>Eternity · sessão atual</span></div>', unsafe_allow_html=True)
    st.caption("Esta experiência guarda conversas apenas na sessão atual do navegador.")

if not api_key:
    st.markdown('<div class="hero"><div class="hero-mark">✦</div><div class="eyebrow">Seu espaço de criação</div><h1>Eternity</h1><p>Configure <b>GROQ_API_KEY</b> em Streamlit → Settings → Secrets para iniciar uma conversa.</p></div>', unsafe_allow_html=True)
    st.stop()
client = Groq(api_key=api_key, timeout=180, max_retries=1)

if not chat["messages"]:
    st.markdown('<div class="hero"><div class="hero-mark">✦</div><div class="eyebrow">Conversa, criação e descoberta</div><h1>Por onde começamos?</h1><p>Uma conversa clara, organizada e no seu ritmo. Escolha um modelo ou deixe a Eternity decidir.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="starter-title">Comece com uma ideia</div>', unsafe_allow_html=True)
    starters = [
        ("✎  Escrever ou editar", "Ajude-me a melhorar um texto para que fique mais claro, natural e convincente."),
        ("⌘  Programar", "Quero ajuda com código. Analise meu problema e proponha uma solução legível."),
        ("◉  Aprender", "Explique um conceito difícil de forma simples, com analogia e exemplo prático."),
        ("✧  Planejar", "Ajude-me a transformar uma ideia em um plano simples, com etapas e prioridades."),
    ]
    starter_columns = st.columns(2, gap="small")
    for i, (label, text) in enumerate(starters):
        with starter_columns[i % 2]:
            if st.button(label, key=f"start_{i}", use_container_width=True):
                st.session_state.et_pending_prompt = text
                st.rerun()
else:
    st.markdown(f'<div class="topline"><div class="topline-title">{html.escape(chat["title"])}</div><div class="topline-meta">{html.escape(st.session_state.et_mode)} · {html.escape(st.session_state.et_model)}</div></div>', unsafe_allow_html=True)
    for item in chat["messages"]:
        show_message(item)

# The controls are grouped above the composer on the welcome screen and remain one click away in chat.
with st.container(key="et_composer_controls"):
    controls = st.columns([.38, .25, .37], vertical_alignment="center")
    with controls[0]:
        st.selectbox("Modelo", list(MODEL_CATALOG), key="et_model", label_visibility="collapsed")
    with controls[1]:
        st.selectbox("Esforço", ["Automático", "Rápido", "Aprofundado"], key="et_effort", label_visibility="collapsed", help="Ajusta o esforço do modelo quando suportado; não exibe raciocínio interno.")
    with controls[2]:
        st.caption(f"Modo: {st.session_state.et_mode} · as respostas podem conter erros")

prompt = st.chat_input("Pergunte, escreva ou cole algo para trabalhar…")
pending = st.session_state.pop("et_pending_prompt", None)
user_text = (prompt or pending or "").strip()

if user_text:
    chat["messages"].append({"role": "user", "content": user_text})
    if chat["title"] == "Nova conversa":
        chat["title"] = re.sub(r"\s+", " ", user_text)[:42] or "Nova conversa"
    with st.chat_message("user", avatar="●"):
        st.markdown(user_text)
    with st.chat_message("assistant", avatar="✦"):
        with st.status("Eternity está preparando sua resposta…", expanded=False) as status:
            st.write("Entendendo o pedido")
            st.write("Organizando uma resposta útil")
            try:
                model_ids = pick_model_ids(st.session_state.et_model)
                answer = st.write_stream(api_stream(
                    client, chat, model_ids, st.session_state.et_mode,
                    st.session_state.et_effort, status,
                ))
                status.update(label="Resposta pronta", state="complete")
            except APIError as exc:
                status.update(label="Não consegui concluir desta vez", state="error")
                st.error("A API de linguagem não respondeu. Confira GROQ_API_KEY e os modelos liberados para sua conta.")
                st.caption(str(exc)[:400])
                answer = ""
    if answer:
        chat["messages"].append({"role": "assistant", "content": answer})
        st.rerun()
elif chat["messages"]:
    markdown_transcript = "\n\n".join(
        f"## {'Você' if item['role'] == 'user' else 'Eternity'}\n\n{item['content']}"
        for item in chat["messages"]
    )
    st.download_button("Baixar conversa (.md)", markdown_transcript, file_name="conversa-eternity.md", mime="text/markdown")
