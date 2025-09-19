import streamlit as st
import sys
import os

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
            padding: 8px 16px;
            font-weight: bold;
            transition: 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #ffffff;
            color: #000000;
            box-shadow: 0 0 10px #FFD700;
        }
        .entry-card {
            background: linear-gradient(145deg, #111111, #222222);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 0 20px #FFD700;
            margin-bottom: 20px;
        }
        .entry-card:hover {
            box-shadow: 0 0 30px #FFD700;
        }
        .entry-header {
            font-size: 18px;
            font-weight: bold;
            color: #FFD700;
        }
        .entry-text {
            font-size: 16px;
            color: #DDDDDD;
        }
        .entry-caption {
            font-size: 14px;
            color: #AAAAAA;
        }
        @media screen and (max-width: 768px) {
            h1 {
                font-size: 1.5rem;
            }
            .entry-card {
                padding: 15px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def run_history():
    st.set_page_config(page_title="EchoSoul History", layout="centered")
    inject_bugatti_css()

    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1>📜 EchoSoul Journal History</h1>
            <p style='color: #AAAAAA;'>Browse your emotional reflections with style</p>
        </div>
    """, unsafe_allow_html=True)

    MOOD_EMOJIS = {
        "happy": "😊", "sad": "😢", "anxious": "😟", "calm": "😌",
        "angry": "😠", "grateful": "🙏", "hopeful": "🌈", "reflective": "🧠",
        "excited": "🤩", "lonely": "😔", "unclear": "📝", "error": "⚠️"
    }

    selected_mood = st.selectbox("Filter by mood:", [
        "All", "Happy", "Sad", "Anxious", "Calm", "Angry", "Grateful",
        "Hopeful", "Reflective", "Excited", "Lonely"
    ])
    search_term = st.text_input("Search by keyword:")

    found_entries = False

    with st.spinner("Loading your entries..."):
        try:
            entries = db.collection("journals").order_by("created_at", direction=firestore.Query.DESCENDING).stream()

            for doc in entries:
                data = doc.to_dict()
                doc_id = doc.id
                mood = data.get("mood", "unknown").lower()
                entry_text = data.get("entry", "").lower()

                if selected_mood != "All" and mood != selected_mood.lower():
                    continue
                if search_term and search_term.lower() not in entry_text:
                    continue

                found_entries = True
                emoji = MOOD_EMOJIS.get(mood, "📝")
                timestamp = data.get("created_at")
                feedback = data.get("feedback", "").lstrip("1234567890.:- ").strip()
                entry = data.get("entry", "")

                st.markdown(f"""
                <div class="entry-card">
                    <div class="entry-header">🧠 Mood: {emoji} {mood.capitalize()}</div>
                    <div class="entry-text">🗣️ Feedback: {feedback}</div>
                    <div class="entry-text">📝 Entry: {entry}</div>
                    <div class="entry-caption">🕒 {timestamp.strftime('%d %b %Y, %I:%M %p') if timestamp else ''}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"🗑️ Delete Entry", key=doc_id):
                    db.collection("journals").document(doc_id).delete()
                    st.success("Entry deleted. Please refresh to update view.")

            if not found_entries:
                st.info("📝 No journal entries found. Try adjusting your filters or start journaling!")

        except Exception as e:
            st.error("⚠️ Failed to load journal entries. Please check your Firebase setup.")
            st.text(str(e))  # Optional: remove after debugging
