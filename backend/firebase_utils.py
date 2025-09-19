from datetime import datetime, timedelta
from firebase_admin import firestore
from backend.firebase_config import db  # ✅ Ensure this import is correct

def update_streak(user_id):
    today = datetime.now().date()
    user_ref = db.collection("users").document(user_id)

    try:
        user_data = user_ref.get().to_dict() or {}
    except Exception as e:
        print(f"Firestore read error: {e}")
        user_data = {}

    last_date = user_data.get("last_entry_date")
    streak = user_data.get("streak_count", 0)

    try:
        if last_date:
            last_date = datetime.strptime(last_date, "%Y-%m-%d").date()
            if today == last_date + timedelta(days=1):
                streak += 1
            elif today != last_date:
                streak = 1
        else:
            streak = 1
    except Exception as e:
        print(f"Date parsing error: {e}")
        streak = 1

    try:
        user_ref.set({
            "last_entry_date": str(today),
            "streak_count": streak
        }, merge=True)
    except Exception as e:
        print(f"Firestore write error: {e}")

    return streak