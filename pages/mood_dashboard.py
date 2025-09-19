import streamlit as st
import sys
import os
from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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
        .chart-box {
            background: linear-gradient(145deg, #111111, #222222);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 0 20px #FFD700;
            margin-bottom: 30px;
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

def run_mood_dashboard():
    st.set_page_config(page_title="Mood Dashboard", layout="centered")
    inject_bugatti_css()

    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1>📊 Mood Frequency Dashboard</h1>
            <p style='color: #AAAAAA;'>Visualize your emotional patterns over the past week</p>
        </div>
    """, unsafe_allow_html=True)

    one_week_ago = datetime.now() - timedelta(days=7)

    try:
        journal_docs = db.collection("journals")\
            .where("created_at", ">", one_week_ago)\
            .select(["mood", "created_at"])\
            .order_by("created_at", direction=firestore.Query.DESCENDING)\
            .limit(100).stream()

        reflection_docs = db.collection("reflections")\
            .where("created_at", ">", one_week_ago)\
            .select(["mood", "created_at"])\
            .order_by("created_at", direction=firestore.Query.DESCENDING)\
            .limit(100).stream()

        mood_data = defaultdict(int)
        mood_by_day = defaultdict(lambda: defaultdict(int))

        for doc in journal_docs:
            d = doc.to_dict()
            mood = d.get("mood", "unknown")
            created_at = d.get("created_at")
            if created_at:
                date = created_at.date()
                mood_data[mood] += 1
                mood_by_day[date][mood] += 1

        for doc in reflection_docs:
            r = doc.to_dict()
            mood = r.get("mood", "unknown")
            created_at = r.get("created_at")
            if created_at:
                date = created_at.date()
                mood_data[mood] += 1
                mood_by_day[date][mood] += 1

        if not mood_data:
            st.info("No mood data found for the past week.")
            return

        # 📊 Bar Chart (Fixed for dark mode)
        st.markdown("<div class='chart-box'><h3>🧠 Mood Frequency (Last 7 Days)</h3></div>", unsafe_allow_html=True)
        mood_df = pd.DataFrame(mood_data.items(), columns=["Mood", "Count"]).sort_values(by="Count", ascending=False)

        fig, ax = plt.subplots(figsize=(8, 5), facecolor="#000000")
        ax.bar(mood_df["Mood"], mood_df["Count"], color="#FFD700")
        ax.set_facecolor("#000000")
        fig.patch.set_facecolor("#000000")
        ax.set_title("Mood Frequency (Last 7 Days)", color="white")
        ax.set_xlabel("Mood", color="white")
        ax.set_ylabel("Frequency", color="white")
        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_color("white")
        st.pyplot(fig)

        # 📈 Line Chart
        st.markdown("<div class='chart-box'><h3>📈 Mood Trends by Day</h3></div>", unsafe_allow_html=True)
        trend_df = pd.DataFrame(mood_by_day).fillna(0).astype(int).T.sort_index()

        mood_colors = {
            "angry": "#1E90FF",
            "happy": "#32CD32",
            "sad": "#FF0000",
            "neutral": "#800080",
            "frustrated": "#808080"
        }

        fig2 = go.Figure()
        for mood in trend_df.columns:
            fig2.add_trace(go.Scatter(
                x=trend_df.index,
                y=trend_df[mood],
                mode="lines+markers",
                name=mood,
                line=dict(color=mood_colors.get(mood, "#FFD700"), width=3),
                marker=dict(size=8, color=mood_colors.get(mood, "#FFD700")),
                hovertemplate=f"<b>{mood}</b><br>Date: %{{x}}<br>Count: %{{y}}<extra></extra>"
            ))

        fig2.update_layout(
            title="Mood Trends by Day",
            xaxis_title="Date",
            yaxis_title="Count",
            font=dict(color="white", size=14),
            plot_bgcolor="#111111",
            paper_bgcolor="black",
            margin=dict(l=40, r=40, t=60, b=40),
            legend=dict(
                bgcolor="#222222",
                bordercolor="#FFD700",
                borderwidth=1
            )
        )

        st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading mood dashboard: {e}")