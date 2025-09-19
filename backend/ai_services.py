import os
import uuid
from dotenv import load_dotenv
import google.generativeai as genai
from backend.firebase_config import db
from firebase_admin import firestore

# 🌍 Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 🔮 Gemini wrapper
def generate_content(prompt, model_name="gemini-1.5-flash"):
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini error: {e}")
        return None  # Return None so caller can handle fallback

# 🧠 Mood analysis from journal entry
def analyze_mood(text):
    if len(text.strip()) < 10:
        return "unclear", "Please write a bit more so I can understand your mood better."

    prompt = f"""Analyze this journal entry and respond with:
Mood: <label only, no numbering>
Feedback: <one helpful sentence only, no numbering or prefix>

Entry:
{text}
"""

    try:
        output = generate_content(prompt)
        mood = "unknown"
        feedback = "no feedback provided."

        if output:
            for line in output.split("\n"):
                if line.lower().startswith("mood:"):
                    mood = line.split(":", 1)[1].strip().lower()
                elif line.lower().startswith("feedback:"):
                    feedback = line.split(":", 1)[1].strip()
                    feedback = feedback.lstrip("1234567890.:- ").strip()

        entry_id = str(uuid.uuid4())
        db.collection("journals").document(entry_id).set({
            "id": entry_id,
            "entry": text,
            "mood": mood,
            "feedback": feedback,
            "created_at": firestore.SERVER_TIMESTAMP
        })

        return mood, feedback

    except Exception as e:
        print(f"Error during mood analysis: {e}")
        return "error", "Could not analyze mood due to an internal issue."

# 🎯 Affirmation generator for booster page
def generate_affirmation(mood):
    prompt = f"Give a one-sentence affirmation for someone feeling {mood}."
    return generate_content(prompt) or "You're doing your best—keep going."

# 🌟 Affirmation + Goal generator for journal page
def generate_affirmation_and_goal(entry, persona_name):
    prompt = (
        f"Based on this journal entry: '{entry}', generate a personalized affirmation "
        f"and one weekly goal for the user named {persona_name}. Format the response as:\n"
        f"'Affirmation: ...'\n'Weekly Goal: ...'"
    )
    response = generate_content(prompt)
    return response or "Affirmation: You're doing great.\nWeekly Goal: Stay consistent and reflect daily."

# 📖 Comfort Food Story generator for RecipeRadar
def generate_comfort_story(recipe_name, mood):
    prompt = (
        f"Write a short, cozy story about someone feeling {mood} and making {recipe_name} to feel better. "
        f"Make it warm, personal, and emotionally uplifting."
    )
    return generate_content(prompt) or f"Someone feeling {mood} found comfort in making {recipe_name}—a simple joy that lifted their spirits."