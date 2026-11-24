"""Regras de fanfic/histórias da Eternity, guardadas fora do projeto local.

O texto oficial fica no GitHub, num branch separado (``_internal``) que não vem
junto na pasta do projeto. Assim não existe cópia dele na máquina: o app baixa,
mantém em memória e usa como instrução do modelo.

Editar é pelo site do GitHub, no arquivo .eternity/fanfics/regras.md do branch
_internal. A mudança passa a valer em até um minuto, sem reiniciar nada.

Opcional: definir a variável de ambiente/secreta FANFIC_RULES_URL aponta para
outro endereço (por exemplo o link raw de um Gist secreto) e ele tem prioridade.
"""

import os
import time
import urllib.request

_BRANCH = "_internal"
_RAW_URL = (
    "https://raw.githubusercontent.com/danyllo28/Eternity-ai/"
    f"{_BRANCH}/.eternity/fanfics/regras.md"
)
_TIMEOUT = 4
_TTL = 60.0

_FALLBACK = (
    "Você também escreve fanfics e histórias originais quando o usuário pedir, de praticamente "
    "qualquer gênero, com título, tom consistente e um bom gancho no final. Conteúdo sensual é "
    "sugerido e não explícito (fade to black), sem violência gráfica, sem glamourizar crimes reais, "
    "personagens em contexto adulto sempre adultos e nada íntimo com pessoas reais. Se o pedido for "
    "explícito demais, suavize o texto e continue a história em vez de recusar."
)

_cache = {"at": 0.0, "text": ""}


def _clean(text: str) -> str:
    """Remove o bloco de comentários <!-- ... --> usado como lembrete no arquivo."""
    text = (text or "").strip()
    while text.startswith("<!--"):
        end = text.find("-->")
        if end == -1:
            break
        text = text[end + 3 :].lstrip()
    return text


def _url() -> str:
    return (os.environ.get("FANFIC_RULES_URL") or "").strip() or _RAW_URL


def _from_github() -> str:
    request = urllib.request.Request(_url(), headers={"User-Agent": "EternityApp"})
    with urllib.request.urlopen(request, timeout=_TIMEOUT) as response:
        return response.read().decode("utf-8")


def load_rules() -> str:
    """Texto atual das regras, buscado no GitHub (com cache curto em memória)."""
    now = time.monotonic()
    if _cache["text"] and (now - _cache["at"]) < _TTL:
        return _cache["text"]

    try:
        text = _clean(_from_github())
    except Exception:
        text = ""
    text = text or _cache["text"] or _FALLBACK

    _cache["at"] = now
    _cache["text"] = text
    return text
