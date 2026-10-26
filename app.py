import os
import base64
import streamlit as st
from groq import Groq

# 1. Configuração da página
st.set_page_config(
    page_title="Eternity",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Design Minimalista & Sofisticado (Estilo ChatGPT / Claude Dark Mode)
st.markdown("""
<style>
    /* Fundo principal minimalista escuro */
    .stApp {
        background-color: #171717;
        color: #ececec;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Cabeçalho minimalista */
    .minimal-header {
        text-align: center;
        padding: 30px 0 15px 0;
    }
    .minimal-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #f3f4f6;
        letter-spacing: -0.5px;
    }
    .minimal-subtitle {
        font-size: 0.85rem;
        color: #8e8ea0;
        margin-top: 2px;
    }

    /* Mensagens limpas */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
        padding: 16px 0 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04) !important;
    }

    /* Caixa de input inferior flutuante */
    .stChatInputContainer {
        border-top: none !important;
        background-color: transparent !important;
        padding-bottom: 10px !important;
    }
    
    .stChatInputContainer textarea {
        background-color: #212121 !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
    }
    
    .stChatInputContainer textarea:focus {
        border-color: #555555 !important;
        box-shadow: none !important;
    }

    /* Upload de imagem minimalista */
    section[data-testid="stFileUploader"] {
        background-color: #212121;
        border: 1px solid #333333;
        border-radius: 10px;
        padding: 6px;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho limpo
st.markdown("""
<div class="minimal-header">
    <div class="minimal-title">Eternity</div>
    <div class="minimal-subtitle">Assistente inteligente & pessoal</div>
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

# 5. Anexo e Entrada de Texto
uploaded_file = st.file_uploader("📎 Anexar imagem ou exercício (opcional):", type=["jpg", "jpeg", "png"])
user_input = st.chat_input("Mensagem para Eternity...")

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
                # Usando modelos atuais e ultra estáveis da Groq
                model_to_use = "llama-3.2-11b-vision-preview" if uploaded_file else "llama-3.3-70b-versatile"
                
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
