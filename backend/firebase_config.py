import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Get the key path from .env
firebase_path = os.getenv("FIREBASE_KEY_PATH")

# Resolve absolute path to the key file
KEY_PATH = os.path.abspath(firebase_path)
print("Resolved Firebase key path:", KEY_PATH)  # Optional debug

# Initialize Firebase Admin SDK (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate(KEY_PATH)
    firebase_admin.initialize_app(cred)

# Create Firestore client
db = firestore.client()
