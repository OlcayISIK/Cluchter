# Import necessary modules
import streamlit as st

# Load external CSS
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def app():
    # This function create the home page

    # Add title to the home page
    st.markdown("""
    <div style='
        font-size: 120px;
        font-weight: 900;
        text-align: center;
        font-family: "Rajdhani", sans-serif;
        margin-bottom: 20px;
        color: white;
    '>
    Cluchter
    </div>
    """, unsafe_allow_html=True)
    # Add image to the home page
    st.image("images/cluchter.png")

    # Add brief description of your web app
    st.markdown(
        """<p style="font-size:20px;">Clutcher is a smart, clip-on wearable designed for esports athletes to manage stress, fatigue, and performance during high-stakes play. Inspired by Hoku acupressure techniques, it integrates biometric sensors (GSR, EMG, IMU, PPG) to track physiological signals discreetly. Real-time insights are transmitted via low-latency Bluetooth to a companion app, offering coaches and players actionable data without interrupting gameplay. Its small, screenless design prioritizes comfort and minimal distraction—making it ideal for both training and tournament use.</p>""",
        unsafe_allow_html=True)
