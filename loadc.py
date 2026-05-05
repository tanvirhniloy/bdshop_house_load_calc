import streamlit as st
import uuid
import json

st.set_page_config(
    page_title="BDSHOP Load Calculator", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Appliance database with categories
appliances_db = {
    "Water Heating": {
        "Immersion Heater": 750,
        "Storage Geyser": 1750,
        "Instant Geyser": 4500,
    },
    "Air Conditioning": {
        "AC 1 Ton Non-Inverter": 1200,
        "AC 1 Ton Inverter": 700,
        "AC 2 Ton Non-Inverter": 2400,
        "AC 2 Ton Inverter": 1400,
        "AC 1.5 Ton Non-Inverter": 1800,
        "AC 1.5 Ton Inverter": 1100,
    },
    "Cooking": {
        "Induction Cooker": 1500,
        "Microwave Oven": 900,
        "OTG Oven": 1500,
        "Electric Built-in Oven": 2500,
        "Infrared Cooker": 2100,
        "Rice Cooker": 700,
        "Electric Kettle": 1700,
    },
    "Refrigeration": {
        "Refrigerator Small": 180,
        "Refrigerator Medium": 200,
        "Refrigerator Large": 350,
    },
    "Laundry & Ironing": {
        "Washing Machine": 500,
        "Iron": 1500,
    },
    "Computing": {
        "Laptop": 50,
        "Desktop Computer": 250,
        "Inkjet Printer": 40,
        "Laser Printer": 400,
    },
    "Entertainment": {
        "Television": 100,
        "WiFi Router + ONU": 15,
    },
    "Ventilation": {
        "Ceiling Fan": 80,
        "BLDC Fan": 32,
        "Exhaust Fan": 30,
    },
    "Lighting": {
        "LED Bulb": 12,
        "LED Tube Light": 20,
    },
    "Others": {
        "Water Pump": 800,
        "CCTV System": 40,
        "Phone Chargers (Multiple)": 10,
        "Hair Dryer": 1200,
    }
}

# Flatten appliances for easy access
all_appliances = {}
for category, items in appliances_db.items():
    all_appliances.update(items)

# Initialize session state
if "rows" not in st.session_state:
    st.session_state.rows = []

if "show_result" not in st.session_state:
    st.session_state.show_result = False

if "saved_configs" not in st.session_state:
    st.session_state.saved_configs = []

# Enhanced CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
}

.main-header {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 10px 40px rgba(59, 130, 246, 0.3);
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.subtitle {
    font-size: 16px;
    color: #e0e7ff;
    margin-top: 8px;
}

.header-row {
    display: grid;
    grid-template-columns: 2fr 0.8fr 1fr 1fr 0.5fr;
    gap: 10px;
    margin-bottom: 15px;
    padding: 15px;
    background: rgba(59, 130, 246, 0.15);
    border-radius: 12px;
    border: 2px solid rgba(59, 130, 246, 0.3);
}

.header-cell {
    color: #60a5fa;
    font-weight: 700;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
    text-align: center;
}

.load-display {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    padding: 12px 20px;
    border-radius: 10px;
    text-align: center;
    color: white;
    font-weight: 700;
    font-size: 16px;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
}

.total-result {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    padding: 35px;
    border-radius: 20px;
    text-align: center;
    margin-top: 30px;
    box-shadow: 0 10px 40px rgba(245, 158, 11, 0.4);
    animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.total-title {
    color: #fef3c7;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 10px;
}

.total-value {
    color: white;
    font-size: 48px;
    font-weight: 800;
    margin: 10px 0;
}

.total-subtitle {
    color: #fef3c7;
    font-size: 14px;
}

.stButton>button {
    border-radius: 10px;
    font-weight: 700;
    height: 48px;
    border: none;
    font-size: 15px;
    transition: all 0.3s;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}

.info-card {
    background: rgba(59, 130, 246, 0.1);
    border: 2px solid rgba(59, 130, 246, 0.3);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
}

.info-title {
    color: #60a5fa;
    font-weight: 700;
    font-size: 16px;
    margin-bottom: 10px;
}

.info-text {
    color: #cbd5e1;
    font-size: 14px;
    line-height: 1.6;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin-top: 20px;
}

.stat-card {
    background: rgba(59, 130, 246, 0.1);
    border: 2px solid rgba(59, 130, 246, 0.3);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}

.stat-value {
    color: #60a5fa;
    font-size: 28px;
    font-weight: 800;
}

.stat-label {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 5px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.category-badge {
    background: rgba(59, 130, 246, 0.2);
    color: #60a5fa;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    display: inline-block;
    margin-top: 5px;
}

div[data-testid="stExpander"] {
    background: rgba(59, 130, 246, 0.05);
    border: 2px solid rgba(59, 130, 246, 0.2);
    border-radius: 12px;
}

.stSelectbox, .stNumberInput {
    border-radius: 10px;
}

div[data-baseweb="select"] > div {
    background-color: rgba(30, 41, 59, 0.8);
    border: 2px solid rgba(59, 130, 246, 0.3);
    border-radius: 10px;
}

input {
    background-color: rgba(30, 41, 59, 0.8) !important;
    border: 2px solid rgba(59, 130, 246, 0.3) !important;
    border-radius: 10px !important;
    color: white !important;
}

.recommendation-box {
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    padding: 25px;
    border-radius: 15px;
    margin-top: 20px;
    color: white;
}

.rec-title {
    font-weight: 700;
    font-size: 18px;
    margin-bottom: 15px;
}

.rec-item {
    background: rgba(255,255,255,0.1);
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 10px;
    border-left: 4px solid #a78bfa;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📋 Quick Info")
    
    st.info("""
    **How to use:**
    1. Select appliances from dropdown or add custom
    2. Set quantity for each item
    3. View individual loads instantly
    4. Calculate total consumption
    """)
    
    st.markdown("### 💡 Tips")
    st.success("""
    - Use inverter ACs to save energy
    - LED lights consume 80% less power
    - BLDC fans are highly efficient
    """)
    
    st.markdown("### 📊 Load Categories")
    for category in appliances_db.keys():
        with st.expander(f"**{category}**"):
            for appliance, watt in appliances_db[category].items():
                st.write(f"• {appliance}: **{watt}W**")
    
    if st.button("🗑️ Clear All Items"):
        st.session_state.rows = []
        st.session_state.show_result = False
        st.rerun()

# Main content
st.markdown("""
<div class='main-header'>
    <div class='main-title'>⚡ BDSHOP Load Calculator</div>
    <div class='subtitle'>Calculate your home electrical load accurately</div>
</div>
""", unsafe_allow_html=True)

# Header row
st.markdown("""
<div class='header-row'>
    <div class='header-cell'>Appliance / Custom Device</div>
    <div class='header-cell'>Quantity</div>
    <div class='header-cell'>Hours/Day</div>
    <div class='header-cell'>Load (W)</div>
    <div class='header-cell'>Action</div>
</div>
""", unsafe_allow_html=True)

# Add initial row if empty
if len(st.session_state.rows) == 0:
    st.session_state.rows.append({
        "id": str(uuid.uuid4()),
        "type": "preset",
        "appliance": None,
        "custom_name": "",
        "custom_watt": 0,
        "qty": 1,
        "hours": 1
    })

total_load = 0
daily_consumption = 0
rows_to_delete = []

# Render rows
for idx, row in enumerate(st.session_state.rows):
    row_id = row["id"]
    
    col1, col2, col3, col4, col5 = st.columns([2, 0.8, 1, 1, 0.5])
    
    with col1:
        # Radio button for preset vs custom
        row_type = st.radio(
            "Type",
            options=["Preset", "Custom"],
            key=f"type_{row_id}",
            horizontal=True,
            label_visibility="collapsed",
            index=0 if row["type"] == "preset" else 1
        )
        
        if row_type == "Preset":
            row["type"] = "preset"
            appliance = st.selectbox(
                "Appliance",
                options=list(all_appliances.keys()),
                index=None if row["appliance"] is None else list(all_appliances.keys()).index(row["appliance"]),
                placeholder="🔍 Select your device",
                key=f"appliance_{row_id}",
                label_visibility="collapsed"
            )
            row["appliance"] = appliance
            
            # Show category badge
            if appliance:
                for cat, items in appliances_db.items():
                    if appliance in items:
                        st.markdown(f"<span class='category-badge'>{cat}</span>", unsafe_allow_html=True)
                        break
        else:
            row["type"] = "custom"
            col_name, col_watt = st.columns([2, 1])
            with col_name:
                custom_name = st.text_input(
                    "Device Name",
                    value=row["custom_name"],
                    placeholder="Enter device name",
                    key=f"custom_name_{row_id}",
                    label_visibility="collapsed"
                )
                row["custom_name"] = custom_name
            
            with col_watt:
                custom_watt = st.number_input(
                    "Watts",
                    min_value=0,
                    value=row["custom_watt"],
                    step=10,
                    key=f"custom_watt_{row_id}",
                    label_visibility="collapsed"
                )
                row["custom_watt"] = custom_watt
    
    with col2:
        qty = st.number_input(
            "Qty",
            min_value=1,
            max_value=50,
            value=row["qty"],
            key=f"qty_{row_id}",
            label_visibility="collapsed"
        )
        row["qty"] = qty
    
    with col3:
        hours = st.number_input(
            "Hours",
            min_value=0.5,
            max_value=24.0,
            value=float(row["hours"]),
            step=0.5,
            key=f"hours_{row_id}",
            label_visibility="collapsed"
        )
        row["hours"] = hours
    
    # Calculate load
    if row["type"] == "preset" and row["appliance"]:
        load = all_appliances[row["appliance"]] * qty
    elif row["type"] == "custom" and row["custom_watt"] > 0:
        load = row["custom_watt"] * qty
    else:
        load = 0
    
    total_load += load
    daily_consumption += (load * hours / 1000)  # kWh
    
    with col4:
        st.markdown(f"<div class='load-display'>{load} W</div>", unsafe_allow_html=True)
    
    with col5:
        if st.button("❌", key=f"delete_{row_id}"):
            rows_to_delete.append(row_id)

# Delete rows
if rows_to_delete:
    st.session_state.rows = [r for r in st.session_state.rows if r["id"] not in rows_to_delete]
    st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Action buttons
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("➕ Add Preset Device", use_container_width=True):
        st.session_state.rows.append({
            "id": str(uuid.uuid4()),
            "type": "preset",
            "appliance": None,
            "custom_name": "",
            "custom_watt": 0,
            "qty": 1,
            "hours": 1
        })
        st.rerun()

with col2:
    if st.button("🔧 Add Custom Device", use_container_width=True):
        st.session_state.rows.append({
            "id": str(uuid.uuid4()),
            "type": "custom",
            "appliance": None,
            "custom_name": "",
            "custom_watt": 0,
            "qty": 1,
            "hours": 1
        })
        st.rerun()

with col3:
    if st.button("⚡ Calculate Total Load", use_container_width=True, type="primary"):
        st.session_state.show_result = True
        st.rerun()

# Results
if st.session_state.show_result and total_load > 0:
    st.markdown(f"""
    <div class='total-result'>
        <div class='total-title'>🏠 TOTAL HOUSE LOAD</div>
        <div class='total-value'>{total_load:,} W</div>
        <div class='total-subtitle'>{total_load/1000:.2f} kW | Daily: {daily_consumption:.2f} kWh</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics
    st.markdown("<div class='stats-grid'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value'>{len(st.session_state.rows)}</div>
            <div class='stat-label'>Total Devices</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        monthly_kwh = daily_consumption * 30
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value'>{monthly_kwh:.1f}</div>
            <div class='stat-label'>Monthly (kWh)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Assuming 8 Tk per kWh
        monthly_cost = monthly_kwh * 8
        st.markdown(f"""
        <div class='stat-card'>
            <div class='stat-value'>৳{monthly_cost:.0f}</div>
            <div class='stat-label'>Est. Bill/Month</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("""
    <div class='recommendation-box'>
        <div class='rec-title'>💡 Smart Recommendations</div>
    """, unsafe_allow_html=True)
    
    recommendations = []
    
    if total_load < 3000:
        recommendations.append("✅ Your load is suitable for a 3kW solar system")
    elif total_load < 5000:
        recommendations.append("✅ Consider a 5kW solar system for backup")
    else:
        recommendations.append("⚠️ High load detected. Consider a 7-10kW solar system")
    
    if daily_consumption > 30:
        recommendations.append("💰 High daily consumption! Switch to energy-efficient appliances")
    
    # Check for non-inverter ACs
    for row in st.session_state.rows:
        if row["type"] == "preset" and row["appliance"] and "Non-Inverter" in row["appliance"]:
            recommendations.append("🌡️ Replace non-inverter AC with inverter type to save 40% energy")
            break
    
    for rec in recommendations:
        st.markdown(f"<div class='rec-item'>{rec}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 20px;'>
    <p style='font-size: 14px;'>Made with ❤️ for Bangladesh | Powered by BDSHOP</p>
    <p style='font-size: 12px; margin-top: 5px;'>💡 Energy efficiency starts with awareness</p>
    <p style='font-size: 12px; margin-top: 5px;'> Developed By: Tanvir Hasan </p>
</div>
""", unsafe_allow_html=True)
