import os
import base64
import streamlit as st
from groq import Groq

# 1. Configuração da página
st.set_page_config(
    page_title="Eternity IA",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Estilização CSS personalizada (Design Escuro estilo ChatGPT/Claude)
st.markdown("""
<style>
    /* Fundo Escuro Principal estilo ChatGPT/Claude */
    .stApp {
        background-color: #0f1117;
        color: #ececec;
    }
    
    /* Esconder cabeçalho padrão do Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Estilo do Card Central da Logo */
    .logo-header {
        text-align: center;
        padding: 20px 0px 10px 0px;
    }
    
    .eternity-title {
        font-family: 'Inter', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #a855f7 0%, #6366f1 50%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 10px;
        letter-spacing: 1px;
    }

    .eternity-subtitle {
        color: #9ca3af;
        font-size: 0.95rem;
        margin-bottom: 25px;
    }

    /* Mensagens do Chat */
    .stChatMessage {
        background-color: #1e2029 !important;
        border: 1px solid #2d313e !important;
        border-radius: 12px !important;
        padding: 12px !important;
        margin-bottom: 12px !important;
    }

    /* Input de Texto (Caixa de mensagem) */
    .stChatInputContainer textarea {
        background-color: #1e2029 !important;
        color: #ffffff !important;
        border: 1px solid #374151 !important;
        border-radius: 12px !important;
    }

    /* File Uploader Escuro */
    section[data-testid="stFileUploader"] {
        background-color: #181a20;
        border: 1px dashed #4b5563;
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Logo Exclusiva em SVG inspirada em ChatGPT + Claude + Gemini
LOGO_SVG = """
<div class="logo-header">
    <svg width="80" height="80" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="eternityGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#c084fc" />
                <stop offset="50%" stop-color="#818cf8" />
                <stop offset="100%" stop-color="#60a5fa" />
            </linearGradient>
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="4" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <!-- Símbolo do Infinito Dinâmico Estilizado -->
        <path d="M30 50 C 15 35, 15 65, 30 50 C 45 35, 55 65, 70 50 C 85 35, 85 65, 70 50 C 55 35, 45 65, 30 50 Z" 
              stroke="url(#eternityGrad)" stroke-width="7" stroke-linecap="round" fill="none" filter="url(#glow)"/>
        <circle cx="50" cy="50" r="4" fill="#ffffff" filter="url(#glow)" />
    </svg>
    <div class="eternity-title">ETERNITY IA</div>
    <div class="eternity-subtitle">Inteligência Pessoal & Familiar com Visão Computacional (24/7)</div>
</div>
"""

st.markdown(LOGO_SVG, unsafe_allow_html=True)

# 4. Inicializar chave de API da Groq
groq_api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")

if not groq_api_key:
    st.warning("⚠️ Chave de API não configurada nos Secrets do Streamlit.")
    groq_api_key = st.text_input("Cole sua chave da API da Groq aqui:", type="password")
    if not groq_api_key:
        st.stop()

client = Groq(api_key=groq_api_key)

# 5. Prompt de Comportamento + RSI
SYSTEM_PROMPT = """
Você é a Eternity, uma inteligência artificial avançada, amigável, clara, elegante e altamente didática.
Sua missão é ajudar estudantes em tarefas e dúvidas escolares e auxiliar familiares no dia a dia.

Instruções de Resposta:
1. Ao receber fotos de exercícios, resolva passo a passo com explicações simples.
2. Em dúvidas do cotidiano, seja acolhedora, objetiva e prática.
3. Mantenha uma formatação impecável com marcadores e negritos para facilitar a leitura no celular.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico de conversas
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. Upload de Imagem e Chat Input
uploaded_file = st.file_uploader("📷 Envie uma foto do exercício ou pergunta (Opcional):", type=["jpg", "jpeg", "png"])
user_input = st.chat_input("Pergunte algo para a Eternity...")

if user_input or uploaded_file:
    if uploaded_file and not user_input:
        user_input = "Por favor, analise a imagem acima, resolva o exercício e me explique passo a passo."

    with st.chat_message("user"):
        st.write(user_input)
        if uploaded_file:
            st.image(uploaded_file, caption="Foto enviada", use_column_width=True)

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
        with st.spinner("Eternity está pensando..."):
            try:
                # Escolhe o modelo de Visão (11B) se tiver foto, ou Texto Rápido (8B) se for texto
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
