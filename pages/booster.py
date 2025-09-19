import streamlit as st
import sys
import os
from backend.ai_services import generate_affirmation

# Add backend path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
        .affirmation-box {
            background: linear-gradient(145deg, #111111, #222222);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 0 20px #FFD700;
            margin-top: 20px;
            font-size: 18px;
            font-style: italic;
        }
        .mood-header {
            font-size: 24px;
            color: #FFD700;
            text-shadow: 0 0 10px #FFD700;
            font-weight: bold;
            margin-top: 30px;
            text-align: center;
        }
        .video-row {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            align-items: flex-start;
            margin-top: 20px;
        }
        .video-card {
            flex: 1 1 320px;
            max-width: 320px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 0 10px #FFD700;
            animation: fadeIn 0.8s ease-in-out;
        }
        .video-card:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px #FFD700;
        }
        .video-summary {
            flex: 1 1 300px;
            font-size: 16px;
            color: #DDDDDD;
            font-style: italic;
            line-height: 1.6;
            padding: 10px;
            border-left: 2px solid #FFD700;
            animation: fadeInText 1s ease-in-out;
        }
        iframe {
            border: none;
            border-radius: 12px;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeInText {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @media screen and (max-width: 768px) {
            .video-row {
                flex-direction: column;
            }
            .video-summary {
                padding: 0;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# 🎥 Mood-based video sets with summaries
MOOD_VIDEOS = {
    "Happy": [
        {
            "url": "https://www.youtube.com/embed/1ZYbU82GVz4",
            "summary": "Gentle piano and ambient tones to elevate your joy and help you unwind."
        },
        {
            "url": "https://www.youtube.com/embed/2OEL4P1Rz04",
            "summary": "A scenic nature walk paired with uplifting music to refresh your spirit."
        },
        {
            "url": "https://www.youtube.com/embed/5yx6BWlEVcY",
            "summary": "Chillhop beats and jazzy rhythms to keep your vibe light and playful."
        }
    ],
    "Sad": [
        {
            "url": "https://www.youtube.com/embed/ZToicYcHIOU",
            "summary": "Guided meditation to help you breathe through sadness and find calm."
        },
        {
            "url": "https://www.youtube.com/embed/O-6f5wQXSu8",
            "summary": "Breathing exercises designed to ground you and ease emotional tension."
        },
        {
            "url": "https://www.youtube.com/embed/4pLUleLdwY4",
            "summary": "Healing frequencies and soft visuals to comfort your heart."
        }
    ],
    "Anxious": [
        {
            "url": "https://www.youtube.com/embed/MIr3RsUWrdo",
            "summary": "Soothing affirmations and visuals to calm racing thoughts."
        },
        {
            "url": "https://www.youtube.com/embed/1vx8iUvfyCY",
            "summary": "Deep sleep music to help you relax and reset your nervous system."
        },
        {
            "url": "https://www.youtube.com/embed/92i5m4tV5SY",
            "summary": "Peaceful tones and breathing guidance to reduce anxiety."
        }
    ],
    "Calm": [
        {
            "url": "https://www.youtube.com/embed/1Ai7nGxT2xE",
            "summary": "Ocean waves and ambient music to deepen your sense of peace."
        },
        {
            "url": "https://www.youtube.com/embed/2OEL4P1Rz04",
            "summary": "A tranquil nature walk with soft melodies to soothe your senses."
        },
        {
            "url": "https://www.youtube.com/embed/1ZYbU82GVz4",
            "summary": "Relaxing music and visuals to help you sleep peacefully."
        }
    ],
    "Excited": [
        {
            "url": "https://www.youtube.com/embed/2Vv-BfVoq4g",
            "summary": "Motivational music to amplify your energy and drive."
        },
        {
            "url": "https://www.youtube.com/embed/3AtDnEC4zak",
            "summary": "High-energy beats to keep your momentum flowing."
        },
        {
            "url": "https://www.youtube.com/embed/OPf0YbXqDm0",
            "summary": "Dance vibes and vibrant visuals to celebrate your excitement."
        }
    ],
    "Reflective": [
        {
            "url": "https://www.youtube.com/embed/4YgkYZZrguA",
            "summary": "Thoughtful piano melodies to support introspection and clarity."
        },
        {
            "url": "https://www.youtube.com/embed/1Ai7nGxT2xE",
            "summary": "Nature scenes and ambient music to guide your reflection."
        },
        {
            "url": "https://www.youtube.com/embed/1vx8iUvfyCY",
            "summary": "Deep sleep tones to help you process and reset."
        }
    ]
}

def run_booster():
    st.set_page_config(page_title="EchoSoul Booster", layout="centered")
    inject_bugatti_css()

    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1>🎯 Mood Booster</h1>
            <p style='color: #AAAAAA;'>Choose your mood and let EchoSoul lift you up</p>
        </div>
    """, unsafe_allow_html=True)

    mood = st.selectbox("Pick your mood:", list(MOOD_VIDEOS.keys()))

    if st.button("Get Affirmation"):
        with st.spinner("Generating affirmation..."):
            affirmation = generate_affirmation(mood)
        st.markdown(f"<div class='affirmation-box'>💬 {affirmation}</div>", unsafe_allow_html=True)

    st.markdown("<div class='mood-header'>🎵 Here's something to lift your mood:</div>", unsafe_allow_html=True)

    for video in MOOD_VIDEOS[mood]:
        st.markdown("<div class='video-row'>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='video-card'>
            <iframe width="320" height="180" src="{video['url']}" allowfullscreen></iframe>
        </div>
        <div class='video-summary'>{video['summary']}</div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)