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

# 2. Design Minimalista Profissional (Estilo ChatGPT / Claude Dark Mode)
st.markdown("""
<style>
    /* Fundo preto fosco global estilo ChatGPT */
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
        padding: 35px 0 15px 0;
    }
    .chat-title {
        font-size: 1.4rem;
        font-weight: 500;
        color: #ffffff;
        letter-spacing: -0.3px;
    }
    .chat-subtitle {
        font-size: 0.85rem;
        color: #757575;
        margin-top: 4px;
    }

    /* Estilo limpo das mensagens (sem caixas pesadas) */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
        padding: 16px 0 !important;
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

    /* Área de upload limpa e discreta no topo lateral */
    div[data-testid="stFileUploader"] {
        background-color: #181818;
        border: 1px dashed #333333;
        border-radius: 10px;
        padding: 8px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho da Eternity
st.markdown("""
<div class="chat-header">
    <div class="chat-title">Eternity</div>
    <div class="chat-subtitle">Assistente Pessoal & Inteligência Modular</div>
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

# 5. Upload de Imagem Discreto e Entrada de Texto
uploaded_file = st.file_uploader("📎 Enviar foto de exercício ou documento (Opcional)", type=["jpg", "jpeg", "png"])
user_input = st.chat_input("Digite sua mensagem para a Eternity...")

if user_input or uploaded_file:
    if uploaded_file and not user_input:
        user_input = "Por favor, analise esta imagem e explique o conteúdo passo a passo."

    with st.chat_message("user"):
        st.write(user_input)
        if uploaded_file:
            st.image(uploaded_file, caption="Imagem enviada", use_column_width=True)

    content_payload = []
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        base64_image = base64.b64encode(bytes_data).decode('utf-8')
        image_url = f"data:image/jpeg;base64,{base64_image}"
        content_payload.append({"type": "text", "text": user_input})
        content_payload.append({
            "type": "image_url",
            "image_url": {"url": image_url}
        })
    else:
        content_payload = user_input

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("..."):
            try:
                # Modelo ultra estável e atualizado da Groq
                model_to_use = "llama-3.2-11b-vision-preview" if uploaded_file else "llama-3.1-8b-instant"
                
                messages_to_send = [{"role": "system", "content": SYSTEM_PROMPT}]
                messages_to_send.append({"role": "user", "content": content_payload})

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
