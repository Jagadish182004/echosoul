import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
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

def run_dashboard():
    st.set_page_config(page_title="EchoSoul Dashboard", layout="wide")
    inject_bugatti_css()

    # 🌈 Styled Title
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: #FFD700;'>📊 EchoSoul Mood Dashboard</h1>
            <p style='color: #AAAAAA;'>Track your emotional journey with vibrant insights</p>
        </div>
    """, unsafe_allow_html=True)

    MOOD_SCORES = {
        "happy": 5, "excited": 4, "grateful": 3, "hopeful": 2,
        "calm": 1, "reflective": 0, "unclear": 0,
        "anxious": -1, "sad": -2, "lonely": -3, "angry": -4, "error": 0
    }

    MOOD_COLORS = {
        "happy": "#FFD700", "excited": "#FF8C00", "grateful": "#32CD32", "hopeful": "#00CED1",
        "calm": "#87CEFA", "reflective": "#A9A9A9", "unclear": "#D3D3D3",
        "anxious": "#FF6347", "sad": "#4682B4", "lonely": "#6A5ACD", "angry": "#DC143C", "error": "#808080"
    }

    with st.spinner("🎨 Loading your mood data..."):
        entries = db.collection("journals")\
            .order_by("created_at", direction=firestore.Query.DESCENDING)\
            .limit(200).stream()

        data = []
        for doc in entries:
            d = doc.to_dict()
            if "mood" in d and "created_at" in d:
                data.append({
                    "datetime": d["created_at"],
                    "date": d["created_at"].date(),
                    "mood": d["mood"].lower()
                })

    if not data:
        st.warning("No journal entries found yet.")
        return

    df = pd.DataFrame(data)
    df["score"] = df["mood"].map(MOOD_SCORES)
    df["color"] = df["mood"].map(MOOD_COLORS)
    df["formatted_date"] = df["datetime"].dt.strftime("%b %d, %Y")

    # 🍰 Pie Chart: Mood Distribution
    st.markdown("<h3 style='color:#FF8C00;'>🍰 Mood Distribution</h3>", unsafe_allow_html=True)
    mood_counts = df["mood"].value_counts().reset_index()
    mood_counts.columns = ["Mood", "Count"]
    fig1 = px.pie(mood_counts, names="Mood", values="Count", title="Mood Distribution",
                  color="Mood", color_discrete_map=MOOD_COLORS,
                  hole=0.3)
    fig1.update_traces(textinfo='percent+label', pull=[0.05]*len(mood_counts))
    fig1.update_layout(paper_bgcolor="black", font=dict(color="white"))
    st.plotly_chart(fig1, use_container_width=True)

    # 📈 Line Chart: Mood Score Over Time
    st.markdown("<h3 style='color:#1E90FF;'>📈 Mood Score Over Time</h3>", unsafe_allow_html=True)
    mood_trend = df.groupby("formatted_date")["score"].mean().reset_index()

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=mood_trend["formatted_date"],
        y=mood_trend["score"],
        mode="lines+markers",
        line=dict(color="#1E90FF", width=4),
        marker=dict(size=10, symbol="circle", color="#1E90FF"),
        hovertemplate="<b>Date:</b> %{x}<br><b>Avg Mood Score:</b> %{y:.2f}<extra></extra>"
    ))

    fig2.update_layout(
        title="Mood Score Over Time",
        xaxis_title="Date",
        yaxis_title="Mood Score",
        xaxis=dict(showgrid=True, tickangle=0),
        yaxis=dict(showgrid=True, zeroline=True),
        font=dict(color="yellow", size=16),
        plot_bgcolor="#e6f2ff",
        paper_bgcolor="black",
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig2, use_container_width=True)