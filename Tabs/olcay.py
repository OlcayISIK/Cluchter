import streamlit as st
from web_functions import detect

def app(df, x, y):
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    if "active_button" not in st.session_state:
        st.session_state.active_button = "5"

    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("images/olcay.jpeg", use_container_width=True, width=200)
    with col2:
        st.markdown("<div class='big-title'>Olcay Işık (Omen)</div>", unsafe_allow_html=True)
        st.markdown("<div class='big-title-second'>Current Status: <span class='optimal'>Optimal</span></div>", unsafe_allow_html=True)

    st.markdown("<div class='sub-title'>Overall Game Stress Predictions</div>", unsafe_allow_html=True)

    presets = {
        "1": [50, 20, 96.5, 10.5, 90.1, 70.1, 8.0, 70],
        "2": [48, 25, 96.8, 14.5, 96.2, 90.1, 7.5, 65],
        "3": [70, 23, 96.5, 13.5, 94.2, 83.1, 6.5, 72],
        "4": [58, 22, 98.4, 12.0, 94.8, 78.4, 5.5, 68]
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

    gsr = slider_val("GSR Data", "olcay_gsr", int(df["gsr"].min()), int(df["gsr"].max()), int(preset_vals[0]))
    rr = slider_val("Respiration Rate", "olcay_rr", int(df["rr"].min()), int(df["rr"].max()), int(preset_vals[1]))
    bt_celsius = slider_val(
        "Body Temperature (in °C)", "olcay_bt", bt_min_c, bt_max_c,
        round((preset_vals[2] - 32) * 5 / 9, 1)
    )
    lm = slider_val("Limb Movement", "olcay_lm", float(df["lm"].min()), float(df["lm"].max()), float(preset_vals[3]))
    bo = slider_val("Blood Oxygen(%)", "olcay_bo", float(df["bo"].min()), float(df["bo"].max()), float(preset_vals[4]))
    rem = slider_val("Mouse Squeeze Muscle Tone", "olcay_rem", float(df["rem"].min()), float(df["rem"].max()), float(preset_vals[5]))
    sh = slider_val("Sleeping Hour", "olcay_sh", float(df["sh"].min()), float(df["sh"].max()), float(preset_vals[6]))
    hr = slider_val("Heart Rate", "olcay_hr", float(df["hr"].min()), float(df["hr"].max()), float(preset_vals[7]))

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
        st.success("Olcay Işık has low stress level")
        st.markdown("### Suggestions:")
        st.markdown("- Stay focused and centered. **Take a few deep breaths** to reinforce calm and readiness.")
    elif detection == 2:
        st.warning("Olcay Işık has medium stress level")
        st.markdown("### Suggestions:")
        st.markdown("- Remain calm. Use short mental resets and **perform a quick breathing drill** to stay composed.")
    elif detection == 3:
        st.error("Olcay Işık has high stress level!")
        st.markdown("### Suggestions:")
        st.markdown("- Pause briefly and reset with 4-7-8 breathing. **Take deep, slow breaths**, loosen your grip, and refocus.")
    elif detection == 4:
        st.error("Olcay Işık has very high stress level!!")
        st.markdown("### Suggestions:")
        st.markdown("- Take a full break from the game. Practice box breathing, **stretch your arms**, and visualize the next round calmly.")
    else:
        st.success("Olcay Işık is stress free and calm")
        st.markdown("### Suggestions:")
        st.markdown("- Keep the rhythm. Stay aware, **breathe steadily**, and maintain focus.")