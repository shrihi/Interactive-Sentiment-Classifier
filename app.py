import streamlit as st
import requests
from pymongo import MongoClient
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from bson.objectid import ObjectId
import time
import base64

# -------------------------------
# Set Page Config (Only once at the top)
# -------------------------------
st.set_page_config(page_title="Interactive Sentiment CLassifier", layout="wide")

# -------------------------------
# MongoDB Connection
# -------------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["chat_sentiment_ai"]
collection = db["messages"]

# -------------------------------
# Streamlit UI Configuration
# -------------------------------
# Session State for Authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "welcome_message" not in st.session_state:
    st.session_state.welcome_message = ""

# -------------------------------
# Authentication Pages
# -------------------------------

import streamlit as st
import requests
import base64

import base64
import streamlit as st

def set_background(image_file):
    with open(image_file, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()

        page_bg_img = f"""
    <style>
    /* Set the background image */
    [data-testid="stApp"] {{
        background-image: url("data:image/webp;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* Center the content */
    .center-content {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 0vh; /* Reduced from 100vh */
        padding-top: 10px;
        padding-bottom: 10px;
    }}

    /* Style headings, labels, and text */
    h1, h4, label, p {{
        color: white;
        text-align: center;
    }}

    /* Style the Streamlit Form */
    div[data-testid="stForm"] {{
        background: rgba(0, 0, 0, 0.6); /* Slightly darker for better contrast */
        padding: 25px 20px;
        border-radius: 18px;
        width: 320px;
        max-width: 90%;
        margin: 0 auto;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.3);
        border: 2px solid white;
        backdrop-filter: blur(5px); /* Slight glass effect */
    }}

    /* Style the input boxes */
    .stTextInput>div>div>input, .stTextArea>div>textarea {{
        text-align: left;
        border-radius: 4px;
        padding: 10px;
        width: 100%;
        font-size: 16px;
    }}

    /* Style the submit button */
    .stButton>button {{
        width: 50%;
        margin-top: 20px;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 12px;
        border-radius: 25px;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }}
    .stButton>button:hover {{
        background-color: #45a049;
    }}

    /* Center radio buttons */
    .stRadio>div {{
        justify-content: center;
    }}
    </style>
    """
        st.markdown(page_bg_img, unsafe_allow_html=True)

def show_login_page():
    set_background("black.jpg")

    with st.container():
        st.markdown('<div class="center-content">', unsafe_allow_html=True)

        st.markdown("<h1>🔐 Welcome to Interactive Sentiment Classifier </h1>", unsafe_allow_html=True)
        st.markdown("<h4>Login or Create a New Account Below</h4>", unsafe_allow_html=True)

        if "auth_mode" not in st.session_state:
            st.session_state.auth_mode = "Login"

        mode = st.radio("", ["Login", "Sign Up"], 
                        index=0 if st.session_state.auth_mode == "Login" else 1, 
                        horizontal=True, 
                        label_visibility="collapsed")
        st.session_state.auth_mode = mode

        with st.form("auth_form", clear_on_submit=False):
            username = st.text_input("Username *", max_chars=30)

            email = None
            if st.session_state.auth_mode == "Sign Up":
                email = st.text_input("Email *", max_chars=50)

            password = st.text_input("Password *", type="password", max_chars=30)
            submitted = st.form_submit_button("Continue")

            if submitted:
                if not username or not password or (st.session_state.auth_mode == "Sign Up" and not email):
                    st.error("⚠️ Please fill all fields before continuing!")
                else:
                    if st.session_state.auth_mode == "Login":
                        response = requests.post("http://127.0.0.1:8000/login", json={"username": username, "password": password})
                        if response.status_code == 200:
                            st.session_state.authenticated = True
                            st.session_state.username = username
                            st.session_state.welcome_message = f"🎉 Welcome back, {username}!"
                            st.rerun()
                        else:
                            st.error("❌ Invalid username or password.")
                    elif st.session_state.auth_mode == "Sign Up":
                        response = requests.post("http://127.0.0.1:8000/register", json={"username": username, "password": password})
                        if response.status_code == 200:
                            st.session_state.authenticated = True
                            st.session_state.username = username
                            st.session_state.welcome_message = "✅ Account created successfully! Welcome!"
                            st.rerun()
                        else:
                            st.error(f"❌ {response.json().get('detail', 'Error creating account')}")

        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# Main App After Login
# -------------------------------
def show_main_app():
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.welcome_message = ""
        st.rerun()

    if st.session_state.welcome_message:
        st.success(st.session_state.welcome_message)
        st.session_state.welcome_message = ""

    tabs = ["Analyze", "History", "Graphs"]
    selected_tab = st.sidebar.radio("Select a Tab", tabs)

    # Analyze Tab
    if selected_tab == "Analyze":
        st.markdown("<h1 style='text-align: center;'>Interactive Sentiment Classifier</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Instantly analyze the emotional tone of your messages.</h3>", unsafe_allow_html=True)

        st.markdown("""<p style='text-align: center;'>
            Analyze the <b>sentiment</b> of your chat messages in real-time — whether it is <b>positive</b>, <b>negative</b>, or <b>neutral</b>.<br>
            Get immediate feedback and track your communication patterns.
            </p>""", unsafe_allow_html=True)

        user_input = st.text_area("Enter your message:", placeholder="Type your message here...", height=120)

        col1, col2 = st.columns(2)
        with col1:
            analyze_button = st.button("Analyze")

        if analyze_button and user_input:
            response = requests.post("http://127.0.0.1:8000/analyze/", json={"text": user_input, "username": st.session_state.username})
            if response.status_code == 200:
                sentiment_score = response.json()["sentiment"]

                st.subheader("Sentiment Score")
                st.write(f"**{sentiment_score:.2f}**")

                if sentiment_score > 0:
                    st.success("😊 Positive Sentiment")
                elif sentiment_score < 0:
                    st.error("😞 Negative Sentiment")
                else:
                    st.warning("😐 Neutral Sentiment")
            else:
                st.error("❌ Error connecting to backend.")
        elif analyze_button and not user_input:
            st.warning("⚠️ Please enter a message to analyze.")

    # History Tab
    elif selected_tab == "History":
        st.markdown("<h1 class='main-title'>Messages Archive</h1>", unsafe_allow_html=True)

        data = list(collection.find({"username": st.session_state.username}).sort("timestamp", -1))

        if data:
            st.markdown("""<style>.main-title { margin-bottom: 25px; text-align: center; }</style>""", unsafe_allow_html=True)

            cols = st.columns([4, 1.5, 1.5, 2, 1])
            headers = ["Message", "Sentiment Score", "Sentiment", "Timestamp", "Delete"]

            for col, header in zip(cols, headers):
                col.markdown(f"<div style='text-align:center; font-weight:bold;'>{header}</div>", unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)

            for item in data:
                sentiment_score = round(item.get("sentiment", 0), 2)
                sentiment_label = "😊 Positive" if sentiment_score > 0 else "😞 Negative" if sentiment_score < 0 else "😐 Neutral"
                timestamp = item.get("timestamp")
                timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S') if isinstance(timestamp, datetime) else "N/A"

                with st.container():
                    row = st.columns([4, 1.5, 1.5, 2, 1])

                    row[0].markdown(f"<div style='text-align:center;'>{item.get('text', '')}</div>", unsafe_allow_html=True)
                    row[1].markdown(f"<div style='text-align:center;'>{sentiment_score:.2f}</div>", unsafe_allow_html=True)
                    row[2].markdown(f"<div style='text-align:center;'>{sentiment_label}</div>", unsafe_allow_html=True)
                    row[3].markdown(f"<div style='text-align:center;'>{timestamp_str}</div>", unsafe_allow_html=True)

                    if row[4].button("🗑️", key=str(item["_id"])):
                        collection.delete_one({"_id": ObjectId(item["_id"])})
                        st.success("✅ Message deleted successfully!")
                        time.sleep(0.5)
                        st.rerun()

        else:
            st.info("No chat history found.")

    # Graphs Tab
    elif selected_tab == "Graphs":
        st.markdown("<h1 style='text-align: center;'>Sentiment Trends</h1>", unsafe_allow_html=True)

        data = list(collection.find({"username": st.session_state.username}).sort("timestamp", -1))

        if data:
            sentiments = [item.get("sentiment", 0) for item in data]
            timestamps = [item.get("timestamp") for item in data]

            sentiment_labels = ['Positive', 'Negative', 'Neutral']
            sentiment_counts = [
                len([s for s in sentiments if s > 0]),
                len([s for s in sentiments if s < 0]),
                len([s for s in sentiments if s == 0])
            ]

            fig_pie = px.pie(
                names=sentiment_labels,
                values=sentiment_counts,
                title="Sentiment Distribution",
                template="plotly_dark"
            )
            st.plotly_chart(fig_pie)
             # Detailed Description for Pie Chart
            st.markdown("""
            **Sentiment Distribution**:
            This pie chart provides an overview of the sentiment distribution in your chat messages. 
            - *Positive* sentiment: Indicates messages with a positive emotional tone, showing uplifting or favorable sentiment.
            - *Negative* sentiment: Reflects messages expressing dissatisfaction, concern, or other negative emotions.
            - *Neutral* sentiment: Represents messages with little to no emotional tone, where the communication is neutral or factual.

            This chart helps you easily assess the general mood of your conversations and track how frequently different sentiment types occur.
        """)


            sentiment_df = pd.DataFrame({"Timestamp": timestamps, "Sentiment": sentiments})
            sentiment_df["Timestamp"] = pd.to_datetime(sentiment_df["Timestamp"])

            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=sentiment_df["Timestamp"],
                y=sentiment_df["Sentiment"],
                mode='lines+markers',
                name='Sentiment'
            ))

            fig_line.update_layout(
                title="Sentiment Trend Over Time",
                xaxis_title="Time",
                yaxis_title="Sentiment Score",
                template="plotly_dark"
            )

            st.plotly_chart(fig_line)
            # Detailed Description for Line Graph
            st.markdown("""
            **Sentiment Trend Over Time**:
            This line graph visualizes the sentiment scores of your messages over time. 
            Each point on the graph corresponds to a message and its sentiment score at a given timestamp:
            - Positive sentiment is represented by a higher value (above 0).
            - Negative sentiment is shown by a lower value (below 0).
            - Neutral sentiment is represented around the 0 mark.

            By examining this trend, you can identify shifts in the emotional tone of your conversations over time. This can be useful for tracking changes in mood, identifying moments of conflict or positivity, and understanding how your interactions evolve.
        """)


        else:
            st.info("No data available for graphs.")

# -------------------------------
# App Flow Controller
# -------------------------------
if not st.session_state.authenticated:
    show_login_page()
else:
    show_main_app()
