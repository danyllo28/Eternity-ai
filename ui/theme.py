"""Visual tokens and stylesheet for the Eternity Streamlit redesign.

The stylesheet is namespaced to avoid affecting Streamlit internals beyond the
small set of stable widget containers needed to theme native controls.
"""

DARK_TOKENS = """
:root {
  color-scheme: dark;
  --et-new-bg: #090A0C;
  --et-new-sidebar: #0E1014;
  --et-new-surface: #151820;
  --et-new-surface-raised: #1B1E26;
  --et-new-border: #292D37;
  --et-new-text: #F4F5F7;
  --et-new-muted: #A2A8B3;
  --et-new-crown: #FFFFFF;
  --et-new-radius-sm: 10px;
  --et-new-radius-md: 16px;
  --et-new-radius-lg: 24px;
  --et-new-content-width: 820px;
  --et-new-shadow: 0 18px 54px rgba(0, 0, 0, .28);
  --et-new-ease: cubic-bezier(.2, .75, .25, 1);
}

.stApp { background: var(--et-new-bg); color: var(--et-new-text); }
.block-container { max-width: 1440px; padding: 1.2rem 1.5rem 8.5rem; }
[data-testid="stSidebar"] { background: var(--et-new-sidebar); border-right: 1px solid var(--et-new-border); }
[data-testid="stSidebar"] .stButton > button {
  min-height: 40px; border-radius: 12px; border: 1px solid transparent;
  background: transparent; color: var(--et-new-text); text-align: left;
  transition: background .18s var(--et-new-ease), border-color .18s var(--et-new-ease);
}
[data-testid="stSidebar"] .stButton > button:hover { background: var(--et-new-surface-raised); border-color: var(--et-new-border); }
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button {
  border-radius: var(--et-new-radius-sm); transition: transform .16s var(--et-new-ease), background .16s var(--et-new-ease);
}
.stButton > button:focus-visible, button:focus-visible, textarea:focus-visible, input:focus-visible {
  outline: 2px solid #DDE1E8; outline-offset: 3px;
}
[data-testid="stChatInput"] {
  max-width: var(--et-new-content-width); margin-inline: auto;
  border: 1px solid var(--et-new-border); border-radius: var(--et-new-radius-lg);
  background: var(--et-new-surface); box-shadow: var(--et-new-shadow);
}
[data-testid="stBottom"] { background: linear-gradient(0deg, var(--et-new-bg) 58%, transparent); }
[data-testid="stBottomBlockContainer"] { padding-bottom: max(.8rem, env(safe-area-inset-bottom)); }
.et-new-brand, .et-new-page-heading { animation: et-new-enter .42s var(--et-new-ease) both; }
.et-new-brand { display: flex; align-items: center; gap: .65rem; color: var(--et-new-text); }
.et-new-brand svg { width: 28px; height: 25px; flex: none; }
.et-new-brand-name { font-size: 1.16rem; font-weight: 650; letter-spacing: -.035em; }
.et-new-welcome { width: min(100%, 760px); margin: clamp(4rem, 14vh, 9rem) auto 1.5rem; text-align: center; }
.et-new-welcome-crown { display: inline-grid; place-items: center; margin-bottom: 1rem; animation: et-new-enter .45s var(--et-new-ease) both; }
.et-new-welcome-crown svg { width: 46px; height: 40px; filter: drop-shadow(0 0 22px rgba(255,255,255,.15)); }
.et-new-welcome h1 { margin: 0; color: var(--et-new-text); font-size: clamp(1.7rem, 3.4vw, 2.45rem); letter-spacing: -.045em; font-weight: 600; }
.et-new-welcome p { margin: .65rem 0 0; color: var(--et-new-muted); font-size: 1rem; }
.et-new-message-area { width: min(100%, var(--et-new-content-width)); margin-inline: auto; }
.et-new-user-message { max-width: min(78%, 680px); margin: 1.1rem 0 1.1rem auto; padding: .8rem 1rem; border: 1px solid var(--et-new-border); border-radius: 18px 18px 5px 18px; background: var(--et-new-surface-raised); overflow-wrap: anywhere; }
.et-new-assistant-message { max-width: min(100%, var(--et-new-content-width)); margin: 1.25rem auto; line-height: 1.75; }
.et-new-loader { display: flex; align-items: center; gap: 12px; width: fit-content; color: var(--et-new-muted); font-size: .88rem; }
.et-new-thinking { position: relative; display: grid; place-items: center; width: 52px; height: 52px; flex: none; }
.et-new-thinking::before { content: ""; position: absolute; inset: 5px; border: 1px solid rgba(255,255,255,.09); border-radius: 50%; box-shadow: 0 0 24px rgba(255,255,255,.04); animation: et-new-halo 2.2s ease-in-out infinite; }
.et-new-thinking svg { position: relative; z-index: 1; width: 31px; height: 28px; overflow: visible; animation: et-new-crown-glow 2.2s ease-in-out infinite; }
.et-new-particle { position: absolute; top: 50%; left: 50%; width: 5px; height: 5px; border-radius: 50%; background: #FFF; box-shadow: 0 0 10px rgba(255,255,255,.9); transform: translate(-50%,-50%); }
.et-new-particle:nth-child(2) { --rx: 21px; --ry: 11px; --phase: 0s; --size: 1; animation: et-new-orbit 2.4s ease-in-out infinite; }
.et-new-particle:nth-child(3) { --rx: 13px; --ry: 21px; --phase: -.8s; --size: .78; animation: et-new-orbit 2.8s ease-in-out infinite; }
.et-new-particle:nth-child(4) { --rx: 23px; --ry: 16px; --phase: -1.5s; --size: .62; animation: et-new-orbit 3.1s ease-in-out infinite; }
.et-new-page-heading { width: min(100%, 960px); margin: 1rem auto 1.5rem; }
.et-new-page-heading h1 { margin: 0; letter-spacing: -.04em; font-size: clamp(1.6rem, 3vw, 2.1rem); }
.et-new-page-heading p { color: var(--et-new-muted); margin: .45rem 0 0; }
[data-testid="stMarkdown"] pre { max-width: 100%; overflow-x: auto; border: 1px solid var(--et-new-border); border-radius: var(--et-new-radius-md); }
[data-testid="stMarkdown"] table { display: block; max-width: 100%; overflow-x: auto; }
@keyframes et-new-enter { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
@keyframes et-new-halo { 0%,100% { opacity: .38; transform: scale(.94); } 50% { opacity: .82; transform: scale(1.05); } }
@keyframes et-new-crown-glow { 0%,100% { filter: drop-shadow(0 0 2px rgba(255,255,255,.3)); opacity: .82; transform: scale(.97); } 50% { filter: drop-shadow(0 0 9px rgba(255,255,255,.75)); opacity: 1; transform: scale(1.03); } }
@keyframes et-new-orbit { 0% { opacity: .25; transform: translate(-50%,-50%) translate(0, calc(var(--ry) * -1)) scale(var(--size)); } 25% { opacity: .9; transform: translate(-50%,-50%) translate(var(--rx), calc(var(--ry) * -.5)) scale(calc(var(--size) * 1.12)); } 50% { opacity: .55; transform: translate(-50%,-50%) translate(calc(var(--rx) * .55), var(--ry)) scale(var(--size)); } 75% { opacity: 1; transform: translate(-50%,-50%) translate(calc(var(--rx) * -1), calc(var(--ry) * .25)) scale(calc(var(--size) * .9)); } 100% { opacity: .25; transform: translate(-50%,-50%) translate(0, calc(var(--ry) * -1)) scale(var(--size)); } }
@media (max-width: 760px) {
  .block-container { padding: .8rem .75rem 8.5rem; }
  .et-new-welcome { margin: 3rem auto 1.1rem; }
  .et-new-user-message { max-width: 94%; }
  [data-testid="stChatInput"] { border-radius: 19px; }
}
@media (prefers-reduced-motion: reduce) {
  .et-new-brand, .et-new-page-heading, .et-new-welcome-crown, .et-new-thinking::before,
  .et-new-thinking svg, .et-new-particle { animation: none !important; }
  .et-new-particle { opacity: .65; }
  *, *::before, *::after { scroll-behavior: auto !important; transition-duration: .01ms !important; }
}
"""


def inject_theme(st, css_extra=""):
    """Inject Eternity's namespaced UI theme into a Streamlit page."""
    st.markdown(f"<style>{DARK_TOKENS}\n{css_extra}</style>", unsafe_allow_html=True)
