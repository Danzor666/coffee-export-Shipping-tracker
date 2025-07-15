import streamlit as st
import json
import os

USERS_FILE = "users.json"

# Initialize users file with admin if not exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({"cha": "supercha123"}, f)  # admin user

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def login():
    st.header("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        users = load_users()
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid username or password")

def signup():
    st.header("📝 Sign Up")
    new_username = st.text_input("Create Username")
    new_password = st.text_input("Create Password", type="password")
    if st.button("Sign Up"):
        users = load_users()
        if new_username in users:
            st.warning("⚠️ Username already exists")
        else:
            users[new_username] = new_password
            save_users(users)
            st.success("✅ Signup successful! Now please login.")
            st.experimental_rerun()

def main():
    if not st.session_state.logged_in:
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
        # Here you can add more app features for logged-in users

main()
