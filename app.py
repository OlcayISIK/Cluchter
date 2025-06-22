import streamlit as st
from datetime import datetime
import base64
from web_functions import load_data
from Tabs import home, maide, olcay, john

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
    "Joshua": {"img": "images/hong-joshua.png", "page": john, "color": "🟡"},
}

for tab in Tabs.values():
    if tab["img"]:
        tab["img_base64"] = img_to_base64(tab["img"])
    else:
        tab["img_base64"] = None

if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Home"

with st.sidebar:
    # Centered Home button with icon
    home_col1, home_col2, home_col3 = st.columns([1, 2, 1])
    with home_col2:
        if st.button("Home", key="home_button"):
            st.session_state.selected_page = "Home"

    # Date display
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"<div class='sidebar-date'>{now}</div>", unsafe_allow_html=True)

    # Title and Valorant logo
    st.markdown("<div class='sidebar-title'>Valorant</div>", unsafe_allow_html=True)
    try:
        with open("images/valorant_logo.png", "rb") as img_file:
            logo_base64 = base64.b64encode(img_file.read()).decode()
        st.markdown(f"<div class='sidebar-logo'><img src='data:image/jpeg;base64,{logo_base64}' /></div>", unsafe_allow_html=True)
    except:
        st.warning("Valorant logo not found.")

    st.markdown("<div class='sidebar-section-header'>👤 Select Gamer</div>", unsafe_allow_html=True)

    # Sidebar tabs with images and colored emoji buttons
    for name, data in Tabs.items():
        if name == "Home":
            continue  # Home already at top

        cols = st.columns([1, 4])
        # Show circular image
        if data["img_base64"]:
            cols[0].image(f"data:image/jpeg;base64,{data['img_base64']}", width=40)
        else:
            cols[0].write("")

        # Button with colored emoji label
        clicked = cols[1].button(f"{data['color']} {name}", key=name)
        if clicked:
            st.session_state.selected_page = name

# Load data
df, x, y = load_data()

# Show selected page
page = st.session_state.selected_page
if page == "Home":
    Tabs[page]["page"].app()
else:
    Tabs[page]["page"].app(df, x, y)

# Sidebar system status
st.sidebar.markdown("<hr style='margin-top: 20px; margin-bottom: 10px;'>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='sidebar-section-header'>System Status</div>", unsafe_allow_html=True)

status_fields = [
    ("Artificial Intelligence", "green"),
    ("GSR Data", "green"),
    ("Respiration Rate", "green"),
    ("Body Tempature", "green"),
    ("Limb Movement", "green"),
    ("Blood Oxygen", "green"),
    ("Mouse Squeeze Muscle Tone", "green"),
    ("Sleeping Hour", "green"),
    ("Heart Rate", "green"),
]

for label, color in status_fields:
    st.sidebar.markdown(f"""
        <div class='system-status'>
            <div class='status-dot' style='background-color: {color};'></div>
            <span class='status-label'>{label} Active</span>
        </div>
    """, unsafe_allow_html=True)
