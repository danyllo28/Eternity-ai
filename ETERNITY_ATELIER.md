# Eternity Atelier

O arquivo `atelier.py` é uma experiência alternativa de chat para a Eternity, com interface reorganizada: barra lateral limpa, histórico pesquisável, modelos agrupados com descrições, seleção de modelo e esforço perto do campo de mensagem, modos de conversa, sugestões iniciais, animações suaves e exportação em Markdown.

## Executar

1. Configure `GROQ_API_KEY` em Streamlit → Settings → Secrets (ou como variável de ambiente).
2. Execute `streamlit run atelier.py`.

O `app.py` original permanece intacto. A experiência usa os modelos Groq cadastrados em `MODEL_CATALOG`. Conversas deste protótipo ficam na sessão atual do navegador; não são sincronizadas com o histórico da app principal.

A interface mostra etapas de carregamento e pode oferecer uma explicação resumida e verificável da resposta. Ela não revela uma transcrição de raciocínio interno privado.
