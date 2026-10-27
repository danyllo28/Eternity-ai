import base64
import io
import os

import streamlit as st
from groq import APIError, BadRequestError, Groq
from PIL import Image, ImageOps

# ───────────────────────── Configuração ─────────────────────────
st.set_page_config(
    page_title="Eternity",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Ordem de preferência. Só entram os que a sua chave realmente enxerga.
# (id do modelo, parâmetros extras opcionais)
TEXT_MODELS = [
    ("openai/gpt-oss-120b", {"reasoning_effort": "low"}),
    ("qwen/qwen3.8-27b", {"reasoning_effort": "none"}),
    ("openai/gpt-oss-20b", {"reasoning_effort": "low"}),
    ("llama-3.3-70b-versatile", {}),
    ("llama-3.1-8b-instant", {}),
]
VISION_MODELS = [
    ("qwen/qwen3.8-27b", {"reasoning_effort": "none"}),
    ("meta-llama/llama-4-scout-17b-16e-instruct", {}),
    ("meta-llama/llama-4-maverick-17b-128e-instruct", {}),
]

MAX_IMAGES = 3          # limite do modelo de visão
MAX_HISTORY = 20        # mensagens enviadas como contexto

SYSTEM_PROMPT = (
    "Você é Eternity, uma IA pessoal e familiar: acolhedora, inteligente e direta. "
    "Responda sempre no idioma do usuário (por padrão, português do Brasil), "
    "com clareza e sem enrolação. Quando receber imagens, descreva e analise com cuidado."
)

# ───────────────────────── Estilo (Dark Mode) ─────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"], .stApp, textarea, button {
    font-family: 'Inter', -apple-system, 'Segoe UI', Roboto, sans-serif !important;
}
.stApp { background: #171717; color: #ECECEC; }

/* Remove o peso visual do Streamlit */
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

.block-container { max-width: 768px; padding-top: 2.5rem; padding-bottom: 9rem; }

/* Mensagens */
[data-testid="stChatMessage"] { background: transparent; padding: 0.35rem 0; gap: 0; }
[data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"],
[data-testid="chatAvatarIcon-user"], [data-testid="chatAvatarIcon-assistant"] { display: none !important; }
[data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li { font-size: 1rem; line-height: 1.7; color: #ECECEC; }

/* Bolha do usuário, alinhada à direita */
[data-testid="stChatMessage"]:has(.u-msg) { justify-content: flex-end; }
[data-testid="stChatMessage"]:has(.u-msg) [data-testid="stChatMessageContent"] {
    background: #2F2F2F; border-radius: 22px; padding: 0.55rem 1.1rem;
    max-width: 80%; width: fit-content; flex: 0 1 auto;
}
[data-testid="stChatMessage"]:has(.u-msg) p { margin: 0; }
[data-testid="stChatMessage"] img { border-radius: 14px; }

/* Barra de digitação flutuante */
[data-testid="stBottom"], [data-testid="stBottom"] > div, [data-testid="stBottomBlockContainer"] {
    background: transparent !important;
}
[data-testid="stBottom"] { background: linear-gradient(to top, #171717 65%, rgba(23,23,23,0)) !important; }
[data-testid="stChatInput"] {
    background: #2F2F2F; border: 1px solid #3B3B3B; border-radius: 28px;
    box-shadow: 0 4px 24px rgba(0,0,0,.35);
}
[data-testid="stChatInput"] > div { background: transparent !important; border: none !important; }
[data-testid="stChatInput"]:focus-within { border-color: #565656; }
[data-testid="stChatInput"] textarea { background: transparent !important; color: #ECECEC !important; caret-color: #ECECEC; }
[data-testid="stChatInput"] textarea::placeholder { color: #8E8E8E; }
[data-testid="stChatInput"] button { background: transparent; color: #B4B4B4; border: none; border-radius: 50%; }
[data-testid="stChatInputSubmitButton"]:not(:disabled) { background: #ECECEC !important; color: #171717 !important; }

/* Sidebar discreta */
[data-testid="stSidebar"] { background: #1E1E1E; border-right: 1px solid #2A2A2A; }
[data-testid="stSidebar"] .stButton > button {
    width: 100%; background: transparent; color: #ECECEC;
    border: 1px solid #3B3B3B; border-radius: 12px;
}
[data-testid="stSidebar"] .stButton > button:hover { background: #2A2A2A; border-color: #4A4A4A; }

/* Tela inicial */
.hero { text-align: center; margin-top: 26vh; }
.hero h1 { font-size: 2.1rem; font-weight: 500; letter-spacing: -0.02em; margin: 0; color: #ECECEC; }
.hero p { color: #8E8E8E; margin-top: .6rem; font-size: 1rem; }
</style>
""",
    unsafe_allow_html=True,
)

# ───────────────────────── Chave e cliente ─────────────────────────
def get_api_key():
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key
    try:
        return st.secrets.get("GROQ_API_KEY")
    except Exception:
        return None


API_KEY = get_api_key()
if not API_KEY:
    st.markdown(
        '<div class="hero"><h1>Eternity</h1>'
        "<p>Configure GROQ_API_KEY em Settings → Secrets para começar.</p></div>",
        unsafe_allow_html=True,
    )
    st.stop()

client = Groq(api_key=API_KEY)


@st.cache_data(ttl=600, show_spinner=False)
def list_available_models(api_key: str):
    """Modelos que ESTA chave realmente pode usar."""
    try:
        return [m.id for m in Groq(api_key=api_key).models.list().data]
    except Exception:
        return []


# ───────────────────────── Funções auxiliares ─────────────────────────
def prepare_image(file) -> bytes:
    """Redimensiona e converte para JPEG (payload leve e compatível)."""
    img = Image.open(file)
    img = ImageOps.exif_transpose(img).convert("RGB")
    img.thumbnail((1568, 1568))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=88)
    return buf.getvalue()


def build_api_messages(history):
    msgs = [{"role": "system", "content": SYSTEM_PROMPT}]
    recent = history[-MAX_HISTORY:]
    last = len(recent) - 1
    for i, m in enumerate(recent):
        images = m.get("images") or []
        if m["role"] == "user" and images and i == last:
            content = [{"type": "text", "text": m["content"] or "Descreva esta imagem."}]
            for raw in images:
                b64 = base64.b64encode(raw).decode()
                content.append(
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                )
            msgs.append({"role": "user", "content": content})
        else:
            text = m["content"] or ""
            if images:  # imagens antigas não são reenviadas (economiza tokens)
                text += "\n[imagem anexada anteriormente]"
            msgs.append({"role": m["role"], "content": text})
    return msgs


def pick_candidates(has_images: bool):
    pool = VISION_MODELS if has_images else TEXT_MODELS
    available = list_available_models(API_KEY)
    if available:
        filtered = [c for c in pool if c[0] in available]
        if filtered:
            return filtered
    return pool


def stream_reply(messages, candidates, state):
    """Gera a resposta em streaming, com fallback automático entre modelos."""
    for model, extras in candidates:
        for params in ([extras, {}] if extras else [{}]):
            started = False
            try:
                stream = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=True,
                    temperature=0.7,
                    max_tokens=4096,
                    **params,
                )
                for chunk in stream:
                    if not chunk.choices:
                        continue
                    delta = chunk.choices[0].delta.content
                    if delta:
                        started = True
                        state["ok"] = True
                        state["model"] = model
                        yield delta
                if started:
                    return
            except BadRequestError as e:      # parâmetro extra recusado → tenta sem ele
                state["error"] = f"{model}: {e}"
                if started:
                    return
                continue
            except APIError as e:             # 404 / sem acesso / limite → próximo modelo
                state["error"] = f"{model}: {e}"
                if started:
                    return
                break


def render_message(m):
    with st.chat_message(m["role"]):
        if m["role"] == "user":
            st.markdown('<span class="u-msg"></span>', unsafe_allow_html=True)
        for img in m.get("images", []):
            st.image(img, width=220)
        if m["content"]:
            st.markdown(m["content"])


# ───────────────────────── Estado e sidebar ─────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    if st.button("＋  Nova conversa"):
        st.session_state.history = []
        st.rerun()
    if st.session_state.get("model_used"):
        st.caption(f"Modelo em uso: `{st.session_state.model_used}`")

# ───────────────────────── Conversa ─────────────────────────
if not st.session_state.history:
    st.markdown(
        '<div class="hero"><h1>✦ Eternity</h1><p>Como posso ajudar você hoje?</p></div>',
        unsafe_allow_html=True,
    )

for m in st.session_state.history:
    render_message(m)

prompt = st.chat_input(
    "Pergunte qualquer coisa à Eternity…",
    accept_file="multiple",
    file_type=["png", "jpg", "jpeg", "webp"],
)

if prompt:
    text = (prompt.text or "").strip()
    files = list(prompt.files or [])
    if len(files) > MAX_IMAGES:
        st.toast(f"Usando apenas as primeiras {MAX_IMAGES} imagens.", icon="⚠️")
        files = files[:MAX_IMAGES]

    images = []
    for f in files:
        try:
            images.append(prepare_image(f))
        except Exception:
            st.toast(f"Não consegui abrir {getattr(f, 'name', 'a imagem')}.", icon="⚠️")

    if text or images:
        user_msg = {"role": "user", "content": text, "images": images}
        st.session_state.history.append(user_msg)
        render_message(user_msg)

        state = {"ok": False, "error": None, "model": None}
        with st.chat_message("assistant"):
            reply = st.write_stream(
                stream_reply(
                    build_api_messages(st.session_state.history),
                    pick_candidates(bool(images)),
                    state,
                )
            )

        if state["ok"] and reply:
            st.session_state.model_used = state["model"]
            st.session_state.history.append({"role": "assistant", "content": reply, "images": []})
        else:
            st.session_state.history.pop()  # remove a pergunta sem resposta
            st.error(
                "Não consegui obter resposta de nenhum modelo da Groq. "
                "Verifique sua chave em console.groq.com e os modelos liberados para ela."
            )
            if state["error"]:
                with st.expander("Detalhes técnicos"):
                    st.code(state["error"])
