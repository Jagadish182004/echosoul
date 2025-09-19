import os
import firebase_admin
from firebase_admin import credentials, firestore

# 🔐 Load secrets safely
project_id = os.getenv("FIREBASE_PROJECT_ID")
client_email = os.getenv("FIREBASE_CLIENT_EMAIL")
private_key_raw = os.getenv("FIREBASE_PRIVATE_KEY")

# 🚨 Fail fast if any secret is missing
if not all([project_id, client_email, private_key_raw]):
    raise ValueError("Missing Firebase credentials. Check your Streamlit secrets.")

# 🔧 Convert escaped newlines to actual newlines
private_key = private_key_raw.replace("\\n", "\n")

# 🔑 Build credential object
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": project_id,
    "private_key": private_key,
    "client_email": client_email,
    "token_uri": "https://oauth2.googleapis.com/token"
})

# 🚀 Initialize Firebase
firebase_admin.initialize_app(cred)
db = firestore.client()
