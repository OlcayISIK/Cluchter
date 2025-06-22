import streamlit as st
from web_functions import detect

def app(df, x, y):
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    if "active_button" not in st.session_state:
        st.session_state.active_button = "5"

    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("images/hong-joshua.png", use_container_width=True, width=200)
    with col2:
        st.markdown("<div class='big-title'>Hong Joshua (Brimstone)</div>", unsafe_allow_html=True)
        st.markdown("<div class='big-title-second'>Current Status: <span class='optimal'>Optimal</span></div>", unsafe_allow_html=True)

    st.markdown("<div class='sub-title'>Overall Game Stress Predictions</div>", unsafe_allow_html=True)

    presets = {
        "1": [90, 25, 97.6, 14.5, 92.2, 90.1, 6.5, 70],
        "2": [92, 23, 97.2, 15.5, 91.2, 89.1, 7.5, 68],
        "3": [46, 25, 96.8, 16.5, 96.2, 90.8, 6.0, 65],
        "4": [98, 22, 97.6, 4.0, 96.8, 88.9, 6.5, 66]
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

    gsr = slider_val("GSR Data", "john_gsr", int(df["gsr"].min()), int(df["gsr"].max()), int(preset_vals[0]))
    rr = slider_val("Respiration Rate", "john_rr", int(df["rr"].min()), int(df["rr"].max()), int(preset_vals[1]))
    bt_celsius = slider_val(
        "Body Temperature (in °C)", "john_bt", bt_min_c, bt_max_c,
        round((preset_vals[2] - 32) * 5 / 9, 1)
    )
    lm = slider_val("Limb Movement", "john_lm", float(df["lm"].min()), float(df["lm"].max()), float(preset_vals[3]))
    bo = slider_val("Blood Oxygen(%)", "john_bo", float(df["bo"].min()), float(df["bo"].max()), float(preset_vals[4]))
    rem = slider_val("Mouse Squeeze Muscle Tone", "john_rem", float(df["rem"].min()), float(df["rem"].max()), float(preset_vals[5]))
    sh = slider_val("Sleeping Hour", "john_sh", float(df["sh"].min()), float(df["sh"].max()), float(preset_vals[6]))
    hr = slider_val("Heart Rate", "john_hr", float(df["hr"].min()), float(df["hr"].max()), float(preset_vals[7]))

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
        st.success("Hong Joshua has low stress level")
        st.markdown("### Suggestions:")
        st.markdown("- Maintain steady focus. **Roll your shoulders back** and stay loose to stay in the zone.")
    elif detection == 2:
        st.warning("Hong Joshua has medium stress level")
        st.markdown("### Suggestions:")
        st.markdown("- Keep your cool. **Do a quick wrist rotation**, breathe evenly, and reset your mental pace.")
    elif detection == 3:
        st.error("Hong Joshua has high stress level!")
        st.markdown("### Suggestions:")
        st.markdown("- Take a short pause and use the 4-7-8 breathing method. **Loosen your jaw**, take a sip of water, and get back with fresh eyes.")
    elif detection == 4:
        st.error("Hong Joshua has very high stress level!!")
        st.markdown("### Suggestions:")
        st.markdown("- Call a hard timeout. **Close your eyes for 10 seconds**, practice box breathing, and drink some cool water before returning.")
    else:
        st.success("Hong Joshua is stress free and calm")
        st.markdown("### Suggestions:")
        st.markdown("- You're in the flow! **Maintain relaxed posture**, sip some water, and keep cruising.")
