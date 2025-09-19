import streamlit as st
import sys
import os
from datetime import datetime

# Add backend path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.ai_services import analyze_mood, generate_affirmation_and_goal, generate_comfort_story
from backend.firebase_config import db
from backend.firebase_utils import update_streak

# Temporary user ID for testing (replace with Firebase Auth later)
user_id = "demo_user"

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
        .recipe-card {
            background-color: #1a1a1a;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 0 10px #FFD700;
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

def basic_mood_detector(text):
    text = text.lower()
    if "sad" in text or "lonely" in text:
        return "sad", "You seem down—take a moment to breathe."
    elif "happy" in text or "excited" in text:
        return "happy", "Glad you're feeling good!"
    elif "anxious" in text or "overwhelmed" in text or "worried" in text:
        return "anxious", "Try grounding yourself—you're doing great."
    elif "calm" in text or "peaceful" in text:
        return "calm", "Enjoy the serenity."
    elif "angry" in text or "frustrated" in text:
        return "angry", "Let it out—your feelings are valid."
    elif "grateful" in text or "thankful" in text:
        return "grateful", "Gratitude is powerful—keep it flowing."
    elif "hopeful" in text or "optimistic" in text:
        return "hopeful", "Hope is a strength—hold onto it."
    elif "reflective" in text or "thinking" in text:
        return "reflective", "Reflection brings clarity—keep exploring."
    else:
        return "unclear", "Couldn't detect mood clearly."

# 🍽️ Mood-to-Recipe mapping
MOOD_TO_RECIPES = {
    "happy": ["Fruit Salad", "Smoothie Bowl", "Grilled Veggies"],
    "sad": ["Mac & Cheese", "Chocolate Cake", "Tomato Soup"],
    "anxious": ["Banana Toast", "Oatmeal", "Green Tea"],
    "angry": ["Spicy Curry", "Chili Paneer", "Garlic Fries"],
    "calm": ["Herbal Tea", "Steamed Rice", "Miso Soup"],
    "grateful": ["Lemon Tart", "Stuffed Paratha", "Sweet Corn Salad"],
    "hopeful": ["Veggie Wrap", "Honey Lemon Drink", "Pasta Primavera"],
    "reflective": ["Khichdi", "Boiled Eggs", "Plain Toast"],
    "unclear": ["Rice Bowl", "Dal", "Chai"]
}

def run_journal():
    st.set_page_config(page_title="EchoSoul Journal", layout="centered")
    inject_bugatti_css()
    st.title("📝 EchoSoul Journal")
    st.subheader("Let your thoughts echo...")

    # Persona input
    persona_name = st.sidebar.text_input("🧑‍🎤 Name your journal persona:", value="EchoSoul", key="persona_input")

    MOOD_EMOJIS = {
        "happy": "😊", "sad": "😢", "anxious": "😟", "calm": "😌",
        "angry": "😠", "grateful": "🙏", "hopeful": "🌈", "reflective": "🧠",
        "excited": "🤩", "lonely": "😔", "unclear": "📝", "error": "⚠️"
    }

    user_input = st.text_area("Write your journal entry here:", height=200)
    engine_choice = st.radio("Choose mood analysis engine:", ["🔮 Gemini", "🧠 Fallback"], horizontal=True)

    if st.button("Analyze Mood"):
        if user_input.strip():
            with st.spinner("Analyzing your mood..."):
                mood, feedback = None, None
                if engine_choice == "🔮 Gemini":
                    try:
                        mood, feedback = analyze_mood(user_input)
                        if not mood or not feedback:
                            raise ValueError("Empty Gemini response")
                    except Exception:
                        st.warning("Gemini failed or quota exceeded. Try fallback mode.")
                        return
                else:
                    mood, feedback = basic_mood_detector(user_input)

                emoji = MOOD_EMOJIS.get(mood.lower(), "📝")
                st.markdown(f"<div class='glow-box'><h3>🧠 Mood: {emoji} {mood.capitalize()}</h3><p>🗣️ {persona_name} says: {feedback}</p></div>", unsafe_allow_html=True)

                # Save journal entry
                db.collection("journals").add({
                    "entry": user_input,
                    "mood": mood,
                    "feedback": feedback,
                    "engine": engine_choice,
                    "created_at": datetime.now()
                })

                # Update streak
                streak = update_streak(user_id)
                if streak >= 3:
                    st.markdown(f"""
                    <div style="text-align:center;">
                        <div style="display:inline-block; padding:20px; border-radius:50%; background:#FFD700; box-shadow:0 0 20px #FFD700; animation:pulse 2s infinite;">
                            <h2 style="color:black;">🔥 Streak: {streak} Days</h2>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # 🌟 Affirmation + Goal
                response = generate_affirmation_and_goal(user_input, persona_name)
                st.markdown(f"<div class='glow-box'><h3>🌟 Affirmation & Goal</h3><p>{response}</p></div>", unsafe_allow_html=True)

                # 🍽️ Mood-Based Recipe Suggestions
                st.markdown("<h3>🍽️ Suggested Recipes Based on Your Mood</h3>", unsafe_allow_html=True)
                recipes = MOOD_TO_RECIPES.get(mood.lower(), ["Rice Bowl", "Dal", "Chai"])
                for r in recipes:
                    st.markdown(f"<div class='recipe-card'>🍴 {r}</div>", unsafe_allow_html=True)

                # 📖 Comfort Food Story (Gemini)
                try:
                    story = generate_comfort_story(recipes[0], mood)
                    st.markdown(f"<div class='glow-box'><h3>📖 Comfort Food Story</h3><p>{story}</p></div>", unsafe_allow_html=True)
                except Exception:
                    st.warning("Could not generate story. Gemini may be unavailable.")
        else:
            st.warning("Please write something before analyzing.")