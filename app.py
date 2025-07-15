# app.py
import streamlit as st
import os
import json
from datetime import datetime

# Paths and constants
DATA_FILE = 'data.json'
UPLOAD_DIR = 'uploads'
REQUIRED_DOCS = [
    'Contract', 'Commercial Invoice', 'Packing List',
    'Bill of Lading', 'Phytosanitary Certificate', 'Certificate of Origin'
]

# Load existing data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

# Save data
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Create upload folder if not exists
def make_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Upload document function
def upload_doc(shipment_id, doc_type):
    file = st.file_uploader(f"Upload {doc_type}", type=['pdf', 'jpg', 'png'], key=f"{shipment_id}_{doc_type}")
    if file:
        path = os.path.join(UPLOAD_DIR, shipment_id)
        make_folder(path)
        ext = file.name.split('.')[-1]
        with open(os.path.join(path, f"{doc_type}.{ext}"), 'wb') as f:
            f.write(file.getbuffer())
        st.success(f"{doc_type} uploaded.")

# Check uploaded docs
def check_uploaded(shipment_id):
    path = os.path.join(UPLOAD_DIR, shipment_id)
    uploaded = []
    if os.path.exists(path):
        uploaded = [f.split('.')[0] for f in os.listdir(path)]
    return uploaded

# Streamlit UI
st.set_page_config(page_title="Coffee Export Tracker", layout="wide")
st.title("📦 Coffee Export Documentation Tracker")

menu = ["Add Shipment", "View Shipments"]
choice = st.sidebar.selectbox("Menu", menu)

all_data = load_data()

if choice == "Add Shipment":
    st.subheader("➕ Add New Shipment")
    with st.form(key='add_form'):
        shipment_id = st.text_input("Shipment ID")
        buyer = st.text_input("Buyer Name")
        etd = st.date_input("ETD")
        contract_date = st.date_input("Contract Date")
        bl_number = st.text_input("Bill of Lading Number")
        container_no = st.text_input("Container Number")
        coffee_type = st.text_input("Coffee Type / Grade")
        quantity = st.number_input("Quantity (bags)", min_value=0, step=1)
        port_loading = st.text_input("Port of Loading")
        exporter_name = st.text_input("Exporter Name")
        submitted = st.form_submit_button("Save Shipment")

        if submitted:
            shipment = {
                "shipment_id": shipment_id,
                "buyer": buyer,
                "etd": etd.strftime('%Y-%m-%d'),
                "contract_date": contract_date.strftime('%Y-%m-%d'),
                "bl_number": bl_number,
                "container_no": container_no,
                "coffee_type": coffee_type,
                "quantity": quantity,
                "port_loading": port_loading,
                "exporter_name": exporter_name,
                "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            all_data.append(shipment)
            save_data(all_data)
            st.success("Shipment added.")

elif choice == "View Shipments":
    st.subheader("📄 Shipment List")
    if not all_data:
        st.info("No shipments yet.")
    else:
        for shipment in all_data:
            with st.expander(f"🚢 {shipment['shipment_id']} - {shipment['buyer']}"):
                st.write(f"**ETD:** {shipment['etd']}")
                st.write(f"**Contract Date:** {shipment['contract_date']}")
                st.write(f"**BL Number:** {shipment.get('bl_number','')}")
                st.write(f"**Container No.:** {shipment.get('container_no','')}")
                st.write(f"**Coffee Type:** {shipment.get('coffee_type','')}")
                st.write(f"**Quantity (bags):** {shipment.get('quantity','')}")
                st.write(f"**Port of Loading:** {shipment.get('port_loading','')}")
                st.write(f"**Exporter Name:** {shipment.get('exporter_name','')}")
                uploaded = check_uploaded(shipment['shipment_id'])

                for doc in REQUIRED_DOCS:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        upload_doc(shipment['shipment_id'], doc)
                    with col2:
                        if doc in uploaded:
                            st.success("Uploaded")
                        else:
                            st.error("Missing")

                missing = [d for d in REQUIRED_DOCS if d not in uploaded]
                if missing:
                    st.warning(f"🚨 Missing documents: {', '.join(missing)}")
                else:
                    st.success("✅ All documents uploaded.")
