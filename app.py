import streamlit as st
from groq import Groq
import os

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LLaMA 4 · Scout",
    page_icon="🦙",
    layout="centered",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset & base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e4dc !important;
    font-family: 'Syne', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 90%, rgba(255,80,30,0.08) 0%, transparent 55%),
        #0a0a0f !important;
}

/* hide default header/footer */
[data-testid="stHeader"], footer { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }

/* ── Main container ── */
.block-container {
    max-width: 780px !important;
    padding: 3rem 2rem 6rem !important;
}

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #ff8c32;
    border: 1px solid rgba(255,140,50,0.35);
    border-radius: 2px;
    padding: 4px 12px;
    margin-bottom: 1.1rem;
    background: rgba(255,140,50,0.06);
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.05;
    margin: 0 0 0.55rem;
    background: linear-gradient(135deg, #fff 30%, #ff8c32 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero p {
    font-size: 0.92rem;
    color: rgba(232,228,220,0.5);
    margin: 0;
    letter-spacing: 0.02em;
}
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,140,50,0.3), transparent);
    margin: 2rem 0;
}

/* ── Chat bubbles ── */
.chat-wrap {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.bubble {
    padding: 0.85rem 1.1rem;
    border-radius: 4px;
    font-size: 0.9rem;
    line-height: 1.65;
    max-width: 88%;
    position: relative;
    animation: fadeUp 0.3s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.bubble-user {
    align-self: flex-end;
    background: rgba(255,140,50,0.12);
    border: 1px solid rgba(255,140,50,0.25);
    color: #f0ece4;
}
.bubble-user::before {
    content: "YOU";
    display: block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.15em;
    color: #ff8c32;
    margin-bottom: 0.4rem;
}
.bubble-ai {
    align-self: flex-start;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    color: #d8d4cc;
}
.bubble-ai::before {
    content: "LLAMA 4 · SCOUT";
    display: block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.15em;
    color: rgba(255,255,255,0.35);
    margin-bottom: 0.4rem;
}

/* ── Input area ── */
[data-testid="stTextInput"] input {
    background: #1a1a24 !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 3px !important;
    color: #ffffff !important;
    caret-color: #ff8c32 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.88rem !important;
    padding: 0.65rem 0.9rem !important;
    transition: border-color 0.2s, background 0.2s;
    -webkit-text-fill-color: #ffffff !important;
}
[data-testid="stTextInput"] input:focus {
    background: #1e1e2e !important;
    border-color: rgba(255,140,50,0.6) !important;
    box-shadow: 0 0 0 3px rgba(255,140,50,0.1) !important;
    -webkit-text-fill-color: #ffffff !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: rgba(255,255,255,0.28) !important;
    -webkit-text-fill-color: rgba(255,255,255,0.28) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #ff8c32, #ff4e1a) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 3px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.06em !important;
    padding: 0.55rem 1.4rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Sidebar / settings panel ── */
[data-testid="stSidebar"] {
    background: #0f0f17 !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}
[data-testid="stSidebar"] * { color: #c8c4bc !important; }
[data-testid="stSidebar"] .stSlider [data-testid="stMarkdownContainer"] p {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.05) !important;
    border-color: rgba(255,255,255,0.12) !important;
    border-radius: 3px !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p { color: #ff8c32 !important; font-size: 0.8rem !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,140,50,0.25); border-radius: 99px; }
</style>
""", unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key" not in st.session_state:
    st.session_state.api_key = ""


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")

    api_key_input = st.text_input(
        "Groq API Key",
        type="password",
        value=st.session_state.api_key,
        placeholder="gsk_...",
        help="Get your key at console.groq.com"
    )
    if api_key_input:
        st.session_state.api_key = api_key_input

    model = st.selectbox(
        "Model",
        options=[
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "meta-llama/llama-4-maverick-17b-128e-instruct",
            "llama3-70b-8192",
            "llama3-8b-8192",
            "mixtral-8x7b-32768",
        ],
        index=0,
    )

    temperature = st.slider("Temperature", 0.0, 2.0, 1.0, 0.05)
    max_tokens  = st.slider("Max Tokens",  256, 4096, 1024, 128)

    st.markdown("---")
    if st.button("🗑  Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        "<p style='font-size:0.7rem;color:rgba(200,196,188,0.35);margin-top:1rem;'>"
        "Powered by Groq · LLaMA 4</p>",
        unsafe_allow_html=True,
    )


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">Groq · LLaMA 4 · Scout</div>
    <h1>Ask Anything</h1>
    <p>Ultra-fast inference · 17B parameters · 16 experts</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Chat history ───────────────────────────────────────────────────────────────
if st.session_state.messages:
    # Show only the latest user + assistant pair (no history buildup)
    last_msgs = st.session_state.messages[-2:] if len(st.session_state.messages) >= 2 else st.session_state.messages
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for msg in last_msgs:
        css_class = "bubble-user" if msg["role"] == "user" else "bubble-ai"
        content = msg["content"].replace("<", "&lt;").replace(">", "&gt;")
        st.markdown(
            f'<div class="bubble {css_class}">{content}</div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)


# ── Input row ──────────────────────────────────────────────────────────────────
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "Message",
        label_visibility="collapsed",
        placeholder="Ask something… e.g. 'Explain AI vs Gen AI vs Agentic AI'",
        key="user_input",
    )
with col2:
    send = st.button("Send →", use_container_width=True)


# ── Send logic ─────────────────────────────────────────────────────────────────
if send and user_input.strip():
    effective_key = st.session_state.api_key or os.environ.get("GROQ_API_KEY", "")

    if not effective_key:
        st.error("⚠️  Please enter your Groq API key in the sidebar.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input.strip()})

    client = Groq(api_key=effective_key)

    with st.spinner("Generating response…"):
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                temperature=temperature,
                max_completion_tokens=max_tokens,
                top_p=1,
                stream=True,
                stop=None,
            )

            full_response = ""
            for chunk in completion:
                delta = chunk.choices[0].delta.content or ""
                full_response += delta

            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

        except Exception as e:
            st.error(f"API error: {e}")
            st.session_state.messages.pop()

    st.rerun()
