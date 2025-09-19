import streamlit as st
import sys
import os

# Add backend path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import page modules
from frontend.journal import run_journal
from pages.history import run_history
from frontend.dashboard import run_dashboard
from pages.reflection import run_reflection
from pages.booster import run_booster
from pages.weekly import run_weekly_summary
from pages.mood_dashboard import run_mood_dashboard  # ✅ Include this

# 🔥 Inject Bugatti-grade CSS
def inject_bugatti_css():
    st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
        }
        h1, h2, h3 {
            color: #FFD700;
            text-shadow: 0 0 10px #FFD700;
        }
        .stButton>button {
            background-color: #FFD700;
            color: black;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
            transition: 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #ffffff;
            color: #000000;
            box-shadow: 0 0 10px #FFD700;
        }
        .glow-box {
            background: linear-gradient(145deg, #111111, #222222);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 0 20px #FFD700;
            margin-bottom: 20px;
        }
        .reflection {
            transform: scaleY(-1);
            opacity: 0.2;
            filter: blur(2px);
        }
        @keyframes pulse {
            0% { transform: scale(1); box-shadow: 0 0 10px #FFD700; }
            50% { transform: scale(1.1); box-shadow: 0 0 30px #FFD700; }
            100% { transform: scale(1); box-shadow: 0 0 10px #FFD700; }
        }
        @media screen and (max-width: 768px) {
            h1, h2, h3 {
                font-size: 1.5rem;
            }
            .stButton>button {
                padding: 8px 16px;
            }
        }
        /* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(145deg, #0a0a0a, #1a1a1a);
    border-right: 2px solid #FFD700;
    box-shadow: 0 0 20px #FFD700;
    padding-top: 20px;
}

/* Sidebar Title */
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2 {
    color: #FFD700;
    text-shadow: 0 0 10px #FFD700;
}

/* Sidebar Radio Buttons */
div[data-testid="stSidebarNav"] label {
    color: #ffffff !important;
    font-weight: bold;
    padding: 8px 12px;
    border-radius: 8px;
    transition: all 0.3s ease;
    display: block;
}

div[data-testid="stSidebarNav"] label:hover {
    background-color: #FFD700;
    color: #000000 !important;
    box-shadow: 0 0 10px #FFD700;
    transform: translateX(5px);
}

/* Selected Option Glow */
div[data-testid="stSidebarNav"] input:checked + div label {
    background-color: #FFD700;
    color: #000000 !important;
    box-shadow: 0 0 15px #FFD700;
    transform: scale(1.05);
}

/* Sidebar Icons (if using emojis) */
div[data-testid="stSidebarNav"] label::before {
    content: "⚡ ";
    color: #FFD700;
    margin-right: 5px;
    transition: transform 0.3s ease;
}

div[data-testid="stSidebarNav"] label:hover::before {
    transform: rotate(20deg);
}        
    </style>
    """, unsafe_allow_html=True)

# 🚀 Page setup
st.sidebar.markdown("#### 🔖 jagadishsprojects")
st.set_page_config(page_title="EchoSoul", layout="wide")
inject_bugatti_css()  # Inject elite styling
st.sidebar.title("🧭 EchoSoul Navigation")

# 🎞️ Optional Hero Section (can move to index/dashboard)
st.markdown("""
<div style="text-align:center; padding:40px;">
    <h1 style="color:#FFD700; text-shadow:0 0 20px #FFD700;">⚡ EchoSoul</h1>
    <p style="font-size:20px;">Your emotional wellness companion, now with Bugatti-grade elegance.</p>
</div>
""", unsafe_allow_html=True)

# 🧭 Navigation
page = st.sidebar.radio("Go to:", [
    "📝 Journal",
    "📜 History",
    "📊 Dashboard",
    "🪞 Reflection",
    "🎯 Booster",
    "🧠 Weekly Summary",
    "📊 Mood Dashboard"
])

# 🔀 Page routing
if page == "📝 Journal":
    run_journal()
elif page == "📜 History":
    run_history()
elif page == "📊 Dashboard":
    run_dashboard()
elif page == "🪞 Reflection":
    run_reflection()
elif page == "🎯 Booster":
    run_booster()
elif page == "🧠 Weekly Summary":
    run_weekly_summary()
elif page == "📊 Mood Dashboard":
    run_mood_dashboard()
