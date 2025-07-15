import streamlit as st
import json
import os

# Load user database
USERS_FILE = "users.json"
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({"cha": "supercha123"}, f)  # Admin account

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# Session state init
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Login page
def login():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        users = load_users()
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("✅ Login successful")
            st.experimental_rerun()
        else:
            st.error("❌ Incorrect username or password")

# Signup page
def signup():
    st.title("📝 Sign Up")
    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    if st.button("Sign Up"):
        users = load_users()
        if username in users:
            st.warning("⚠️ Username already exists")
        else:
            users[username] = password
            save_users(users)
            st.success("✅ Signup successful. Now login.")
            st.experimental_rerun()

# Document form
def document_entry():
    st.title("📄 Coffee Export Document Form")

    shipment_id = st.text_input("Shipment ID")
    buyer_name = st.text_input("Buyer Name")
    etd = st.date_input("ETD (Estimated Time of Departure)")
    contract_date = st.date_input("Contract Date")

    doc_file = st.file_uploader("Upload Supporting Document (PDF, DOCX, XLSX)", type=["pdf", "docx", "xlsx"])

    if st.button("Submit"):
        st.success("✅ Document submitted")
        # You can extend this to save data in a database or CSV

# Admin dashboard
def admin_dashboard():
    st.title("👑 Admin Dashboard - All Submissions")
    st.info("🔧 You can add functionality to view/export user submissions here.")

# Navigation
def main():
    if not st.session_state.logged_in:
        menu = st.sidebar.radio("Choose an option", ["Login", "Sign Up"])
        if menu == "Login":
            login()
        else:
            signup()
    else:
        st.sidebar.success(f"Welcome, {st.session_state.username}")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.experimental_rerun()

        if st.session_state.username == "cha":
            admin_dashboard()
        else:
            document_entry()

main()

