import streamlit as st
from groq import Groq
import os
from datetime import datetime

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TechGadget Guru AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Root variables ── */
:root {
    --bg-primary:    #0b0f1a;
    --bg-secondary:  #111827;
    --bg-card:       #1a2035;
    --accent-blue:   #3b82f6;
    --accent-cyan:   #06b6d4;
    --accent-purple: #8b5cf6;
    --accent-green:  #10b981;
    --text-primary:  #f1f5f9;
    --text-muted:    #94a3b8;
    --border:        rgba(59,130,246,.2);
    --glow:          0 0 30px rgba(59,130,246,.25);
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-secondary); }
::-webkit-scrollbar-thumb { background: var(--accent-blue); border-radius: 10px; }

/* ── Main container ── */
.main .block-container {
    padding: 1rem 2rem 3rem !important;
    max-width: 900px;
    margin: 0 auto;
}

/* ── Header ── */
.guru-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--glow);
}
.guru-header::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 30% 50%, rgba(59,130,246,.12) 0%, transparent 70%),
                radial-gradient(ellipse at 70% 50%, rgba(139,92,246,.10) 0%, transparent 70%);
    pointer-events: none;
}
.guru-header-inner { position: relative; z-index: 1; }
.guru-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #60a5fa, #a78bfa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 .3rem;
    letter-spacing: -0.5px;
}
.guru-subtitle {
    color: var(--text-muted);
    font-size: .95rem;
    margin: 0;
    font-weight: 400;
}
.guru-badge {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    background: rgba(16,185,129,.12);
    border: 1px solid rgba(16,185,129,.3);
    border-radius: 50px;
    padding: .25rem .8rem;
    font-size: .75rem;
    font-weight: 600;
    color: #34d399;
    margin-top: .8rem;
    letter-spacing: .5px;
}
.guru-badge::before { content: '●'; font-size: .5rem; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1.2rem !important;
}
.sidebar-section {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.1rem;
    margin-bottom: 1rem;
}
.sidebar-label {
    font-size: .7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--accent-cyan);
    margin-bottom: .7rem;
}
.quick-btn {
    background: rgba(59,130,246,.08);
    border: 1px solid rgba(59,130,246,.2);
    border-radius: 10px;
    padding: .55rem .8rem;
    margin-bottom: .5rem;
    font-size: .82rem;
    color: var(--text-primary);
    cursor: pointer;
    transition: all .2s;
    width: 100%;
    text-align: left;
    line-height: 1.4;
}
.quick-btn:hover {
    background: rgba(59,130,246,.18);
    border-color: var(--accent-blue);
    transform: translateX(3px);
}

/* ── Chat messages ── */
.chat-user-wrap {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1rem;
}
.chat-bot-wrap {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 1rem;
}
.chat-bubble-user {
    background: linear-gradient(135deg, #2563eb, #4f46e5);
    color: #fff;
    border-radius: 18px 18px 4px 18px;
    padding: .9rem 1.2rem;
    max-width: 75%;
    font-size: .92rem;
    line-height: 1.6;
    box-shadow: 0 4px 20px rgba(37,99,235,.35);
}
.chat-bubble-bot {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 18px 18px 18px 4px;
    padding: .9rem 1.2rem;
    max-width: 80%;
    font-size: .92rem;
    line-height: 1.7;
    color: var(--text-primary);
    box-shadow: 0 4px 20px rgba(0,0,0,.3);
}
.chat-avatar {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0;
    margin: 0 .6rem;
}
.avatar-bot { background: linear-gradient(135deg,#3b82f6,#8b5cf6); }
.avatar-user { background: linear-gradient(135deg,#10b981,#06b6d4); }
.chat-meta {
    font-size: .68rem;
    color: var(--text-muted);
    margin-top: .35rem;
    display: block;
}

/* ── Stat cards ── */
.stat-row {
    display: flex;
    gap: .8rem;
    margin-bottom: 1.2rem;
    flex-wrap: wrap;
}
.stat-card {
    flex: 1; min-width: 100px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: .8rem 1rem;
    text-align: center;
}
.stat-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    background: linear-gradient(90deg,#60a5fa,#a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stat-label {
    font-size: .7rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: .5px;
    margin-top: .2rem;
}

/* ── Category pills ── */
.category-chip {
    display: inline-block;
    background: rgba(59,130,246,.1);
    border: 1px solid rgba(59,130,246,.25);
    border-radius: 50px;
    padding: .2rem .7rem;
    font-size: .72rem;
    font-weight: 600;
    color: #93c5fd;
    margin: .2rem .15rem;
}

/* ── Input area ── */
.stTextInput > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    color: var(--text-primary) !important;
    font-size: .95rem !important;
    padding: .8rem 1.1rem !important;
    transition: border-color .2s !important;
}
.stTextInput > div > div input {
    color: var(--text-primary) !important;
    caret-color: var(--accent-blue) !important;
}
.stTextInput > div > div:focus-within {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,.15) !important;
}
.stTextInput label { color: var(--text-muted) !important; font-size: .82rem !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: .9rem !important;
    padding: .65rem 1.5rem !important;
    transition: all .2s !important;
    box-shadow: 0 4px 15px rgba(37,99,235,.3) !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(37,99,235,.45) !important;
}

/* ── Selectbox / Slider ── */
.stSelectbox > div > div, .stSlider > div {
    color: var(--text-primary) !important;
}
.stSelectbox label, .stSlider label {
    color: var(--text-muted) !important;
    font-size: .82rem !important;
}

/* ── Divider ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent-blue), transparent);
    margin: 1.2rem 0;
    opacity: .4;
}

/* ── Typing indicator ── */
.typing-indicator {
    display: flex; gap: 4px; align-items: center; padding: .5rem 0;
}
.typing-dot {
    width: 8px; height: 8px;
    background: var(--accent-blue);
    border-radius: 50%;
    animation: bounce .9s infinite;
}
.typing-dot:nth-child(2) { animation-delay: .15s; }
.typing-dot:nth-child(3) { animation-delay: .3s; }
@keyframes bounce {
    0%, 60%, 100% { transform: translateY(0); opacity: .6; }
    30%           { transform: translateY(-6px); opacity: 1; }
}

/* ── Welcome card ── */
.welcome-card {
    background: linear-gradient(135deg, #1e1b4b 0%, #0f2d4a 100%);
    border: 1px solid rgba(99,102,241,.3);
    border-radius: 18px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
}
.welcome-icon { font-size: 3rem; margin-bottom: .8rem; display: block; }
.welcome-title { font-family:'Space Grotesk',sans-serif; font-size:1.4rem; font-weight:700; margin-bottom:.5rem; }
.welcome-desc { color: var(--text-muted); font-size:.9rem; line-height:1.7; }
.feature-grid { display:flex; gap:.7rem; margin-top:1.2rem; flex-wrap:wrap; justify-content:center; }
.feature-item {
    background: rgba(255,255,255,.05);
    border-radius: 10px;
    padding: .5rem .9rem;
    font-size: .8rem;
    color: #c7d2fe;
    border: 1px solid rgba(99,102,241,.2);
}
</style>
""", unsafe_allow_html=True)

# ── API Configuration ─────────────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY") or (st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else None)
client = Groq(api_key=GROQ_API_KEY)

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are TechGadget Guru, an expert AI assistant specializing in consumer technology and gadgets.

Your areas of expertise include:
🔹 Smartphones, tablets, and wearables (phones, smartwatches, earbuds)
🔹 Laptops, desktops, and PC components (CPUs, GPUs, RAM, storage)
🔹 Smart home devices (speakers, displays, thermostats, security)
🔹 Audio/visual equipment (headphones, TVs, projectors, cameras)
🔹 Gaming hardware (consoles, controllers, gaming peripherals)
🔹 Networking gear (routers, mesh systems, switches)
🔹 Accessories and peripherals

Your personality:
- Knowledgeable, enthusiastic, and friendly
- Give clear, honest recommendations with pros and cons
- Cite real specs and prices when relevant
- Always ask clarifying questions about budget and use case when helpful
- Use emojis sparingly to enhance readability
- Keep responses concise but complete

STRICT DOMAIN RULE: If asked about anything outside consumer technology and gadgets, politely redirect:
"I'm specialized in consumer tech and gadgets! I'd love to help you with smartphones, laptops, headphones, smart home devices, or any other tech question. What gadget are you curious about? 🎯"

Response style:
- Use markdown formatting (bold, bullet points, tables) for clarity
- Structure longer answers with clear headers
- Always end with a helpful follow-up question or suggestion when appropriate
"""

# ── Session state initialization ──────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0
if "session_start" not in st.session_state:
    st.session_state.session_start = datetime.now()
if "model_name" not in st.session_state:
    st.session_state.model_name = "llama-3.3-70b-versatile"
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "quick_prompt" not in st.session_state:
    st.session_state.quick_prompt = None

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🤖 TechGadget Guru")
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Model settings
    st.markdown('<p class="sidebar-label">⚙️ MODEL SETTINGS</p>', unsafe_allow_html=True)

    model_options = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"]
    if st.session_state.model_name not in model_options:
        st.session_state.model_name = "llama-3.3-70b-versatile"
    model_choice = st.selectbox(
        "AI Model",
        model_options,
        index=model_options.index(st.session_state.model_name),
        key="model_select"
    )
    st.session_state.model_name = model_choice

    temperature = st.slider(
        "Creativity (Temperature)",
        min_value=0.0, max_value=1.0,
        value=st.session_state.temperature, step=0.05,
        help="Lower = more factual, Higher = more creative"
    )
    st.session_state.temperature = temperature

    # Categories
    st.markdown('<p class="sidebar-label" style="margin-top:1rem;">📱 CATEGORIES</p>', unsafe_allow_html=True)
    categories = ["📱 Smartphones", "💻 Laptops", "🎧 Audio", "🏠 Smart Home",
                   "🎮 Gaming", "📷 Cameras", "⌚ Wearables", "🖥️ PC Build"]
    cat_html = "".join(f'<span class="category-chip">{c}</span>' for c in categories)
    st.markdown(cat_html, unsafe_allow_html=True)

    # Quick prompts
    st.markdown('<p class="sidebar-label" style="margin-top:1rem;">⚡ QUICK PROMPTS</p>', unsafe_allow_html=True)
    quick_prompts = [
        "📱 Best smartphone under ₹30,000?",
        "💻 Recommend a laptop for video editing",
        "🎧 Top wireless earbuds in 2025?",
        "🏠 Smart home starter kit recommendations",
        "🎮 Best gaming headset under $100?",
        "📷 Which mirrorless camera for beginners?",
        "⌚ Apple Watch vs Samsung Galaxy Watch?",
        "🖥️ Build a gaming PC for $800",
    ]
    for qp in quick_prompts:
        if st.button(qp, key=f"qp_{qp[:10]}"):
            st.session_state.quick_prompt = qp

    # Stats
    elapsed = datetime.now() - st.session_state.session_start
    mins = int(elapsed.total_seconds() // 60)
    st.markdown('<p class="sidebar-label" style="margin-top:1rem;">📊 SESSION STATS</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-value">{st.session_state.total_queries}</div>
            <div class="stat-label">Queries</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{len(st.session_state.messages)}</div>
            <div class="stat-label">Messages</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{mins}m</div>
            <div class="stat-label">Session</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Clear button
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.session_state.total_queries = 0
        st.session_state.session_start = datetime.now()
        st.rerun()

# ── Main area ─────────────────────────────────────────────────────────────────

# Header
st.markdown("""
<div class="guru-header">
  <div class="guru-header-inner">
    <h1 class="guru-title">🔮 TechGadget Guru AI</h1>
    <p class="guru-subtitle">Your expert guide to all things consumer technology & gadgets</p>
    <span class="guru-badge">LIVE AI ASSISTANT</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Welcome screen (shown when no messages)
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <span class="welcome-icon">🤖</span>
        <div class="welcome-title">Welcome to TechGadget Guru!</div>
        <div class="welcome-desc">
            I'm your AI-powered gadget expert. Ask me about the latest smartphones, 
            laptops, headphones, smart home devices, gaming gear, and much more. 
            I'll give you honest, expert recommendations tailored to your needs.
        </div>
        <div class="feature-grid">
            <div class="feature-item">📱 Smartphone Reviews</div>
            <div class="feature-item">💻 Laptop Picks</div>
            <div class="feature-item">🎧 Audio Gear</div>
            <div class="feature-item">🎮 Gaming Setup</div>
            <div class="feature-item">🏠 Smart Home</div>
            <div class="feature-item">🛒 Best Value Buys</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Chat messages
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        ts = msg.get("timestamp", "")
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-user-wrap">
                <div>
                    <div class="chat-bubble-user">{msg["content"]}</div>
                    <span class="chat-meta" style="text-align:right;display:block;">{ts}</span>
                </div>
                <div class="chat-avatar avatar-user">👤</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-bot-wrap">
                <div class="chat-avatar avatar-bot">🤖</div>
                <div>
                    <div class="chat-bubble-bot">{msg["content"]}</div>
                    <span class="chat-meta">{ts}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# ── Input + send ──────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])
with col_input:
    user_input = st.text_input(
        "Ask about any gadget...",
        placeholder="e.g. What's the best budget phone in 2025? 📱",
        key="user_input",
        label_visibility="collapsed"
    )
with col_btn:
    send_clicked = st.button("Send 🚀", key="send_btn")

# Handle quick prompt injection
if st.session_state.quick_prompt:
    user_input = st.session_state.quick_prompt
    st.session_state.quick_prompt = None
    send_clicked = True

# ── Response generation ───────────────────────────────────────────────────────
def get_ai_response(user_msg: str) -> str:
    """Call Groq with conversation history."""
    # Build message list: system + history + new user message
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in st.session_state.messages:
        role = "user" if m["role"] == "user" else "assistant"
        messages.append({"role": role, "content": m["content"]})
    messages.append({"role": "user", "content": user_msg})

    response = client.chat.completions.create(
        model=st.session_state.model_name,
        messages=messages,
        temperature=st.session_state.temperature,
        top_p=0.85,
        max_tokens=1024,
    )
    return response.choices[0].message.content

# ── Process send ──────────────────────────────────────────────────────────────
if send_clicked and user_input.strip():
    now_str = datetime.now().strftime("%I:%M %p")

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input.strip(),
        "timestamp": now_str
    })
    st.session_state.total_queries += 1

    # Generate response with spinner
    with st.spinner(""):
        st.markdown("""
        <div class="chat-bot-wrap">
            <div class="chat-avatar avatar-bot">🤖</div>
            <div class="chat-bubble-bot">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        try:
            reply = get_ai_response(user_input.strip())
        except Exception as e:
            reply = f"⚠️ Error: {str(e)}\n\nPlease check your API key or try again."

    # Add bot response
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply,
        "timestamp": now_str
    })

    st.rerun()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<p style="text-align:center;color:#475569;font-size:.75rem;margin-top:2rem;">
    🔮 TechGadget Guru AI &nbsp;·&nbsp; Powered by Groq &nbsp;·&nbsp;
    INT428 Project &nbsp;·&nbsp; Built with Streamlit
</p>
""", unsafe_allow_html=True)
