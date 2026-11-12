# Eternity Atelier

O arquivo `atelier.py` adiciona uma experiência de chat alternativa, com uma identidade visual própria da Eternity: interface responsiva, animações suaves, conversas por sessão, modos para conversa/código/escrita/estudo, seleção de modelo, esforço rápido/aprofundado, sugestões de início e exportação em Markdown.

## Executar

1. Configure `GROQ_API_KEY` em Streamlit → Settings → Secrets (ou como variável de ambiente).
2. Execute `streamlit run atelier.py`.

O `app.py` original permanece intacto. O Atelier é um ponto de entrada alternativo para testar o redesign sem substituir as funções existentes.

### Sobre explicações

O Atelier pode apresentar uma explicação breve e verificável da resposta, mas não revela transcrições de raciocínio interno privado. O indicador de progresso mostra estados de interface, não uma reprodução do pensamento oculto do modelo.
