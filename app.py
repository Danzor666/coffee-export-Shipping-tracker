import streamlit as st
import json
import os

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def login():
    st.header("🔑 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_clicked = st.button("Login")

    if login_clicked:
        users = load_users()
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("❌ Invalid username or password")

def signup():
    st.header("📝 Sign Up")
    new_username = st.text_input("Create Username", key="signup_username")
    new_password = st.text_input("Create Password", type="password", key="signup_password")
    signup_clicked = st.button("Sign Up")

    if signup_clicked:
        users = load_users()
        if new_username in users:
            st.warning("⚠️ Username already exists")
        else:
            users[new_username] = new_password
            save_users(users)
            st.success("✅ Signup successful! Now please login.")
            st.session_state.signup_done = True

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "signup_done" not in st.session_state:
    st.session_state.signup_done = False

def main():
    if not st.session_state.logged_in:
        if st.session_state.signup_done:
            st.session_state.signup_done = False
            st.experimental_rerun()

        choice = st.radio("Choose action:", ["Login", "Sign Up"])
        if choice == "Login":
            login()
        else:
            signup()
    else:
        st.write(f"👋 Hello, {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.experimental_rerun()

if __name__ == "__main__":
    main()
