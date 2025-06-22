import streamlit as st
from web_functions import detect

def app(df, x, y):
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # CSS for buttons ONLY in the main page (not sidebar)
    main_page_button_css = """
    <style>
        /* Target ONLY buttons inside the main block (not sidebar) */
        div.block-container div.stButton > button,
        div.stApp > div:first-child > div > div > div.stButton > button {
            font-family: 'Rajdhani', sans-serif;
            font-weight: bold;
            border: 2px solid #4a4a4a;
            border-radius: 8px;
            background-color: #1e1e1e;
            color: white;
            padding: 0.5rem 1rem;
            transition: all 0.3s;
            width: 100%;
        }

        /* Hover effect (main page buttons only) */
        div.block-container div.stButton > button:hover,
        div.stApp > div:first-child > div > div > div.stButton > button:hover {
            background-color: #2e2e2e;
            border-color: #5a5a5a;
            color: #ff4b4b;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        /* Active state (main page buttons only) */
        div.block-container div.stButton > button:active,
        div.stApp > div:first-child > div > div > div.stButton > button:active {
            background-color: #ff4b4b;
            color: white;
            transform: translateY(0);
        }

        /* Focus state (main page buttons only) */
        div.block-container div.stButton > button:focus:not(:active),
        div.stApp > div:first-child > div > div > div.stButton > button:focus:not(:active) {
            box-shadow: 0 0 0 0.2rem rgba(255, 75, 75, 0.5);
        }

        /* Game stats buttons (5-column layout) */
        div.block-container div[data-testid="column"] > div.stButton > button {
            background: linear-gradient(145deg, #1a1a1a, #252525);
        }
    </style>
    """
    st.markdown(main_page_button_css, unsafe_allow_html=True)

    # Initialize page-specific session state variables
    if "maide_active_button" not in st.session_state:
        st.session_state.maide_active_button = "5"
    if "maide_show_suggestion" not in st.session_state:
        st.session_state.maide_show_suggestion = False

    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("images/maide.jpeg", use_container_width=True, width=200)
    with col2:
        st.markdown("<div class='big-title'>Maide Sarı / Entry 🔴</div>", unsafe_allow_html=True)
        st.markdown("<div class='big-title-second'>Current Character: <span class='optimal'>Jett</span></div>", unsafe_allow_html=True)       
        st.markdown("<div class='big-title-second'>Current Status: <span class='critical'>Critical</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='big-title-second'>Currently Playing: <span class='critical'>Competitive</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='big-title-second'>Current Game Status: <span class='optimal'>Pratice Mode</span></div>", unsafe_allow_html=True)

    st.markdown("<div class='sub-title'>Overall Game Status</div>", unsafe_allow_html=True)
    game_cols = st.columns(5)
    with game_cols[0]:
        st.markdown("<div class='game-status-item'>13-9</div>", unsafe_allow_html=True)
    with game_cols[1]:
        st.markdown("<div class='game-status-item'>15-13</div>", unsafe_allow_html=True)
    with game_cols[2]:
        st.markdown("<div class='game-status-item'>8-13</div>", unsafe_allow_html=True)
    with game_cols[3]:
        st.markdown("<div class='game-status-item'>6-13</div>", unsafe_allow_html=True)
    with game_cols[4]:
        st.markdown("<div class='game-status-item current'>CURRENT</div>", unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([1, 6, 1])
    with col_center:
        st.image("images/score_panel.png", use_container_width=True)

    st.markdown("<div class='sub-title'>Overall Game Stress Predictions</div>", unsafe_allow_html=True)

    presets = {
        "1": [98, 25, 98.6, 10.5, 96.2, 90.1, 3.5, 70],
        "2": [100, 20, 96.6, 18.5, 96.2, 90.1, 4.5, 68],
        "3": [97, 27, 98.2, 16.5, 94.2, 93.1, 5.5, 65],
        "4": [92, 24, 96.5, 13.5, 94.2, 93.1, 6.5, 72],
    }

    with st.container():
        st.markdown('<div class="game-button-panel">', unsafe_allow_html=True)

        colb1, colb2, colb3, colb4, colb5 = st.columns(5)
        if colb1.button("1.Game Stats"):
            st.session_state.maide_active_button = "1"
            detect_and_display(x, y, presets["1"])
            st.session_state.maide_show_suggestion = True
        if colb2.button("2.Game Stats"):
            st.session_state.maide_active_button = "2"
            detect_and_display(x, y, presets["2"])
            st.session_state.maide_show_suggestion = True
        if colb3.button("3.Game Stats"):
            st.session_state.maide_active_button = "3"
            detect_and_display(x, y, presets["3"])
            st.session_state.maide_show_suggestion = True
        if colb4.button("4.Game Stats"):
            st.session_state.maide_active_button = "4"
            detect_and_display(x, y, presets["4"])
            st.session_state.maide_show_suggestion = True
        if colb5.button("Current Game"):
            st.session_state.maide_active_button = "5"
            st.session_state.maide_show_suggestion = False
            st.session_state.pop("maide_stress_level", None)

        st.markdown('</div>', unsafe_allow_html=True)

    bt_min_c = round((df["bt"].min() - 32) * 5 / 9, 1)
    bt_max_c = round((df["bt"].max() - 32) * 5 / 9, 1)
    readonly = st.session_state.maide_active_button != "5"

    def slider_val(label, key, minv, maxv, default):
        return st.slider(label, minv, maxv, value=default, disabled=readonly, key=key)

    if st.session_state.maide_active_button in presets:
        preset_vals = presets[st.session_state.maide_active_button]
    else:
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

    has_suggestion = st.session_state.get("maide_show_suggestion", False)

    if has_suggestion:
        slider_col, separator_col, suggestion_col = st.columns([3, 0.05, 2])
    else:
        slider_col = st.container()
        separator_col = None
        suggestion_col = None

    with slider_col:
        st.markdown("<h3 class='AI-label'>Biometric Data</h3>", unsafe_allow_html=True)

        gsr = slider_val("GSR Data", "maide_gsr", int(df["gsr"].min()), int(df["gsr"].max()), int(preset_vals[0]))
        rr = slider_val("Respiration Rate", "maide_rr", int(df["rr"].min()), int(df["rr"].max()), int(preset_vals[1]))
        bt_celsius = slider_val(
            "Body Temperature (in °C)", "maide_bt", bt_min_c, bt_max_c,
            round((preset_vals[2] - 32) * 5 / 9, 1)
        )
        lm = slider_val("Limb Movement", "maide_lm", float(df["lm"].min()), float(df["lm"].max()), float(preset_vals[3]))
        bo = slider_val("Blood Oxygen(%)", "maide_bo", float(df["bo"].min()), float(df["bo"].max()), float(preset_vals[4]))
        rem = slider_val("Hand Tremors", "maide_rem", float(df["rem"].min()), float(df["rem"].max()), float(preset_vals[5]))
        sh = slider_val("Sleeping Hour", "maide_sh", float(df["sh"].min()), float(df["sh"].max()), float(preset_vals[6]))
        hr = slider_val("Heart Rate", "maide_hr", float(df["hr"].min()), float(df["hr"].max()), float(preset_vals[7]))

    if has_suggestion and separator_col is not None:
        with separator_col:
            st.markdown(
                "<div class='vertical-separator' style='height:100%; min-height:300px;'></div>",
                unsafe_allow_html=True
            )

    if has_suggestion and suggestion_col is not None:
        with suggestion_col:
            st.markdown("<h3 class='AI-label'>AI Suggestions</h3>", unsafe_allow_html=True)
            show_suggestion(st.session_state.get("maide_stress_level"))

    if st.session_state.maide_active_button == "5":
        if st.button("Predict User Stress Level"):
            bt = (bt_celsius * 9 / 5) + 32
            features = [gsr, rr, bt, lm, bo, rem, sh, hr]
            detect_and_display(x, y, features)
            st.session_state.maide_show_suggestion = True
            st.rerun()

def detect_and_display(x, y, features):
    detection, score = detect(x, y, features)
    st.session_state.maide_stress_level = detection
    st.info("Stress Level Calculated. Reports are being sent.")

def show_suggestion(detection):
    if detection == 1:
        st.success("Low Stress Level")
        st.markdown("<div class='suggestion-box'>- Stay sharp and composed.<br>- Breathe steadily.<br>- <b>Drink water regularly</b>.</div>", unsafe_allow_html=True)
    elif detection == 2:
        st.warning("Medium Stress Level")
        st.markdown("<div class='suggestion-box'>- Take mental resets.<br>- Stay calm.<br>- <b>Splash cool water</b> on your face.</div>", unsafe_allow_html=True)
    elif detection == 3:
        st.error("High Stress Level!")
        st.markdown("<div class='suggestion-box'>- Use 4-7-8 breathing.<br>- <b>Drink cold water</b>.<br>- Stretch and fix posture.</div>", unsafe_allow_html=True)
    elif detection == 4:
        st.error("Very High Stress Level!!")
        st.markdown("<div class='suggestion-box'>- Take a timeout.<br>- Try box breathing.<br>- <b>Drink an isotonic beverage</b>.</div>", unsafe_allow_html=True)
    else:
        st.success("Stress Free and Calm")
        st.markdown("<div class='suggestion-box'>- Maintain rhythm.<br>- <b>Sip water</b>.<br>- Stay focused and refreshed.</div>", unsafe_allow_html=True)