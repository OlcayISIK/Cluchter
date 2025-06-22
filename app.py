import streamlit as st
st.set_page_config(layout="wide")  # <--- Add this as the very first Streamlit call
from datetime import datetime
import base64
from web_functions import load_data
from Tabs import home, maide, olcay, hongjoshua, kim

# Load external CSS
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def img_to_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

Tabs = {
    "Home": {"img": None, "page": home, "color": ""},
    "Maide": {"img": "images/maide.jpeg", "page": maide, "color": "🔴"},
    "Olcay": {"img": "images/olcay.jpeg", "page": olcay, "color": "🟢"},
    "Joshua": {"img": "images/hong-joshua.png", "page": hongjoshua, "color": "🟡"},
    "Ji-won": {"img": "images/kimjiwon.jpeg", "page": kim, "color": "🔵"}
}

for tab in Tabs.values():
    if tab["img"]:
        tab["img_base64"] = img_to_base64(tab["img"])
    else:
        tab["img_base64"] = None

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Home"

with st.sidebar:
    # Current time and date
    now = datetime.now()
    time_str = now.strftime("%H:%M")
    date_str = now.strftime("%a,%d").upper()

    st.markdown(f"""
    <div class="sidebar-top-time-date">
        <div class="time-left">{time_str}</div>
        <div class="date-right">{date_str}</div>
    </div>
    """, unsafe_allow_html=True)

    # Stylized CLUCHTER button as a heading
    st.markdown("""
    <style>
    .cluchter-button > button {
        font-size: 2.2rem !important;
        font-weight: bold !important;
        color: white !important;
        background: transparent !important;
        border: none !important;
        text-align: center !important;
        padding: 0.5rem 1rem !important;
        width: 100%;
    }
    .cluchter-button > button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        cursor: pointer !important;
    }
    </style>
    """, unsafe_allow_html=True)

    home_col1, home_col2, home_col3 = st.columns([1, 4, 1])
    with home_col2:
        st.markdown('<div class="cluchter-button">', unsafe_allow_html=True)
        if st.button("CLUCHTER", key="home_button"):
            st.session_state.selected_page = "Home"
        st.markdown('</div>', unsafe_allow_html=True)

    # Logo
    try:
        with open("images/valorant_logo.png", "rb") as img_file:
            logo_base64 = base64.b64encode(img_file.read()).decode()
        st.markdown(f"<div class='sidebar-logo'><img src='data:image/jpeg;base64,{logo_base64}' /></div>", unsafe_allow_html=True)
    except:
        st.warning("Valorant logo not found.")

    # Player selector
    st.markdown("<div class='sidebar-section-header'>👤 Select Player</div>", unsafe_allow_html=True)

    for name, data in Tabs.items():
        if name == "Home":
            continue
        cols = st.columns([1, 4])
        if data["img_base64"]:
            cols[0].image(f"data:image/jpeg;base64,{data['img_base64']}", width=40)
        else:
            cols[0].write("")
        clicked = cols[1].button(f"{name} {data['color']}", key=name)
        if clicked:
            st.session_state.selected_page = name

# Load data
df, x, y = load_data()

# Render selected page
page = st.session_state.selected_page
if page == "Home":
    Tabs[page]["page"].app()
else:
    Tabs[page]["page"].app(df, x, y)

# System status
st.sidebar.markdown("<hr style='margin-top: 20px; margin-bottom: 10px;'>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='sidebar-section-header'>System Status</div>", unsafe_allow_html=True)

status_fields = [
    ("Artificial Intelligence", "green"),
    ("GSR Data", "green"),
    ("Respiration Rate", "green"),
    ("Body Tempature", "green"),
    ("Limb Movement", "green"),
    ("Blood Oxygen", "green"),
    ("Hand Tremors", "green"),
    ("Sleeping Hour", "green"),
    ("Heart Rate", "green"),
]

for label, color in status_fields:
    st.sidebar.markdown(f"""
        <div class='system-status'>
            <div class='status-dot' style='background-color: {color};'></div>
            <span class='status-label'>{label}</span>
        </div>
    """, unsafe_allow_html=True)
