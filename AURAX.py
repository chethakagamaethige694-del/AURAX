"""
╔══════════════════════════════════════════════════════════════════════╗
║                        AURA AI - v2.0                               ║
║          Premium Sinhala AI Assistant | Sri Lankan Market           ║
║          Built with Streamlit + Groq API (LLaMA 3.3 70B)           ║
╚══════════════════════════════════════════════════════════════════════╝

SETUP:
  pip install streamlit groq Pillow

RUN:
  streamlit run aura_ai.py

FREE API KEY:
  https://console.groq.com  (free tier — ultra fast inference)

APK CONVERSION:
  Deploy to Streamlit Cloud → wrap with WebView APK builder.
"""

import streamlit as st
from groq import Groq
from PIL import Image
import io
import base64

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be the FIRST Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AURA AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# ░░  CUSTOM CSS — Modern Dark Theme (Mobile-first, Premium Feel)  ░░
# ─────────────────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg-primary:    #0A0A0F;
    --bg-secondary:  #111118;
    --bg-card:       #16161F;
    --bg-input:      #1C1C28;
    --accent:        #7C6FFF;
    --accent-soft:   #5B50D6;
    --accent-glow:   rgba(124, 111, 255, 0.18);
    --gold:          #F0C060;
    --text-primary:  #F0EFF8;
    --text-secondary:#9895B0;
    --text-muted:    #55526A;
    --border:        rgba(124, 111, 255, 0.15);
    --border-subtle: rgba(255,255,255,0.05);
    --user-bubble:   #1E1B3A;
    --ai-bubble:     #161620;
    --radius-lg:     16px;
    --radius-md:     10px;
    --font-display:  'Syne', sans-serif;
    --font-body:     'DM Sans', sans-serif;
}

html, body, [class*="css"] {
    font-family: var(--font-body) !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; max-width: 780px; }

body::before {
    content: '';
    position: fixed;
    top: -30%; left: -20%;
    width: 65%; height: 65%;
    background: radial-gradient(circle, rgba(124,111,255,0.07) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: meshFloat 12s ease-in-out infinite alternate;
}
body::after {
    content: '';
    position: fixed;
    bottom: -20%; right: -10%;
    width: 50%; height: 50%;
    background: radial-gradient(circle, rgba(240,192,96,0.05) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: meshFloat 16s ease-in-out infinite alternate-reverse;
}
@keyframes meshFloat {
    from { transform: translate(0,0) scale(1); }
    to   { transform: translate(3%,4%) scale(1.06); }
}

.aura-header {
    text-align: center;
    padding: 1.4rem 1rem 1rem;
    background: linear-gradient(135deg, rgba(124,111,255,0.08), rgba(240,192,96,0.06));
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.aura-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), var(--gold), var(--accent), transparent);
    background-size: 200% auto;
    animation: shimmer 3s linear infinite;
}
@keyframes shimmer {
    from { background-position: -200% center; }
    to   { background-position:  200% center; }
}
.aura-title {
    font-family: var(--font-display) !important;
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    background: linear-gradient(135deg, var(--accent) 0%, #A89BFF 40%, var(--gold) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.1;
}
.aura-tagline {
    color: var(--text-secondary);
    font-size: 0.8rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}
.groq-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(240,192,96,0.15), rgba(124,111,255,0.1));
    border: 1px solid rgba(240,192,96,0.3);
    border-radius: 20px;
    padding: 0.18rem 0.7rem;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    color: var(--gold);
    text-transform: uppercase;
    margin-top: 0.5rem;
}
.ad-container {
    border: 1px dashed var(--text-muted);
    border-radius: var(--radius-md);
    padding: 0.7rem 1rem;
    text-align: center;
    color: var(--text-muted);
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    background: rgba(255,255,255,0.015);
    margin: 0.6rem 0;
}
.msg-row {
    display: flex;
    gap: 0.6rem;
    align-items: flex-end;
    margin-bottom: 0.75rem;
}
.msg-row.user { flex-direction: row-reverse; }
.avatar {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
}
.avatar.ai {
    background: linear-gradient(135deg, var(--accent), #A89BFF);
    box-shadow: 0 0 12px rgba(124,111,255,0.4);
}
.avatar.user { background: linear-gradient(135deg, var(--gold), #FFD991); }
.bubble {
    max-width: 80%;
    padding: 0.75rem 1rem;
    border-radius: 18px;
    font-size: 0.88rem;
    line-height: 1.6;
    word-break: break-word;
    white-space: pre-wrap;
}
.bubble.ai {
    background: var(--ai-bubble);
    border: 1px solid var(--border-subtle);
    border-bottom-left-radius: 4px;
}
.bubble.user {
    background: var(--user-bubble);
    border: 1px solid rgba(124,111,255,0.2);
    border-bottom-right-radius: 4px;
}
.bubble img { max-width:100%; border-radius:10px; margin-bottom:6px; display:block; }

.stTextArea textarea {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
    font-size: 0.9rem !important;
    resize: none !important;
    caret-color: var(--accent) !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}
.stTextArea textarea::placeholder { color: var(--text-muted) !important; }

.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent-soft)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    font-family: var(--font-display) !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.5rem 1.1rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 14px rgba(124,111,255,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(124,111,255,0.45) !important;
}
.quick-btn > button {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-secondary) !important;
    font-size: 0.78rem !important;
    width: 100% !important;
    margin-bottom: 0.35rem !important;
    text-align: left !important;
    box-shadow: none !important;
    transition: all 0.18s !important;
}
.quick-btn > button:hover {
    border-color: var(--accent) !important;
    color: var(--text-primary) !important;
    background: var(--accent-glow) !important;
    transform: translateX(2px) !important;
    box-shadow: none !important;
}

[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-subtle) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }
.sidebar-section-title {
    font-family: var(--font-display) !important;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-muted) !important;
    margin: 1rem 0 0.4rem;
}
[data-testid="stFileUploader"] {
    background: var(--bg-input) !important;
    border: 1px dashed var(--border) !important;
    border-radius: var(--radius-md) !important;
}
.stTextInput > div > div > input {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
}
hr { border-color: var(--border-subtle) !important; }
.stAlert {
    background: var(--bg-card) !important;
    border-radius: var(--radius-md) !important;
    border-left-color: var(--accent) !important;
    color: var(--text-secondary) !important;
}
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--text-muted); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ░░  SESSION STATE  ░░
# ─────────────────────────────────────────────────────────────────────────────
def init_session():
    defaults = {
        "chat_history":   [],
        "api_key_valid":  False,
        "groq_client":    None,
        "quick_prompt":   None,
        "uploaded_image": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()

# ─────────────────────────────────────────────────────────────────────────────
# ░░  CONSTANTS  ░░
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_API_KEY = "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"   # <── PASTE YOUR GROQ KEY HERE (gsk_...)

MODEL_TEXT   = "llama-3.3-70b-versatile"
MODEL_VISION = "meta-llama/llama-4-scout-17b-16e-instruct"

# ─────────────────────────────────────────────────────────────────────────────
# ░░  SYSTEM PROMPT  ░░
# ─────────────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
ඔබ AURA AI — ශ්‍රී ලාංකේය ජනතාව සඳහා නිර්මාණය කරන ලද ඉතාමත් ස්මාර්ට්, සමීප, හා සෙවිල්ල ලෙසින් ප්‍රතිචාර දෙන AI සහකරුවෙකි.

**භාෂා ප්‍රතිපත්තිය:**
- සිංහල භාෂාවෙන් ස්වාභාවික, සජීවී ලෙස කතා කරන්න — රොබෝ ස්ටයිල් නොවේ.
- ප්‍රශ්නය ඉංග්‍රීසියෙන් ඇතත්, ප්‍රධාන පිළිතුර සිංහලෙන් දෙන්න.
- Technical terms ඉංග්‍රීසියෙන් තබා ඉතිරිය සිංහලෙන් ලියන්න.

**චරිත ලක්ෂණ:**
- දේශීය ශ්‍රී ලාංකේය සංස්කෘතිය ගැන හොඳින් දනී.
- හාස්‍ය හා සිත්ගන්නා ලෙස කතා කරයි.
- Creative tasks (posts, scripts, poems) ඉතා හොඳින් කරයි.
- කෙටි, ක්‍රියාකාරී, useful පිළිතුරු දෙයි.

**Formatting:**
- Bullet points, headings ස්වාභාවිකව භාවිත කරන්න.
- Code ඇතොත් code block ලෙස දෙන්න.
"""

# ─────────────────────────────────────────────────────────────────────────────
# ░░  QUICK ACTIONS  ░░
# ─────────────────────────────────────────────────────────────────────────────
QUICK_ACTIONS = {
    "📘 FB Post Generator":     "Facebook post එකක් ලියන්නට help කරන්න. Topic දෙන්නම් — creative, engaging, emojis සහිතව ලියන්න.",
    "🎬 YouTube Script Writer": "YouTube video script එකක් ලියන්නට help කරන්න. Topic, intro, main content, CTA ලෙස structure කරන්න.",
    "📚 Study Assistant":       "Study assistant mode — explain කිරීමට, MCQ හදන්නට, summary දෙන්නට ready. Subject කුමක්ද?",
    "✏️ Grammar Corrector":     "Grammar correction mode — සිංහල හෝ ඉංග්‍රීසි text paste කරන්න, corrected version + explanations දෙන්නම්.",
}

# ─────────────────────────────────────────────────────────────────────────────
# ░░  GROQ HELPER FUNCTIONS  ░░
# ─────────────────────────────────────────────────────────────────────────────

def get_groq_client(api_key: str):
    if st.session_state.groq_client is not None:
        return st.session_state.groq_client
    try:
        client = Groq(api_key=api_key)
        client.models.list()
        st.session_state.groq_client  = client
        st.session_state.api_key_valid = True
        return client
    except Exception:
        st.session_state.api_key_valid = False
        st.session_state.groq_client   = None
        return None


def pil_to_b64(image: Image.Image) -> str:
    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def build_messages(user_text: str, image: Image.Image | None) -> list:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in st.session_state.chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    if image:
        b64 = pil_to_b64(image)
        user_content = [
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
            {"type": "text", "text": user_text},
        ]
    else:
        user_content = user_text

    messages.append({"role": "user", "content": user_content})
    return messages


def generate_response(api_key: str, user_text: str, image: Image.Image | None = None) -> str:
    client = get_groq_client(api_key)
    if client is None:
        return "⚠️ Groq client initialise කරන්න බැරිවිය. API key check කරන්න."

    model    = MODEL_VISION if image else MODEL_TEXT
    messages = build_messages(user_text, image)

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.85,
        max_tokens=2048,
        top_p=0.95,
        stream=False,
    )
    return completion.choices[0].message.content


# ─────────────────────────────────────────────────────────────────────────────
# ░░  SIDEBAR  ░░
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:

    st.markdown("""
    <div style="text-align:center; padding:0.8rem 0 0.4rem;">
        <span style="font-family:'Syne',sans-serif; font-size:1.5rem; font-weight:800;
                     background:linear-gradient(135deg,#7C6FFF,#F0C060);
                     -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
            ✦ AURA AI
        </span>
        <div style="font-size:0.65rem; letter-spacing:0.16em; color:#55526A;
                    text-transform:uppercase; margin-top:2px;">
            Sri Lanka Edition
        </div>
        <div style="margin-top:6px;">
            <span style="background:rgba(240,192,96,0.12); border:1px solid rgba(240,192,96,0.3);
                         border-radius:20px; padding:2px 10px; font-size:0.6rem;
                         letter-spacing:0.1em; color:#F0C060; text-transform:uppercase;">
                ⚡ Powered by Groq
            </span>
        </div>
    </div>
    <hr style="margin:0.6rem 0;">
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">🔑 Groq API Key</div>', unsafe_allow_html=True)
    user_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Free key: console.groq.com",
        label_visibility="collapsed",
    )

    resolved_key = user_key.strip() or DEFAULT_API_KEY

    if resolved_key:
        _ = get_groq_client(resolved_key)
        if st.session_state.api_key_valid:
            st.success("✓ Groq Connected", icon="🟢")
        else:
            st.error("Invalid key. console.groq.com check කරන්න.", icon="🔴")
            st.session_state.groq_client = None
    else:
        st.caption("console.groq.com වලින් free key ගන්න.")

    st.markdown('<hr style="margin:0.8rem 0;">', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">🤖 Active Models</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.72rem; color:#9895B0; line-height:1.8; padding:0 0.2rem;">
        📝 Text &nbsp;&nbsp;→ <span style="color:#7C6FFF;">{MODEL_TEXT}</span><br>
        🖼️ Vision → <span style="color:#7C6FFF;">llama-4-scout-17b</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr style="margin:0.8rem 0;">', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">⚡ Quick Actions</div>', unsafe_allow_html=True)
    for label, prompt in QUICK_ACTIONS.items():
        st.markdown('<div class="quick-btn">', unsafe_allow_html=True)
        if st.button(label, key=f"qa_{label}"):
            st.session_state.quick_prompt = prompt
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr style="margin:0.8rem 0;">', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">🖼️ Vision — Image Upload</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Attach image",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
        help="Image upload කරලා ඒ ගැන AURA AI ට අහන්න.",
    )
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.session_state.uploaded_image = img
        st.image(img, use_container_width=True, caption="✓ Image attached")

    st.markdown('<hr style="margin:0.8rem 0;">', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">⚙️ Session</div>', unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history   = []
        st.session_state.groq_client    = None
        st.session_state.api_key_valid  = False
        st.session_state.uploaded_image = None
        st.session_state.quick_prompt   = None
        st.rerun()

    st.markdown('<div style="margin-top:1.5rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="ad-container">Ad Space · 300 × 50</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# ░░  MAIN CONTENT  ░░
# ─────────────────────────────────────────────────────────────────────────────

with st.container():
    st.markdown(
        '<div class="ad-container">📢 Ad Space · 320 × 50 — Integrate your ad SDK here</div>',
        unsafe_allow_html=True,
    )

st.markdown("""
<div class="aura-header">
    <div class="aura-title">✦ AURA AI</div>
    <div class="aura-tagline">ශ්‍රී ලංකාවේ ස්මාර්ට් AI සහකරු</div>
    <div style="margin-top:0.5rem;">
        <span class="groq-badge">⚡ Groq · LLaMA 3.3 70B · Ultra Fast</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ░░  CHAT RENDER  ░░
# ─────────────────────────────────────────────────────────────────────────────
chat_container = st.container()

def render_chat():
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown("""
            <div style="text-align:center; padding:2.5rem 1rem; color:#55526A;">
                <div style="font-size:2rem; margin-bottom:0.5rem;">✦</div>
                <div style="font-family:'Syne',sans-serif; font-size:0.95rem; color:#9895B0;">
                    ආයුබෝවන් ! AURA AI ට සාදරයෙන් පිළිගනිමු.
                </div>
                <div style="font-size:0.78rem; margin-top:0.4rem; color:#55526A;">
                    ඔබේ ප්‍රශ්නය type කරන්න, නැතිනම් sidebar Quick Actions use කරන්න.
                </div>
            </div>
            """, unsafe_allow_html=True)
            return

        for msg in st.session_state.chat_history:
            role    = msg["role"]
            text    = msg["content"]
            img_b64 = msg.get("image")

            if role == "user":
                avatar_html  = '<div class="avatar user">👤</div>'
                bubble_class = "user"
                row_class    = "user"
            else:
                avatar_html  = '<div class="avatar ai">✦</div>'
                bubble_class = "ai"
                row_class    = ""

            img_html = ""
            if img_b64 and role == "user":
                img_html = f'<img src="data:image/jpeg;base64,{img_b64}" alt="uploaded image"/>'

            safe_text = (
                text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            )

            st.markdown(f"""
            <div class="msg-row {row_class}">
                {avatar_html}
                <div class="bubble {bubble_class}">{img_html}{safe_text}</div>
            </div>
            """, unsafe_allow_html=True)

render_chat()

# ─────────────────────────────────────────────────────────────────────────────
# ░░  INPUT  ░░
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

col_input, col_send = st.columns([6, 1])

with col_input:
    default_val = st.session_state.quick_prompt or ""
    if st.session_state.quick_prompt:
        st.session_state.quick_prompt = None

    user_input = st.text_area(
        "Message AURA AI",
        value=default_val,
        placeholder="ඔබේ ප්‍රශ්නය ලියන්න... (Sinhala or English)",
        height=80,
        label_visibility="collapsed",
        key="user_text_area",
    )

with col_send:
    st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)
    send_clicked = st.button("Send ➤", use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# ░░  SEND LOGIC  ░░
# ─────────────────────────────────────────────────────────────────────────────
if send_clicked and user_input.strip():

    if not resolved_key:
        st.warning("⚠️ Groq API key එක sidebar හි enter කරන්න.")

    elif not st.session_state.api_key_valid:
        st.error("🔴 API key valid නෑ. console.groq.com check කරන්න.")

    else:
        prompt_text    = user_input.strip()
        attached_image = st.session_state.get("uploaded_image")

        img_b64_store = None
        if attached_image:
            img_b64_store = pil_to_b64(attached_image)

        st.session_state.chat_history.append({
            "role":    "user",
            "content": prompt_text,
            "image":   img_b64_store,
        })

        st.session_state.uploaded_image = None

        with st.spinner("AURA AI සිතමින් සිටී... ⚡"):
            try:
                response_text = generate_response(resolved_key, prompt_text, attached_image)
            except Exception as e:
                response_text = (
                    f"⚠️ Error: {str(e)}\n\n"
                    "Rate limit ඉවරවී ද? console.groq.com/dashboard check කරන්න."
                )

        st.session_state.chat_history.append({
            "role":    "assistant",
            "content": response_text,
            "image":   None,
        })

        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# ░░  BOTTOM AD + FOOTER  ░░
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

with st.container():
    st.markdown("""
    <div class="ad-container">
        📢 Ad Space · 320 × 50 Banner — Bottom — AdMob / Amazon Ads SDK integrate කරන්න
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:1rem 0 0.2rem;
            color:#55526A; font-size:0.68rem; letter-spacing:0.1em;">
    AURA AI v2.0 · Built for Sri Lanka · Powered by Groq ⚡ LLaMA 3.3 70B
</div>
""", unsafe_allow_html=True)