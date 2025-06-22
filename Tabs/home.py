import streamlit as st
import base64

with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_base64_of_bin_file(bin_file_path):
    with open(bin_file_path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def app():
    st.markdown("""
    <div class="cluchter-title">
        Cluchter
    </div>
    """, unsafe_allow_html=True)

    img_base64 = get_base64_of_bin_file("images/cluchter.png")

    st.markdown(f"""
    <div class="center-box">
        <img src="data:image/png;base64,{img_base64}" />
        <p class="main-description">
        Clutcher is a smart, clip-on wearable designed for esports athletes to manage stress, fatigue, and performance during high-stakes play. Inspired by Hoku acupressure techniques, it integrates biometric sensors (GSR, EMG, IMU, PPG) to track physiological signals discreetly. Real-time insights are transmitted via low-latency Bluetooth to a companion app, offering coaches and players actionable data without interrupting gameplay. Its small, screenless design prioritizes comfort and minimal distraction—making it ideal for both training and tournament use.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Parallel content sections
    st.markdown("""
    <div class="features-container">
        <div class="feature-box">
            <h3>Real-time Biometrics</h3>
            <p>Track GSR, EMG, IMU, and PPG signals with millisecond precision to monitor player stress and fatigue levels during gameplay.</p>
        </div>
        <div class="feature-box">
            <h3>Non-intrusive Design</h3>
            <p>Clip-on wearable that doesn't interfere with performance or distract from the game experience.</p>
        </div>
        <div class="feature-box">
            <h3>Low-latency Bluetooth</h3>
            <p>Instant data transmission to coaching dashboards with minimal delay for real-time adjustments.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()  # Default gray line

        # Technology highlight
    st.markdown("""
    <div class="tech-highlight">
        <h2 style="text-align: center;">Powered by Advanced Sensor Fusion</h2>
        <div class="tech-grid">
            <div class="tech-item">
                <h4>GSR Monitoring</h4>
                <p>Galvanic skin response tracking for stress detection</p>
            </div>
            <div class="tech-item">
                <h4>EMG Sensors</h4>
                <p>Muscle activity measurement for tension analysis</p>
            </div>
            <div class="tech-item">
                <h4>IMU Tracking</h4>
                <p>Body movement and posture monitoring</p>
            </div>
            <div class="tech-item">
                <h4>PPG Technology</h4>
                <p>Heart rate and blood flow monitoring</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()  # Default gray line

    # Testimonials/Use Cases section
    st.markdown("""
    <div class="testimonials">
        <h2>Trusted by Esports Professionals</h2>
        <div class="testimonial-grid">
            <div class="testimonial-card">
                <p>"Cluchter helped our team identify stress patterns during tournament play, allowing us to adjust our training regimen."</p>
                <p class="author">- Pro Team Coach</p>
            </div>
            <div class="testimonial-card">
                <p>"I can focus on the game while knowing my biometrics are being monitored for optimal performance timing."</p>
                <p class="author">- Pro Valorant Player</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    