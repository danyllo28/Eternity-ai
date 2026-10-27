import base64
import hmac
import html
import io
import json
import os
import random
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

import streamlit as st
from groq import APIError, BadRequestError, Groq
from PIL import Image, ImageOps

st.set_page_config(
    page_title="Eternity",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ───────────────────────── Modelos ─────────────────────────
_OSS = {"fast": {"reasoning_effort": "low"}, "deep": {"reasoning_effort": "high"},
        "max_fast": 4096, "max_deep": 16384}
_LLAMA = {"fast": {}, "deep": {}, "max_fast": 4096, "max_deep": 8192}
MODELS = {
    "openai/gpt-oss-120b": _OSS,
    "openai/gpt-oss-20b": _OSS,
    "qwen/qwen3.8-27b": {
        "fast": {"reasoning_effort": "none", "reasoning_format": "hidden"},
        "deep": {"reasoning_effort": "high", "reasoning_format": "hidden"},
        "max_fast": 4096, "max_deep": 16000,
    },
    "llama-3.3-70b-versatile": _LLAMA,
    "llama-3.1-8b-instant": _LLAMA,
    "meta-llama/llama-4-scout-17b-16e-instruct": _LLAMA,
    "meta-llama/llama-4-maverick-17b-128e-instruct": _LLAMA,
}
TEXT_ORDER = ["openai/gpt-oss-120b", "qwen/qwen3.8-27b", "openai/gpt-oss-20b",
              "llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
VISION_ORDER = ["qwen/qwen3.8-27b", "meta-llama/llama-4-scout-17b-16e-instruct",
                "meta-llama/llama-4-maverick-17b-128e-instruct"]

MAX_IMAGES = 3
MAX_HISTORY = 20
REFLECT_EVERY = 3
MEM_FILE = "eternity_memory.json"
MODE_LABELS = {"⚡ Rápido": "fast", "🧠 Profundo": "deep", "🎨 Imagem": "img"}
LANGUAGES = {
    "Português (Brasil)": "português brasileiro",
    "English": "English",
    "Español": "español",
    "Français": "français",
    "Deutsch": "Deutsch",
    "Italiano": "italiano",
    "日本語": "japonês",
    "한국어": "coreano",
    "中文": "chinês simplificado",
    "العربية": "árabe",
    "हिन्दी": "hindi",
    "Русский": "russo",
}
CREATOR_TRIGGER = re.compile(
    r"\b(quem\s+(criou|fez|desenvolveu|inventou)\s+(a\s+)?(eternity|você|voce|ela)"
    r"|quem\s+(te|lhe)\s+(criou|fez|desenvolveu)|quem\s+(desenvolveu|programou|construiu)\s+(a\s+)?(eternity|você|voce|ela)"
    r"|quem\s+é\s+(o\s+)?(seu\s+)?criador"
    r"|who\s+(created|made|built)\s+(you|eternity)"
    r"|who\s+is\s+your\s+creator"
    r"|qui\s+a\s+créé\s+(eternity|toi)"
    r"|quién\s+(creó|hizo)\s+(a\s+)?(eternity|tú))", re.I
)
CREATOR_ANSWERS = {
    "Português (Brasil)": "Fui totalmente desenvolvida por Danyllo, meu criador. ✦",
    "English": "I was entirely developed by Danyllo, my creator. ✦",
    "Español": "Fui desarrollada íntegramente por Danyllo, mi creador. ✦",
    "Français": "J’ai été entièrement développée par Danyllo, mon créateur. ✦",
    "Deutsch": "Ich wurde vollständig von Danyllo, meinem Schöpfer, entwickelt. ✦",
    "Italiano": "Sono stata interamente sviluppata da Danyllo, il mio creatore. ✦",
    "日本語": "私は創造主であるDanylloによって全面的に開発されました。✦",
    "한국어": "저는 제 창조자인 Danyllo가 전적으로 개발했습니다. ✦",
    "中文": "我由我的创造者 Danyllo 完全开发。✦",
    "العربية": "تم تطويري بالكامل بواسطة Danyllo، منشئي. ✦",
    "हिन्दी": "मुझे मेरे निर्माता Danyllo ने पूरी तरह विकसित किया है। ✦",
    "Русский": "Я была полностью разработана Danyllo, моим создателем. ✦",
}

BASE_PROMPT = (
    "Você é Eternity, uma IA pessoal e familiar: acolhedora, inteligente e direta. "
    "A Eternity foi totalmente desenvolvida por Danyllo. Quando perguntarem quem criou, desenvolveu ou fez a Eternity, responda com clareza que ela foi totalmente desenvolvida por Danyllo, seu criador. Não atribua a criação a outra pessoa. "
    "Responda no idioma selecionado nas configurações, com clareza e sem enrolação. "
    "Ao receber imagens, descreva e analise com cuidado. "
    "Você consegue criar imagens: se o usuário pedir uma, diga que pode e que basta usar o modo "
    "🎨 Imagem (ou começar a mensagem com /imagem). "
    "Use a memória abaixo de forma natural, sem dizer que consultou uma lista, e nunca invente "
    "fatos sobre a família."
)
DEEP_PROMPT = (
    "MODO PENSAMENTO PROFUNDO: analise o problema com muito cuidado, considere alternativas, "
    "verifique cálculos e conclusões e só então entregue uma resposta completa e bem estruturada."
)
REFLECT_PROMPT = (
    "Você é o módulo de auto-aperfeiçoamento da Eternity, uma IA familiar. Receberá a memória atual "
    "e a conversa recente. Devolva SOMENTE um JSON no formato "
    '{"facts": [...], "lessons": [...]}.\n'
    "- facts: fatos duráveis sobre o usuário e a família (nomes, gostos, rotinas, projetos). "
    "Nunca guarde senhas, documentos, cartões ou dados bancários.\n"
    "- lessons: instruções curtas sobre COMO responder melhor (tom, formato, correções recebidas, "
    "erros a evitar).\n"
    "Mantenha o que continua válido, remova duplicados e contradições, no máximo 40 facts e "
    "20 lessons, cada item com até 160 caracteres."
)

# ───────────────────────── Estilo ─────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
html, body, [class*="css"], .stApp, textarea, button {
    font-family: 'Inter', -apple-system, 'Segoe UI', Roboto, sans-serif !important;
}
.stApp { background: #171717; color: #ECECEC; }
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 860px; padding: 1.5rem 1.1rem 8rem 1.1rem; }

/* Mensagem do usuário: SEMPRE à direita */
.user-row { display: flex; justify-content: flex-end; width: 100%; margin: 0.9rem 0 0.4rem 0; }
.user-bubble {
    background: #2F2F2F; color: #ECECEC; border-radius: 22px; padding: 0.6rem 1.1rem;
    max-width: 85%; text-align: left; line-height: 1.6; font-size: 1rem;
    overflow-wrap: anywhere; word-break: break-word;
}
.user-bubble img { display: block; max-width: 200px; width: 100%; border-radius: 12px; margin: 0 0 8px 0; }
.note { color: #8E8E8E; font-size: .85rem; margin-bottom: 4px; }
@media (max-width: 640px) {
  .block-container { padding: 1rem .65rem 7rem .65rem; }
  .user-bubble { max-width: 92%; padding: .65rem .9rem; font-size: .96rem; }
  .hero { margin-top: 12vh; }
  .hero h1 { font-size: 1.8rem; }
  [data-testid="stChatInput"] { border-radius: 22px; }
  [data-testid="stSidebar"] { min-width: 82vw; }
}

/* Resposta da Eternity: à esquerda, sem bolha */
.stMarkdown p, .stMarkdown li { line-height: 1.7; font-size: 1rem; }
[data-testid="stImage"] img { border-radius: 14px; }
.thinking { color: #8E8E8E; animation: pulse 1.5s ease-in-out infinite; padding: .3rem 0; }
@keyframes pulse { 0%,100% { opacity: .35 } 50% { opacity: 1 } }

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
[data-testid="stChatInput"] textarea { background: transparent !important; color: #ECECEC !important; }
[data-testid="stChatInput"] textarea::placeholder { color: #8E8E8E; }
[data-testid="stChatInput"] button { background: transparent; color: #B4B4B4; border: none; border-radius: 50%; }
[data-testid="stChatInputSubmitButton"]:not(:disabled) { background: #ECECEC !important; color: #171717 !important; }

/* Seletor de modo centralizado */
[data-testid="stElementContainer"]:has([data-testid="stButtonGroup"]) { display: flex; justify-content: center; }

/* Sidebar */
[data-testid="stSidebar"] { background: #1E1E1E; border-right: 1px solid #2A2A2A; }
[data-testid="stSidebar"] .stButton > button {
    width: 100%; background: transparent; color: #ECECEC; border: 1px solid #3B3B3B; border-radius: 12px;
}
[data-testid="stSidebar"] .stButton > button:hover { background: #2A2A2A; border-color: #4A4A4A; }

.hero { text-align: center; margin-top: 20vh; }
.hero h1 { font-size: 2.1rem; font-weight: 500; letter-spacing: -0.02em; margin: 0; color: #ECECEC; }
.hero p { color: #8E8E8E; margin-top: .6rem; }
</style>
""",
    unsafe_allow_html=True,
)

# ───────────────────────── Segredos e acesso ─────────────────────────
def secret(name, default=None):
    v = os.environ.get(name)
    if v:
        return v
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


def hero(text):
    st.markdown(f'<div class="hero"><h1>✦ Eternity</h1><p>{text}</p></div>', unsafe_allow_html=True)


API_KEY = secret("GROQ_API_KEY")
if not API_KEY:
    hero("Configure GROQ_API_KEY em Settings → Secrets para começar.")
    st.stop()

client = Groq(api_key=API_KEY, timeout=300, max_retries=2)


@st.cache_data(ttl=600, show_spinner=False)
def list_available_models(api_key: str):
    try:
        return [m.id for m in Groq(api_key=api_key).models.list().data]
    except Exception:
        return []


# ───────────────────────── Contas e memória individual ─────────────────────────
MEM_FILE = "eternity_memory.json"
ACCOUNTS_FILE = "eternity_accounts.json"
LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_PATH = os.path.join(LOCAL_DIR, MEM_FILE)
ACCOUNTS_PATH = os.path.join(LOCAL_DIR, ACCOUNTS_FILE)


def default_memory():
    return {"messages": [], "facts": [], "lessons": [], "turns": 0}


def gh_call(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {secret('GITHUB_TOKEN')}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "eternity-app",
        "Content-Type": "application/json",
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        body = r.read().decode()
        return json.loads(body) if body else {}


def use_gist():
    return bool(secret("GITHUB_TOKEN") and secret("GIST_ID"))


def gist_read(filename):
    gist = gh_call("GET", f"https://api.github.com/gists/{secret('GIST_ID')}")
    f = gist.get("files", {}).get(filename)
    if not f:
        return None
    if f.get("truncated") and f.get("raw_url"):
        with urllib.request.urlopen(f["raw_url"], timeout=20) as r:
            return r.read().decode()
    return f.get("content")


def gist_write(filename, content):
    gh_call("PATCH", f"https://api.github.com/gists/{secret('GIST_ID')}",
            {"files": {filename: {"content": content}}})


def read_json_file(filename, local_path, default):
    try:
        if use_gist():
            raw = gist_read(filename)
        else:
            raw = open(local_path, encoding="utf-8").read() if os.path.exists(local_path) else None
        return json.loads(raw) if raw else default
    except Exception:
        return default


def write_json_file(filename, local_path, data):
    content = json.dumps(data, ensure_ascii=False, indent=2)
    try:
        if use_gist():
            gist_write(filename, content)
        else:
            with open(local_path, "w", encoding="utf-8") as fh:
                fh.write(content)
        return True
    except Exception:
        return False


def load_accounts():
    data = read_json_file(ACCOUNTS_FILE, ACCOUNTS_PATH, {"users": {}})
    if not isinstance(data, dict) or not isinstance(data.get("users"), dict):
        return {"users": {}}
    return data


def save_accounts(accounts):
    return write_json_file(ACCOUNTS_FILE, ACCOUNTS_PATH, accounts)


def username_key(username):
    import hashlib
    return hashlib.sha256(username.casefold().encode("utf-8")).hexdigest()[:20]


def memory_filename(user_key):
    return f"eternity_memory_{user_key}.json"


def memory_local_path(user_key):
    return os.path.join(LOCAL_DIR, memory_filename(user_key))


def password_digest(password, salt_hex):
    import hashlib
    salt = bytes.fromhex(salt_hex)
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 310000).hex()


def register_user(username, password):
    import secrets as _secrets
    accounts = load_accounts()
    display = username.strip()
    login = display.casefold()
    if len(display) < 3 or len(display) > 24 or not re.fullmatch(r"[A-Za-z0-9_-]+", display):
        return False, "Use um nome de usuário de 3 a 24 caracteres: letras, números, _ ou -."
    if len(password) < 8:
        return False, "A senha precisa ter pelo menos 8 caracteres."
    if login in accounts["users"]:
        return False, "Esse nome de usuário já existe. Escolha outro."
    salt = _secrets.token_hex(16)
    accounts["users"][login] = {
        "username": display,
        "user_key": username_key(login),
        "salt": salt,
        "password_hash": password_digest(password, salt),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    if not save_accounts(accounts):
        return False, "Não consegui salvar a conta. Confira GITHUB_TOKEN e GIST_ID em Secrets."
    # Migra a memória antiga para a primeira conta criada, sem compartilhá-la com contas futuras.
    if len(accounts["users"]) == 1:
        legacy = read_json_file(MEM_FILE, LOCAL_PATH, None)
        if isinstance(legacy, dict) and legacy:
            write_json_file(memory_filename(username_key(login)), memory_local_path(username_key(login)), legacy)
    return True, accounts["users"][login]


def authenticate_user(username, password):
    accounts = load_accounts()
    login = username.strip().casefold()
    record = accounts["users"].get(login)
    if not record:
        return None
    candidate = password_digest(password, record.get("salt", ""))
    if hmac.compare_digest(candidate, record.get("password_hash", "")):
        return record
    return None


def show_auth_screen():
    hero("Seu espaço pessoal, do seu jeito.")
    st.markdown("<div style='text-align:center;color:#9B9B9B;margin-bottom:1.2rem'>Entre na sua conta ou crie uma nova para ter sua própria memória.</div>", unsafe_allow_html=True)
    if not use_gist():
        st.warning("Atenção: GITHUB_TOKEN e GIST_ID não estão configurados. As contas e memórias ficarão no armazenamento local temporário e podem sumir quando o Streamlit reiniciar.")
    login_tab, create_tab = st.tabs(["Entrar", "Criar minha conta"])
    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Nome de usuário", max_chars=24, placeholder="Seu usuário")
            password = st.text_input("Sua senha", type="password", placeholder="Sua senha")
            submitted = st.form_submit_button("Entrar", use_container_width=True)
        if submitted:
            record = authenticate_user(username, password)
            if record:
                st.session_state.current_user = record
                st.rerun()
            st.error("Usuário ou senha incorretos.")
    with create_tab:
        with st.form("register_form"):
            new_username = st.text_input("Escolha um nome de usuário", max_chars=24, placeholder="Ex.: maria_01")
            new_password = st.text_input("Crie sua senha", type="password", placeholder="Mínimo de 8 caracteres")
            confirm_password = st.text_input("Confirme sua senha", type="password")
            created = st.form_submit_button("Criar conta", use_container_width=True)
        if created:
            if new_password != confirm_password:
                st.error("As senhas não coincidem.")
            else:
                ok, result = register_user(new_username, new_password)
                if ok:
                    st.session_state.current_user = result
                    st.rerun()
                st.error(result)
    st.caption("As senhas são armazenadas como hashes, não em texto puro. Não há recuperação de senha automática nesta versão.")


API_KEY = secret("GROQ_API_KEY")
if not API_KEY:
    hero("Configure GROQ_API_KEY em Settings → Secrets para começar.")
    st.stop()

client = Groq(api_key=API_KEY, timeout=300, max_retries=2)

if "current_user" not in st.session_state:
    st.session_state.current_user = None
if not st.session_state.current_user:
    show_auth_screen()
    st.stop()

CURRENT_USER = st.session_state.current_user
CURRENT_USER_KEY = CURRENT_USER["user_key"]


def load_memory():
    mem = default_memory()
    filename = memory_filename(CURRENT_USER_KEY)
    local_path = memory_local_path(CURRENT_USER_KEY)
    data = read_json_file(filename, local_path, {})
    if isinstance(data, dict):
        mem["messages"] = [m for m in data.get("messages", [])
                           if isinstance(m, dict) and m.get("role") in ("user", "assistant")]
        mem["facts"] = [str(x) for x in data.get("facts", []) if isinstance(x, str)]
        mem["lessons"] = [str(x) for x in data.get("lessons", []) if isinstance(x, str)]
        mem["turns"] = int(data.get("turns", 0) or 0)
    return mem, ("gist" if use_gist() else "local")


def serializable(mem):
    msgs = []
    for m in mem["messages"][-60:]:
        note = m.get("note")
        if m.get("thumbs"):
            note = "📷 imagem enviada"
        if m.get("gen"):
            note = "🖼️ imagem gerada"
        item = {"role": m["role"], "content": str(m.get("content", ""))[:6000]}
        if note:
            item["note"] = note
        msgs.append(item)
    out = {"messages": msgs, "facts": mem["facts"], "lessons": mem["lessons"], "turns": mem["turns"]}
    while len(json.dumps(out, ensure_ascii=False)) > 600_000 and out["messages"]:
        out["messages"].pop(0)
    return out


def save_memory(mem):
    return write_json_file(memory_filename(CURRENT_USER_KEY), memory_local_path(CURRENT_USER_KEY), serializable(mem))


if "loaded_user_key" not in st.session_state or st.session_state.loaded_user_key != CURRENT_USER_KEY:
    st.session_state.mem, st.session_state.store_kind = load_memory()
    st.session_state.loaded_user_key = CURRENT_USER_KEY
if "pend_n" not in st.session_state:
    st.session_state.pend_n = 0
mem = st.session_state.mem

# ───────────────────────── Utilidades de IA ─────────────────────────
def clean(raw):
    t = re.sub(r"<think>.*?</think>", "", raw, flags=re.S)
    if "<think>" in t:
        t = t.split("<think>")[0]
    return t.strip()


def parse_json(text):
    if not text:
        return None
    s, e = text.find("{"), text.rfind("}")
    if s < 0 or e <= s:
        return None
    try:
        return json.loads(text[s:e + 1])
    except Exception:
        return None


def attempts(model, mode):
    full = MODELS[model][mode]
    variants = [full]
    if "reasoning_format" in full:
        variants.append({k: v for k, v in full.items() if k != "reasoning_format"})
    if full:
        variants.append({})
    out = []
    for v in variants:
        if v not in out:
            out.append(v)
    return out


def pick_models(has_images):
    order = VISION_ORDER if has_images else TEXT_ORDER
    avail = list_available_models(API_KEY)
    if avail:
        filtered = [m for m in order if m in avail]
        if filtered:
            return filtered
    return order


def stream_reply(messages, models, mode, state):
    for model in models:
        cfg = MODELS[model]
        for params in attempts(model, mode):
            started = False
            try:
                stream = client.chat.completions.create(
                    model=model, messages=messages, stream=True,
                    temperature=0.9 if mode == "deep" else 0.7,
                    max_tokens=cfg["max_" + mode], **params,
                )
                for chunk in stream:
                    if not chunk.choices:
                        continue
                    delta = chunk.choices[0].delta.content
                    if delta:
                        started = True
                        state["ok"], state["model"] = True, model
                        yield delta
                if started:
                    return
            except BadRequestError as e:
                state["error"] = f"{model}: {e}"
                if started:
                    return
                continue
            except APIError as e:
                state["error"] = f"{model}: {e}"
                if started:
                    return
                break


def chat_once(messages, models, json_mode=False, max_tokens=800):
    for model in models[:3]:
        dead = False
        for params in attempts(model, "fast"):
            if dead:
                break
            for jm in ([True, False] if json_mode else [False]):
                try:
                    kw = {"response_format": {"type": "json_object"}} if jm else {}
                    r = client.chat.completions.create(
                        model=model, messages=messages, temperature=0.3,
                        max_tokens=max_tokens, **params, **kw)
                    txt = clean(r.choices[0].message.content or "")
                    if txt:
                        return txt
                except BadRequestError:
                    continue
                except APIError:
                    dead = True
                    break
    return None


def build_system(mode):
    now = datetime.now(timezone(timedelta(hours=-3))).strftime("%d/%m/%Y %H:%M")
    lang_label = st.session_state.get("response_language", "Português (Brasil)")
    parts = [BASE_PROMPT, f"Responda sempre em {LANGUAGES.get(lang_label, 'português brasileiro')}, salvo se o usuário pedir explicitamente outro idioma.", f"Data e hora atuais (Brasília): {now}."]
    if mode == "deep":
        parts.append(DEEP_PROMPT)
    if mem["facts"]:
        parts.append("MEMÓRIA SOBRE O USUÁRIO E A FAMÍLIA:\n" + "\n".join(f"- {f}" for f in mem["facts"]))
    if mem["lessons"]:
        parts.append("APRENDIZADOS PARA RESPONDER MELHOR:\n" + "\n".join(f"- {l}" for l in mem["lessons"]))
    return "\n\n".join(parts)


def build_api_messages(system, history, current_images):
    msgs = [{"role": "system", "content": system}]
    recent = history[-MAX_HISTORY:]
    last = len(recent) - 1
    for i, m in enumerate(recent):
        text = m.get("content", "") or ""
        if m["role"] == "user" and current_images and i == last:
            content = [{"type": "text", "text": text or "Descreva esta imagem."}]
            for raw in current_images:
                b64 = base64.b64encode(raw).decode()
                content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}})
            msgs.append({"role": "user", "content": content})
        else:
            if m.get("thumbs") or m.get("note"):
                text += "\n[imagem anexada anteriormente]" if m["role"] == "user" else ""
            msgs.append({"role": m["role"], "content": text})
    return msgs


def reflect():
    """Auto-aperfeiçoamento: atualiza fatos e aprendizados a partir da conversa recente."""
    convo = "\n".join(
        f'{"Usuário" if m["role"] == "user" else "Eternity"}: {str(m.get("content", ""))[:600]}'
        for m in mem["messages"][-8:]
    )
    current = json.dumps({"facts": mem["facts"], "lessons": mem["lessons"]}, ensure_ascii=False)
    out = chat_once(
        [{"role": "system", "content": REFLECT_PROMPT},
         {"role": "user", "content": f"MEMÓRIA ATUAL:\n{current}\n\nCONVERSA RECENTE:\n{convo}"}],
        pick_models(False), json_mode=True, max_tokens=1500)
    data = parse_json(out)
    if not isinstance(data, dict):
        return False

    def norm(items, cap):
        seen, res = set(), []
        for x in items if isinstance(items, list) else []:
            if isinstance(x, str):
                x = x.strip()[:160]
                if x and x.lower() not in seen:
                    seen.add(x.lower())
                    res.append(x)
        return res[:cap]

    facts, lessons = norm(data.get("facts"), 40), norm(data.get("lessons"), 20)
    if not facts and not lessons:
        return False
    changed = facts != mem["facts"] or lessons != mem["lessons"]
    mem["facts"], mem["lessons"] = facts, lessons
    return changed


# ───────────────────────── Imagens ─────────────────────────
def prepare_image(file) -> bytes:
    img = ImageOps.exif_transpose(Image.open(file)).convert("RGB")
    img.thumbnail((1568, 1568))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=88)
    return buf.getvalue()


def make_thumb(raw: bytes) -> str:
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    img.thumbnail((360, 360))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=75)
    return base64.b64encode(buf.getvalue()).decode()


def rewrite_image_prompt(text):
    out = chat_once(
        [{"role": "system", "content": "Transforme o pedido do usuário em um prompt de geração de imagem "
                                       "em inglês, detalhado e visual (estilo, luz, composição), em 1 a 3 "
                                       "frases. Responda SOMENTE com o prompt."},
         {"role": "user", "content": text}],
        pick_models(False), max_tokens=800)
    return (out or text).strip()[:700]


def generate_image(prompt):
    last = "erro desconhecido"
    for _ in range(3):
        seed = random.randint(1, 10**6)
        url = (f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}"
               f"?width=1024&height=1024&nologo=true&seed={seed}")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Eternity)"})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            Image.open(io.BytesIO(data)).verify()
            return data, None
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code == 429:
                time.sleep(16)
                continue
        except Exception as e:
            last = str(e)
        time.sleep(3)
    return None, last


IMG_INTENT = re.compile(
    r"^\s*(?:por favor,?\s*)?(?:crie|cria|criar|gere|gera|gerar|desenhe|desenha|desenhar|fa[cç]a|faz|fazer|monte|ilustre)"
    r"\b.{0,40}\b(imagem|foto|fotografia|desenho|ilustra[cç][aã]o|logo|logotipo|arte|pintura|wallpaper)\b",
    re.I)
LEARN_TRIGGER = re.compile(
    r"\b(lembre|lembra|memoriz|anote|guarde|aprenda|prefiro|n[aã]o gosto|a partir de agora|"
    r"de agora em diante|meu nome|minha fam[ií]lia)", re.I)


def parse_command(text, mode, has_images):
    low = text.lower()
    if low.startswith("/imagem"):
        return text[7:].strip(), "img"
    if low.startswith("/profundo") or low.startswith("/pensar"):
        return text.split(" ", 1)[1].strip() if " " in text else "", "deep"
    if mode != "img" and not has_images and IMG_INTENT.search(text):
        return text, "img"
    return text, mode


# ───────────────────────── Renderização ─────────────────────────
def render(m):
    if m["role"] == "user":
        imgs = "".join(f'<img src="data:image/jpeg;base64,{b}">' for b in m.get("thumbs", []))
        note = (f'<div class="note">{html.escape(m["note"])}</div>'
                if m.get("note") and not imgs else "")
        body = html.escape(m.get("content", "")).replace("$", "&#36;").replace("\n", "<br>")
        st.markdown(f'<div class="user-row"><div class="user-bubble">{imgs}{note}{body}</div></div>',
                    unsafe_allow_html=True)
    else:
        if m.get("gen"):
            st.image(m["gen"], width=480)
        elif m.get("note"):
            st.caption(m["note"])
        st.markdown(m.get("content", ""))


def stream_to(ph, gen, label):
    raw = ""
    ph.markdown(f'<div class="thinking">{label}</div>', unsafe_allow_html=True)
    for d in gen:
        raw += d
        view = clean(raw)
        if view:
            ph.markdown(view + " ▌")
    view = clean(raw)
    ph.markdown(view)
    return view


# ───────────────────────── Sidebar ─────────────────────────
n = st.session_state.pend_n
with st.sidebar:
    st.markdown(f"**✦ Eternity**\n\nConta: `{html.escape(CURRENT_USER.get('username', 'usuário'))}`")
    if st.button("Sair da conta", use_container_width=True):
        st.session_state.current_user = None
        st.session_state.pop("mem", None)
        st.session_state.pop("loaded_user_key", None)
        st.rerun()
    st.selectbox("Idioma das respostas", list(LANGUAGES), key="response_language")
    st.divider()
    if st.button("＋  Nova conversa", use_container_width=True):
        mem["messages"] = []
        save_memory(mem)
        st.rerun()

    st.markdown("**Anexar imagens**")
    tab_g, tab_c = st.tabs(["📷 Galeria", "📸 Câmera"])
    with tab_g:
        gallery = st.file_uploader("Galeria", type=["png", "jpg", "jpeg", "webp"],
                                   accept_multiple_files=True, key=f"up_{n}",
                                   label_visibility="collapsed")
    with tab_c:
        camera = st.camera_input("Câmera", key=f"cam_{n}", label_visibility="collapsed")
    side_files = list(gallery or []) + ([camera] if camera else [])
    if side_files:
        st.caption(f"{len(side_files)} imagem(ns) pronta(s) — vão junto com a próxima mensagem.")

    with st.expander("🧠 Memória da Eternity"):
        kind = st.session_state.get("store_kind", "local")
        if kind == "gist":
            st.caption("💾 Memória permanente (Gist)")
        elif kind == "gist-erro":
            st.caption("⚠️ Não consegui ler o Gist. Verifique GITHUB_TOKEN e GIST_ID.")
        else:
            st.caption("⚠️ Memória temporária. Configure o Gist para não perder nada.")
        st.markdown("**Fatos que ela aprendeu**")
        for f in mem["facts"] or ["(nenhum ainda)"]:
            st.caption(f"• {f}")
        st.markdown("**Como ela aprendeu a responder**")
        for l in mem["lessons"] or ["(nenhum ainda)"]:
            st.caption(f"• {l}")
        if st.button("Esquecer tudo", key="forget"):
            mem.update(default_memory())
            save_memory(mem)
            st.rerun()

# ───────────────────────── Tela principal ─────────────────────────
choice = st.segmented_control("Modo", list(MODE_LABELS), default="⚡ Rápido",
                              key="mode_sel", label_visibility="collapsed")
mode = MODE_LABELS.get(choice or "⚡ Rápido", "fast")

if not mem["messages"]:
    hero("Como posso ajudar você hoje?")
for m in mem["messages"]:
    render(m)

prompt = st.chat_input(
    "Pergunte qualquer coisa à Eternity…",
    accept_file="multiple",
    file_type=["png", "jpg", "jpeg", "webp"],
)

if prompt:
    text = (prompt.text or "").strip()
    files = (list(prompt.files or []) + side_files)[:MAX_IMAGES]
    used_side = bool(side_files)

    images = []
    for f in files:
        try:
            images.append(prepare_image(f))
        except Exception:
            st.toast("Não consegui abrir uma das imagens.", icon="⚠️")

    text, run_mode = parse_command(text, mode, bool(images))
    if images and run_mode == "img":
        run_mode = "fast"  # não dá para gerar imagem a partir de uma foto: vira pergunta de visão

    if text or images:
        user_msg = {"role": "user", "content": text, "thumbs": [make_thumb(b) for b in images]}
        mem["messages"].append(user_msg)
        mem["turns"] += 1
        render(user_msg)
        ph = st.empty()
        ok = False

        if run_mode == "img":
            ph.markdown('<div class="thinking">🎨 Criando sua imagem… pode levar até um minuto.</div>',
                        unsafe_allow_html=True)
            en_prompt = rewrite_image_prompt(text)
            data, err = generate_image(en_prompt)
            if data:
                reply_msg = {"role": "assistant", "gen": data,
                             "content": f"Pronto! 🎨\n\n*Prompt usado:* {en_prompt}"}
                mem["messages"].append(reply_msg)
                with ph.container():
                    render(reply_msg)
                ok = True
            else:
                ph.empty()
                st.error("O gerador de imagens gratuito está ocupado ou indisponível agora. "
                         "Tente de novo em alguns instantes.")
                with st.expander("Detalhes técnicos"):
                    st.code(str(err))
        else:
            if CREATOR_TRIGGER.search(text or "") and not images:
                lang_label = st.session_state.get("response_language", "Português (Brasil)")
                reply = CREATOR_ANSWERS.get(lang_label, "Foi você que me criou! ✦")
                ph.markdown(reply)
                mem["messages"].append({"role": "assistant", "content": reply})
                ok = True
            else:
                state = {"ok": False, "error": None, "model": None}
                label = "🧠 Pensando a fundo… isso pode levar um pouco" if run_mode == "deep" else "Pensando…"
                api_msgs = build_api_messages(build_system(run_mode), mem["messages"], images)
                reply = stream_to(ph, stream_reply(api_msgs, pick_models(bool(images)), run_mode, state), label)
                if state["ok"] and reply:
                    mem["messages"].append({"role": "assistant", "content": reply})
                    st.session_state.model_used = state["model"]
                    ok = True
                else:
                    ph.empty()
                    st.error("Não consegui obter resposta de nenhum modelo da Groq. "
                             "Verifique sua chave e os modelos liberados para ela.")
                    if state["error"]:
                        with st.expander("Detalhes técnicos"):
                            st.code(state["error"])

        if ok:
            save_memory(mem)
            if mem["turns"] % REFLECT_EVERY == 0 or LEARN_TRIGGER.search(text or ""):
                try:
                    if reflect():
                        save_memory(mem)
                        st.toast("Memória atualizada", icon="🧬")
                except Exception:
                    pass
        else:
            mem["messages"].pop()
            mem["turns"] -= 1

        if used_side:
            st.session_state.pend_n += 1
            st.rerun()
