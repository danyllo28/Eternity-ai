# Eternity AI

Eternity é uma IA pessoal criada pelo Danyllo, com identidade própria, memória, conversas, imagens, arquivos e interface responsiva.

## Novidades desta versão

- Ações rápidas: Resumir, Explicar simples, Continuar, Ideias, Estudar, Traduzir, Regenerar e Melhorar texto.
- Copiar, Ouvir e Salvar respostas.
- Conversas fixadas no histórico.
- Modo foco.
- Ícones personalizados da Eternity, inspirados na coroa oficial.
- Interface adaptada para PC, tablet e celular.
- Barra inferior no celular e menu lateral em gaveta.
- Suporte a safe-area em celulares com notch.

## Como rodar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Estrutura

- `app.py` — aplicação principal.
- `eternity_ui/` — identidade, tema, componentes e recursos.
- `assets/icons/` — pacote de ícones SVG da Eternity.
- `eternity_memory.json` — memória local (criada ao usar o app).

## Ícones

Os ícones ficam em `assets/icons/` e também podem ser usados direto no código:

```python
from eternity_ui.icons import icon_svg
st.markdown(icon_svg("sparkle", 18), unsafe_allow_html=True)
```

## Enviar para o GitHub

1. Crie um repositório no GitHub.
2. Envie todos os arquivos desta pasta.
3. No FreeBuff, peça para adicionar o repositório e rodar:

```bash
pip install -r requirements.txt
streamlit run app.py
```

A Eternity pode cometer erros. Confira informações importantes.
