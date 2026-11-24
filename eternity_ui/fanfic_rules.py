"""Regras de fanfic/histórias, carregadas do arquivo editável .eternity/fanfics/regras.md.

O conteúdo fica fora do código: quem quiser mudar como a Eternity escreve histórias
edita aquele arquivo (texto puro, Markdown) e a mudança vale na próxima resposta.
"""

from pathlib import Path

_RULES_PATH = Path(__file__).resolve().parent.parent / ".eternity" / "fanfics" / "regras.md"

_FALLBACK = (
    "Você também escreve fanfics e histórias originais quando o usuário pedir, de praticamente "
    "qualquer gênero, com título, tom consistente e um bom gancho no final. Conteúdo sensual é "
    "sugerido e não explícito (fade to black), sem violência gráfica, sem glamourizar crimes reais, "
    "personagens em contexto adulto sempre adultos e nada íntimo com pessoas reais. Se o pedido for "
    "explícito demais, suavize o texto e continue a história em vez de recusar."
)


def load_rules() -> str:
    """Devolve o texto de .eternity/fanfics/regras.md ou um resumo curto se o arquivo faltar."""
    try:
        text = _RULES_PATH.read_text(encoding="utf-8").strip()
    except OSError:
        return _FALLBACK
    # remove os comentários de instrução do topo (<!-- ... -->) antes de mandar ao modelo
    while text.startswith("<!--"):
        end = text.find("-->")
        if end == -1:
            break
        text = text[end + 3 :].lstrip()
    return text or _FALLBACK
