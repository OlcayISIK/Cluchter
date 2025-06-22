import streamlit as st
from web_functions import detect

def app(df, x, y):
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    if "active_button" not in st.session_state:
        st.session_state.active_button = "5"

    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("images/kimjiwon.jpeg", use_container_width=True, width=200)
    with col2:
        st.markdown("<div class='big-title'>Kim Ji-Won (Raze)</div>", unsafe_allow_html=True)
        st.markdown("<div class='big-title-second'>Current Status: <span class='optimal'>Optimal</span></div>", unsafe_allow_html=True)

    st.markdown("<div class='sub-title'>Overall Game Stress Predictions</div>", unsafe_allow_html=True)

    presets = {
        "1": [89, 24, 97.6, 16.0, 92.2, 90.5, 6.5, 70],
        "2": [92, 23, 97.2, 15.5, 91.2, 89.1, 7.5, 68],
        "3": [56, 22, 98.4, 12.0, 94.8, 78.4, 6.5, 68],
        "4": [58, 25, 97.4, 14.0, 93.8, 76.4, 6.5, 68]
        # "5" removed — handled dynamically below
    }

    colb1, colb2, colb3, colb4, colb5 = st.columns(5)
    if colb1.button("1.Game Stats"):
        st.session_state.active_button = "1"
        detect_and_display(x, y, presets["1"])
    if colb2.button("2.Game Stats"):
        st.session_state.active_button = "2"
        detect_and_display(x, y, presets["2"])
    if colb3.button("3.Game Stats"):
        st.session_state.active_button = "3"
        detect_and_display(x, y, presets["3"])
    if colb4.button("4.Game Stats"):
        st.session_state.active_button = "4"
        detect_and_display(x, y, presets["4"])
    if colb5.button("Current Game"):
        st.session_state.active_button = "5"

    bt_min_c = round((df["bt"].min() - 32) * 5 / 9, 1)
    bt_max_c = round((df["bt"].max() - 32) * 5 / 9, 1)

    readonly = st.session_state.active_button != "5"

    def slider_val(label, key, minv, maxv, default):
        return st.slider(
            label, minv, maxv, value=default,
            disabled=readonly, key=key
        )

    # Determine preset values
    if st.session_state.active_button in presets:
        preset_vals = presets[st.session_state.active_button]
    else:
        # Dynamic min values for "Current Game"
        preset_vals = [
            int(df["gsr"].min()),
            int(df["rr"].min()),
            float(df["bt"].min()),
            float(df["lm"].min()),
            float(df["bo"].min()),
            float(df["rem"].min()),
            float(df["sh"].min()),
            float(df["hr"].min())
        ]

    gsr = slider_val("GSR Data", "kimjiwon_gsr", int(df["gsr"].min()), int(df["gsr"].max()), int(preset_vals[0]))
    rr = slider_val("Respiration Rate", "kimjiwon_rr", int(df["rr"].min()), int(df["rr"].max()), int(preset_vals[1]))
    bt_celsius = slider_val(
        "Body Temperature (in °C)", "kimjiwon_bt", bt_min_c, bt_max_c,
        round((preset_vals[2] - 32) * 5 / 9, 1)
    )
    lm = slider_val("Limb Movement", "kimjiwon_lm", float(df["lm"].min()), float(df["lm"].max()), float(preset_vals[3]))
    bo = slider_val("Blood Oxygen(%)", "kimjiwon_bo", float(df["bo"].min()), float(df["bo"].max()), float(preset_vals[4]))
    rem = slider_val("Mouse Squeeze Muscle Tone", "kimjiwon_rem", float(df["rem"].min()), float(df["rem"].max()), float(preset_vals[5]))
    sh = slider_val("Sleeping Hour", "kimjiwon_sh", float(df["sh"].min()), float(df["sh"].max()), float(preset_vals[6]))
    hr = slider_val("Heart Rate", "kimjiwon_hr", float(df["hr"].min()), float(df["hr"].max()), float(preset_vals[7]))

    if st.session_state.active_button == "5":
        if st.button("Stres Seviyesini Tahmin Et"):
            bt = (bt_celsius * 9 / 5) + 32
            features = [gsr, rr, bt, lm, bo, rem, sh, hr]
            detect_and_display(x, y, features)

def detect_and_display(x, y, features):
    detection, score = detect(x, y, features)
    st.session_state.stress_level = detection

    st.info("Stres Seviyesi Hesaplandı. Raporlar Gönderiliyor.")

    if detection == 1:
        st.success("Kim Ji-Won has low stress level 🙂")
        st.markdown("### Suggestions:")
        st.markdown("- Great start! **Relax your shoulders**, breathe through your nose, and stay focused.")
    elif detection == 2:
        st.warning("Kim Ji-Won has medium stress level 😐")
        st.markdown("### Suggestions:")
        st.markdown("- Stay composed. **Do a light neck stretch**, take three deep breaths, and reset your rhythm.")
    elif detection == 3:
        st.error("Kim Ji-Won has high stress level! 😞")
        st.markdown("### Suggestions:")
        st.markdown("- Step back for a moment. Use the 4-7-8 breathing technique, **drink lukewarm water**, and gently stretch your fingers.")
    elif detection == 4:
        st.error("Kim Ji-Won has very high stress level!! 😫")
        st.markdown("### Suggestions:")
        st.markdown("- Pause everything. **Rest your eyes for 20 seconds**, do box breathing, and take a deep breath before re-engaging.")
    else:
        st.success("Kim Ji-Won is stress free and calm 😄")
        st.markdown("### Suggestions:")
        st.markdown("- Keep your tempo steady. **Stay hydrated**, breathe easy, and enjoy your performance.")
