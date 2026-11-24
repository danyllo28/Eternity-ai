"""Regras de fanfic/histórias da Eternity.

A fonte oficial do texto é o arquivo no GitHub (branch main):
https://github.com/danyllo28/Eternity-ai/blob/main/.eternity/fanfics/regras.md

O app baixa esse arquivo do GitHub a cada minuto, então editar lá (pelo site do
GitHub, sem terminal) muda o comportamento da Eternity sem reiniciar nada.
A cópia local .eternity/fanfics/regras.md só é usada como reserva quando o app
está sem internet — editar a cópia local não tem efeito enquanto houver conexão.
"""

import time
import urllib.request
from pathlib import Path

_RAW_URL = "https://raw.githubusercontent.com/danyllo28/Eternity-ai/main/.eternity/fanfics/regras.md"
_LOCAL_PATH = Path(__file__).resolve().parent.parent / ".eternity" / "fanfics" / "regras.md"
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


def _from_github() -> str:
    request = urllib.request.Request(_RAW_URL, headers={"User-Agent": "EternityApp"})
    with urllib.request.urlopen(request, timeout=_TIMEOUT) as response:
        return response.read().decode("utf-8")


def _from_local() -> str:
    try:
        return _LOCAL_PATH.read_text(encoding="utf-8")
    except OSError:
        return ""


def load_rules() -> str:
    """Texto atual das regras (GitHub primeiro, arquivo local como reserva)."""
    now = time.monotonic()
    if _cache["text"] and (now - _cache["at"]) < _TTL:
        return _cache["text"]

    text = ""
    try:
        text = _clean(_from_github())
    except Exception:
        text = ""
    text = text or _clean(_from_local()) or _FALLBACK

    _cache["at"] = now
    _cache["text"] = text
    return text
