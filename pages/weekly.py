import streamlit as st
import sys
import os
from datetime import datetime, timedelta
from collections import Counter
import random
import concurrent.futures

# Add backend path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.firebase_config import db
from backend.ai_services import generate_content
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
        .story-box {
            background: linear-gradient(145deg, #111111, #222222);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 0 20px #FFD700;
            margin-bottom: 20px;
            font-style: italic;
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

# Local stories for each emotion
EMOTION_STORIES = {
    "happy": [
        "She danced barefoot in the rain, laughing like the sky was hers.",
        "He watched the sunrise with coffee and peace in his heart.",
        "They reunited after years, and the hug felt like home."
    ],
    "sad": [
        "She deleted the photos but couldn’t erase the memories.",
        "He smiled in the group photo, but felt alone inside.",
        "Her voice cracked as she said goodbye for the last time."
    ],
    "anxious": [
        "She rehearsed her lines, palms sweating, mind spinning.",
        "He refreshed his inbox, waiting for the job reply.",
        "The silence before the results felt louder than thunder."
    ],
    "calm": [
        "She painted for hours, lost in the rhythm of color.",
        "The waves whispered peace as he walked the shore.",
        "He journaled slowly, each word grounding his soul."
    ],
    "excited": [
        "She jumped when the email said: 'You’re selected!'",
        "He packed his bags—tomorrow, the adventure begins.",
        "She couldn’t sleep, imagining the stage lights on her."
    ],
    "reflective": [
        "She reread her old diary, amazed at her growth.",
        "He forgave himself for the choices that shaped him.",
        "She whispered thanks to the past for teaching her strength."
    ]
}

# Helper to save story to journal
def save_story_to_journal(user_id, mood, story_text):
    entry = {
        "user_id": user_id,
        "mood": mood,
        "entry": story_text,
        "source": "story",
        "created_at": datetime.now()
    }
    db.collection("journals").add(entry)

def run_weekly_summary():
    st.set_page_config(page_title="EchoSoul Weekly", layout="centered")
    inject_bugatti_css()

    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1>🧠 Weekly Mood Summary</h1>
            <p style='color: #AAAAAA;'>Reflect on your emotional journey and save stories that resonate</p>
        </div>
    """, unsafe_allow_html=True)

    one_week_ago = datetime.now() - timedelta(days=7)

    try:
        journal_docs = db.collection("journals")\
            .where("created_at", ">", one_week_ago)\
            .select(["mood"])\
            .order_by("created_at", direction=firestore.Query.DESCENDING)\
            .limit(20).stream()

        reflection_docs = db.collection("reflections")\
            .where("created_at", ">", one_week_ago)\
            .select(["mood", "rating"])\
            .order_by("created_at", direction=firestore.Query.DESCENDING)\
            .limit(20).stream()

        journal_moods = [doc.to_dict().get("mood", "unknown") for doc in journal_docs]
        reflection_data = [doc.to_dict() for doc in reflection_docs]
        reflection_moods = [r.get("mood", "unknown") for r in reflection_data]
        reflection_ratings = [r.get("rating", 0) for r in reflection_data if isinstance(r.get("rating", 0), (int, float))]

        all_moods = journal_moods + reflection_moods

        if not all_moods:
            st.info("No entries found for this week.")
            return

        mood_counts = Counter(all_moods)
        dominant_mood = mood_counts.most_common(1)[0][0]
        avg_rating = round(sum(reflection_ratings) / len(reflection_ratings), 2) if reflection_ratings else "N/A"

        st.markdown(f"<div class='story-box'>🧠 Dominant Mood: <b>{dominant_mood.capitalize()}</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='story-box'>📊 Average Day Rating: <b>{avg_rating}</b></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#FFD700;'>🗂️ Mood Distribution:</h3>", unsafe_allow_html=True)
        for mood, count in mood_counts.items():
            st.markdown(f"- {mood.capitalize()}: {count}")

        # 🎭 Emotion Story Section
        st.markdown("<hr style='border-top: 1px solid #FFD700;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#FFD700;'>🎭 Emotion Stories</h3>", unsafe_allow_html=True)

        for mood in EMOTION_STORIES:
            with st.expander(f"📖 {mood.capitalize()} Story"):
                col1, col2 = st.columns([1, 1])

                with col1:
                    if st.button(f"✨ Gemini Story", key=f"{mood}_gemini"):
                        try:
                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                future = executor.submit(generate_content, f"Write a 5-line emotional story that captures the feeling of being {mood}.")
                                story = future.result(timeout=4)
                            st.markdown(f"<div class='story-box'>✨ {story}</div>", unsafe_allow_html=True)
                            if st.button(f"💾 Save to Journal", key=f"{mood}_gemini_save"):
                                save_story_to_journal("demo_user", mood, story)
                                st.success("Story saved to journal!")
                        except Exception:
                            st.error("⚠️ Gemini failed to generate a story.")

                with col2:
                    if st.button(f"📚 Local Story", key=f"{mood}_local"):
                        story = random.choice(EMOTION_STORIES[mood])
                        st.markdown(f"<div class='story-box'>📚 {story}</div>", unsafe_allow_html=True)
                        if st.button(f"💾 Save to Journal", key=f"{mood}_local_save"):
                            save_story_to_journal("demo_user", mood, story)
                            st.success("Story saved to journal!")

    except Exception as e:
        st.error(f"Error loading weekly summary: {e}")