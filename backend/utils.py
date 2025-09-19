def save_story_to_journal(user_id, mood, story_text):
    from backend.firebase_config import db
    from datetime import datetime
    entry = {
        "user_id": user_id,
        "mood": mood,
        "entry": story_text,
        "source": "story",
        "created_at": datetime.now()
    }
    db.collection("journals").add(entry)