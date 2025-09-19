import streamlit as st
import sys
import os
from datetime import datetime, timedelta

# Add backend path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.firebase_config import db
from firebase_admin import firestore

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
        .stMetric {
            background-color: #111111;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0 0 15px #FFD700;
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
    </style>
    """, unsafe_allow_html=True)

def run_reflection():
    st.set_page_config(page_title="EchoSoul Reflection", layout="centered")
    inject_bugatti_css()

    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1>🪞 Daily Reflection</h1>
            <p style='color: #AAAAAA;'>Capture your thoughts and track your emotional streak</p>
        </div>
    """, unsafe_allow_html=True)

    # ✍️ Input section
    prompt = st.text_area("What went well today?")
    mood = st.selectbox("How do you feel?", ["Happy", "Sad", "Anxious", "Calm", "Excited", "Reflective"])
    rating = st.slider("Rate your day", 1, 5)

    # 💾 Save to Firestore
    if st.button("Save Reflection"):
        if prompt.strip():
            db.collection("reflections").add({
                "text": prompt,
                "mood": mood.lower(),
                "rating": rating,
                "created_at": datetime.now()
            })
            st.success("Reflection saved!")
        else:
            st.warning("Please write something before saving.")

    # 🔥 Streak Tracker
    st.markdown("<hr style='border-top: 1px solid #FFD700;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#FFD700;'>🔥 Your Reflection Streak</h3>", unsafe_allow_html=True)

    try:
        reflections = db.collection("reflections").order_by("created_at", direction=firestore.Query.DESCENDING).stream()

        dates = []
        for doc in reflections:
            data = doc.to_dict()
            created_at = data.get("created_at")
            if created_at:
                dates.append(created_at.date())

        streak = 0
        today = datetime.now().date()
        for i in range(len(dates)):
            if dates[i] == today - timedelta(days=streak):
                streak += 1
            else:
                break

        st.markdown(f"""
        <div style="text-align:center;">
            <div style="display:inline-block; padding:20px; border-radius:50%; background:#FFD700; box-shadow:0 0 20px #FFD700; animation:pulse 2s infinite;">
                <h2 style="color:black;">🔥 Streak: {streak} Days</h2>
            </div>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error loading streak: {e}")