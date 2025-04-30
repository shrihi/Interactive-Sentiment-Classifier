# frontend/authentication.py

import streamlit as st
import requests

# URL where your FastAPI backend is running
API_URL = "http://localhost:8000"

def register_user(username: str, password: str) -> bool:
    """Registers a new user by calling the FastAPI backend."""
    if not username or not password:
        st.warning("Username and Password cannot be empty!")
        return False

    payload = {"username": username, "password": password}
    try:
        response = requests.post(f"{API_URL}/register", json=payload)
        if response.status_code == 200:
            st.success("Registration successful! You can now log in.")
            return True
        else:
            st.error(f"Registration failed: {response.json().get('detail', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"Failed to connect to server: {e}")
        return False

def login_user(username: str, password: str) -> bool:
    """Logs in a user by calling the FastAPI backend."""
    if not username or not password:
        st.warning("Username and Password cannot be empty!")
        return False

    payload = {"username": username, "password": password}
    try:
        response = requests.post(f"{API_URL}/login", json=payload)
        if response.status_code == 200:
            st.success(f"Logged in as: {username}")
            st.session_state['logged_in_user'] = username  # Save username to session state
            return True
        else:
            st.error(f"Login failed: {response.json().get('detail', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"Failed to connect to server: {e}")
        return False
