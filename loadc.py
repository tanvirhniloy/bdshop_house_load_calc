import streamlit as st
import uuid

st.set_page_config(page_title="Home Load Calculator", layout="wide")

# Appliance watt list
appliances = {
    "Immersion Heater": 750,
    "Storage Geyser": 1750,
    "Instant Geyser": 4500,
    "AC 1 Ton Non-Inverter": 1200,
    "AC 1 Ton Inverter": 700,
    "AC 2 Ton Non-Inverter": 2400,
    "AC 2 Ton Inverter": 1400,
    "AC 1.5 Ton Non-Inverter": 1800,
    "AC 1.5 Ton Inverter": 1100,
    "Induction Cooker": 1500,
    "Microwave Oven": 900,
    "OTG Oven": 1500,
    "Electric Built-in Oven": 2500,
    "Infrared Cooker": 2100,
    "Rice Cooker": 700,
    "Electric Kettle": 1700,
    "Refrigerator Small": 180,
    "Refrigerator Medium": 200,
    "Refrigerator Large": 350,
    "Washing Machine": 500,
    "Iron": 1500,
    "Water Pump": 800,
    "Laptop": 50,
    "Desktop Computer": 250,
    "Inkjet Printer": 40,
    "Laser Printer": 400,
    "Television": 100,
    "WiFi Router + ONU": 15,
    "CCTV System": 40,
    "Phone Chargers (Multiple)": 10,
    "Ceiling Fan": 80,
    "BLDC Fan": 32,
    "Exhaust Fan": 30,
    "Hair Dryer": 1200,
    "LED Bulb": 12,
    "LED Tube Light": 20
}

# Initialize session state
if "rows" not in st.session_state:
    st.session_state.rows = [{
        "id": str(uuid.uuid4()),
        "appliance": None,
        "qty": 1
    }]

# CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1f2937, #111827);
    color: white;
}
.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    color: #ffffff;
    margin-bottom: 30px;
}
.header-box {
    background: #2563eb;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    color: white;
    font-weight: bold;
    font-size: 18px;
    margin-bottom: 10px;
}
.load-box {
    background: #ffffff;
    padding: 12px;
    border-radius: 10px;
    text-align: center;
    color: #111827;
    font-weight: bold;
    border: 2px solid #2563eb;
}
.total-box {
    background: linear-gradient(90deg, #10b981, #059669);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-size: 28px;
    font-weight: bold;
    margin-top: 30px;
}
.stButton>button {
    width: 100%;
    border-radius: 10px;
    background: #2563eb;
    color: white;
    font-weight: bold;
    height: 45px;
    border: none;
    font-size: 15px;
}
.stButton>button:hover {
    background: #1d4ed8;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='main-title'>⚡ BDSHOP Home Load Calculator</div>", unsafe_allow_html=True)

# Header
col1, col2, col3, col4 = st.columns([4, 2, 3, 1])
with col1:
    st.markdown("<div class='header-box'>Appliance Selection</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='header-box'>Quantity</div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='header-box'>Load</div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div class='header-box'>Delete</div>", unsafe_allow_html=True)

total_load = 0

# Render rows
for row in st.session_state.rows:
    row_id = row["id"]

    col1, col2, col3, col4 = st.columns([4, 2, 3, 1])

    with col1:
        appliance = st.selectbox(
            "Appliance",
            options=list(appliances.keys()),
            index=None if row["appliance"] is None else list(appliances.keys()).index(row["appliance"]),
            placeholder="Select your device",
            key=f"appliance_{row_id}",
            label_visibility="collapsed"
        )

    with col2:
        qty = st.number_input(
            "Qty",
            min_value=1,
            value=row["qty"],
            key=f"qty_{row_id}",
            label_visibility="collapsed"
        )

    load = appliances[appliance] * qty if appliance else 0
    total_load += load

    with col3:
        st.markdown(f"<div class='load-box'>{load} W</div>", unsafe_allow_html=True)

    with col4:
        if st.button("❌", key=f"delete_{row_id}"):
            st.session_state.rows = [
                r for r in st.session_state.rows if r["id"] != row_id
            ]
            st.rerun()

    row["appliance"] = appliance
    row["qty"] = qty

# Buttons
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("➕ Add New Item"):
        st.session_state.rows.append({
            "id": str(uuid.uuid4()),
            "appliance": None,
            "qty": 1
        })
        st.rerun()

with col2:
    calculate = st.button("⚡ Calculate Total Load")

# Result
if calculate:
    st.markdown(
        f"<div class='total-box'>Total House Load: {total_load} W ({total_load/1000:.2f} kW)</div>",
        unsafe_allow_html=True
    )
