import os
import base64
import streamlit as st
from groq import Groq

# 1. Configuração da Página
st.set_page_config(
    page_title="Eternity",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Design Minimalista Estilo ChatGPT / Claude (Dark Mode Profissional)
st.markdown("""
<style>
    /* Fundo preto fosco global */
    .stApp {
        background-color: #121212;
        color: #e3e3e3;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Cabeçalho minimalista centralizado */
    .chat-header {
        text-align: center;
        padding: 40px 0 20px 0;
    }
    .chat-title {
        font-size: 1.5rem;
        font-weight: 500;
        color: #ffffff;
        letter-spacing: -0.3px;
    }
    .chat-subtitle {
        font-size: 0.85rem;
        color: #757575;
        margin-top: 4px;
    }

    /* Estilo limpo das mensagens */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
        padding: 18px 0 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03) !important;
    }

    /* Caixa de input inferior flutuante */
    .stChatInputContainer {
        padding-bottom: 15px !important;
        background-color: transparent !important;
    }
    
    .stChatInputContainer textarea {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
    }
    
    .stChatInputContainer textarea:focus {
        border-color: #666666 !important;
        box-shadow: none !important;
    }

    /* Esconder elementos feios nativos do Streamlit */
    div[data-testid="stFileUploader"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho da Eternity
st.markdown("""
<div class="chat-header">
    <div class="chat-title">Eternity</div>
    <div class="chat-subtitle">Como posso ajudar você hoje?</div>
</div>
""", unsafe_allow_html=True)

# 3. Inicializar chave de API da Groq
groq_api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

if not groq_api_key:
    st.warning("⚠️ Chave de API não configurada.")
    groq_api_key = st.text_input("Insira sua Groq API Key:", type="password")
    if not groq_api_key:
        st.stop()

client = Groq(api_key=groq_api_key)

# 4. Prompt de Comportamento
SYSTEM_PROMPT = """
Você é a Eternity, uma inteligência artificial minimalista, direta, inteligente e muito educada.
Responda de forma clara, limpa e objetiva, sem excessos de emojis ou textos enrolados.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico de conversas
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. Entrada de Texto Flutuante (Estilo ChatGPT puro)
user_input = st.chat_input("Mensagem para Eternity...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("..."):
            try:
                # Modelo super estável da Groq que nunca falha
                model_to_use = "llama3-8b-8k"
                
                messages_to_send = [{"role": "system", "content": SYSTEM_PROMPT}]
                for m in st.session_state.messages:
                    messages_to_send.append({"role": m["role"], "content": m["content"]})

                response = client.chat.completions.create(
                    model=model_to_use,
                    messages=messages_to_send,
                    temperature=0.7,
                    max_tokens=1024,
                )
                
                bot_reply = response.choices[0].message.content
                st.write(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            except Exception as e:
                st.error(f"Erro ao processar: {e}")
