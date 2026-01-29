import streamlit as st
import time
import math
from datetime import datetime

st.set_page_config(
    page_title="CO₂ Emission Prediction",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

def inject_css():
    st.markdown(
        """
        <style>
        :root{
            --bg1:#0b1220;
            --bg2:#082a3a;
            --bg3:#1a1040;
            --glass: rgba(255,255,255,0.10);
            --stroke: rgba(255,255,255,0.16);
            --shadow: 0 18px 60px rgba(0,0,0,0.45);
            --txt: rgba(255,255,255,0.92);
            --muted: rgba(255,255,255,0.72);
            --muted2: rgba(255,255,255,0.55);
            --accent: #7CFFB2;
            --accent2: #5DE2FF;
            --warn: #FFD36E;
            --danger: #FF6B8A;
            --radius: 22px;
            --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            --sans: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
        }

        html, body, [class*="css"]{
            font-family: var(--sans) !important;
        }

        .stApp{
            background: transparent;
        }

        .bg-wrap{
            position: fixed;
            inset: 0;
            z-index: -2;
            overflow: hidden;
            background:
                radial-gradient(1200px 700px at 15% 15%, rgba(124,255,178,0.20), transparent 55%),
                radial-gradient(1000px 600px at 85% 25%, rgba(93,226,255,0.18), transparent 55%),
                radial-gradient(900px 600px at 55% 90%, rgba(255,107,138,0.12), transparent 60%),
                linear-gradient(120deg, var(--bg1), var(--bg2), var(--bg3));
            background-size: 200% 200%;
            animation: gradientShift 14s ease-in-out infinite;
        }

        @keyframes gradientShift{
            0%{ background-position: 0% 50%; }
            50%{ background-position: 100% 50%; }
            100%{ background-position: 0% 50%; }
        }

        .blob{
            position: absolute;
            width: 420px;
            height: 420px;
            filter: blur(48px);
            opacity: 0.55;
            border-radius: 999px;
            transform: translate3d(0,0,0);
            mix-blend-mode: screen;
            animation: floaty 10s ease-in-out infinite;
        }
        .blob.b1{ left: -120px; top: 10%; background: rgba(124,255,178,0.35); animation-duration: 12s;}
        .blob.b2{ right: -140px; top: 18%; background: rgba(93,226,255,0.32); animation-duration: 14s;}
        .blob.b3{ left: 35%; bottom: -160px; background: rgba(255,107,138,0.24); animation-duration: 16s;}

        @keyframes floaty{
            0%{ transform: translate(0px,0px) scale(1); }
            50%{ transform: translate(25px,-18px) scale(1.05); }
            100%{ transform: translate(0px,0px) scale(1); }
        }

        section[data-testid="stSidebar"]{
            background: rgba(255,255,255,0.06);
            backdrop-filter: blur(18px);
            border-right: 1px solid rgba(255,255,255,0.10);
        }

        header[data-testid="stHeader"]{
            background: rgba(0,0,0,0) !important;
        }

        .kicker{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            font-family: var(--mono);
            font-size: 12px;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: rgba(255,255,255,0.75);
            padding: 10px 14px;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.14);
            background: rgba(255,255,255,0.06);
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
            width: fit-content;
        }
        .pill-dot{
            width: 8px; height: 8px;
            border-radius: 999px;
            background: var(--accent);
            box-shadow: 0 0 0 6px rgba(124,255,178,0.12);
            animation: pulse 2.4s ease-in-out infinite;
        }
        @keyframes pulse{
            0%{ transform: scale(1); opacity: 1;}
            50%{ transform: scale(1.12); opacity: 0.85;}
            100%{ transform: scale(1); opacity: 1;}
        }

        .h1{
            font-size: clamp(34px, 4vw, 54px);
            font-weight: 780;
            line-height: 1.05;
            letter-spacing: -0.02em;
            color: rgba(255,255,255,0.92);
            margin: 0;
        }
        .sub{
            font-size: 16px;
            color: rgba(255,255,255,0.72);
            line-height: 1.6;
            margin-top: 10px;
            max-width: 72ch;
        }

        .glass{
            background: var(--glass);
            border: 1px solid var(--stroke);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
        }

        .card{
            padding: 18px 18px;
            transition: transform 260ms ease, border-color 260ms ease, background 260ms ease, box-shadow 260ms ease;
        }
        .card:hover{
            transform: translateY(-4px);
            border-color: rgba(255,255,255,0.22);
            background: rgba(255,255,255,0.12);
            box-shadow: 0 24px 70px rgba(0,0,0,0.52);
        }

        .card-title{
            font-size: 14px;
            color: rgba(255,255,255,0.82);
            font-weight: 650;
            letter-spacing: 0.01em;
            margin: 0 0 8px 0;
        }
        .card-value{
            font-size: 28px;
            font-weight: 820;
            letter-spacing: -0.02em;
            color: rgba(255,255,255,0.92);
            margin: 0;
        }
        .card-note{
            font-size: 13px;
            color: rgba(255,255,255,0.55);
            margin-top: 6px;
            line-height: 1.45;
        }

        .stTextInput input, .stNumberInput input, .stTextArea textarea{
            background: rgba(255,255,255,0.08) !important;
            border: 1px solid rgba(255,255,255,0.14) !important;
            color: rgba(255,255,255,0.92) !important;
            border-radius: 14px !important;
            box-shadow: 0 12px 30px rgba(0,0,0,0.18);
        }
        .stSelectbox div[data-baseweb="select"] > div{
            background: rgba(255,255,255,0.08) !important;
            border: 1px solid rgba(255,255,255,0.14) !important;
            border-radius: 14px !important;
            box-shadow: 0 12px 30px rgba(0,0,0,0.18);
        }

        .stButton > button{
            border-radius: 14px !important;
            padding: 10px 14px !important;
            font-weight: 650 !important;
            border: 1px solid rgba(255,255,255,0.16) !important;
            background: rgba(255,255,255,0.10) !important;
            color: rgba(255,255,255,0.92) !important;
            transition: transform 200ms ease, box-shadow 200ms ease, background 200ms ease, border-color 200ms ease !important;
            box-shadow: 0 12px 30px rgba(0,0,0,0.25) !important;
        }
        .stButton > button:hover{
            transform: translateY(-2px);
            background: rgba(255,255,255,0.14) !important;
            border-color: rgba(255,255,255,0.24) !important;
            box-shadow: 0 18px 45px rgba(0,0,0,0.34) !important;
        }

        .divider{
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent);
            margin: 18px 0;
        }

        .ring{
            width: 44px;
            height: 44px;
            border-radius: 999px;
            border: 4px solid rgba(255,255,255,0.16);
            border-top-color: rgba(124,255,178,0.85);
            animation: spin 0.9s linear infinite;
            margin: 6px auto 0 auto;
        }
        @keyframes spin{
            to{ transform: rotate(360deg); }
        }

        .footer{
            margin-top: 26px;
            padding: 16px 18px;
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,0.12);
            background: rgba(255,255,255,0.06);
            color: rgba(255,255,255,0.62);
            text-align: center;
        }

        footer {visibility: hidden;}
        </style>

        <div class="bg-wrap">
            <div class="blob b1"></div>
            <div class="blob b2"></div>
            <div class="blob b3"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def init_state():
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    if "last_pred" not in st.session_state:
        st.session_state.last_pred = None
    if "history" not in st.session_state:
        st.session_state.history = []
    if "units" not in st.session_state:
        st.session_state.units = "kg CO₂"
    if "precision" not in st.session_state:
        st.session_state.precision = 2

def sidebar_nav():
    with st.sidebar:
        st.markdown(
            """
            <div style="padding: 14px 12px 6px 12px;">
                <div class="kicker"><span class="pill-dot"></span> CO₂ Prediction Suite</div>
                <div style="height:10px;"></div>
                <div style="color: rgba(255,255,255,0.72); font-size: 13px; line-height: 1.5;">
                    Predict emissions with a model-ready interface and polished UI.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        page = st.radio(
            "Navigation",
            ["Dashboard", "Predict", "Insights", "About"],
            index=["Dashboard", "Predict", "Insights", "About"].index(st.session_state.page),
        )
        st.session_state.page = page

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("**Preferences**")
        st.session_state.units = st.selectbox("Output Units", ["kg CO₂", "t CO₂"], index=0)
        st.session_state.precision = st.slider("Display Precision", 0, 4, 2)

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def format_emission(value_kg):
    if st.session_state.units == "t CO₂":
        return f"{value_kg/1000:.{st.session_state.precision}f} t CO₂"
    return f"{value_kg:.{st.session_state.precision}f} kg CO₂"

def dummy_predict(distance_km, fuel_type, vehicle_type, passengers, payload_kg, avg_speed_kmph):
    fuel_factor = {"Petrol": 0.192, "Diesel": 0.171, "CNG": 0.120, "Electric": 0.050}.get(fuel_type, 0.180)
    vehicle_factor = {"Car": 1.00, "Bike": 0.35, "Bus": 0.22, "Truck": 1.75, "Train": 0.12, "Flight": 2.90}.get(vehicle_type, 1.00)

    speed_penalty = 1.0 + clamp((avg_speed_kmph - 60.0) / 180.0, -0.15, 0.35)
    passenger_factor = 1.0 / clamp(passengers, 1, 6)
    payload_factor = 1.0 + clamp(payload_kg / 1200.0, 0.0, 0.8)

    base = distance_km * 1000.0 * fuel_factor * vehicle_factor * speed_penalty * payload_factor * passenger_factor
    noise = (math.sin(distance_km * 0.12) + math.cos(avg_speed_kmph * 0.05)) * 0.02
    base = base * (1.0 + noise)

    return clamp(base, 0.0, 1e9)

def risk_band(value_kg):
    if value_kg < 2.5:
        return "Low", "rgba(124,255,178,0.18)"
    if value_kg < 12.0:
        return "Moderate", "rgba(255,211,110,0.18)"
    return "High", "rgba(255,107,138,0.18)"

def render_hero():
    left, right = st.columns([1.35, 0.65], gap="large")
    with left:
        st.markdown(
            """
            <div class="glass card" style="padding: 22px 22px;">
                <div class="kicker"><span class="pill-dot"></span> CO₂ Emission Prediction</div>
                <div style="height: 12px;"></div>
                <h1 class="h1">Estimate emissions with a model-ready interface.</h1>
                <p class="sub">
                    Enter trip details, run a prediction, and review results instantly with a clean UI.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            f"""
            <div class="glass card" style="padding: 18px 18px;">
                <div class="card-title">Today</div>
                <div class="card-value" style="font-size: 22px;">{datetime.now().strftime("%b %d, %Y")}</div>
                <div class="card-note">System time • {datetime.now().strftime("%H:%M:%S")}</div>
                <div style="height: 10px;"></div>
                <div class="divider"></div>
                <div class="card-title">Status</div>
                <div class="card-note">Inference ready • Dummy model active</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

def render_input_section():
    st.markdown(
        """
        <div class="glass card" style="padding: 18px 18px;">
            <div class="card-title" style="font-size: 15px;">Input Section</div>
            <div style="color: rgba(255,255,255,0.60); font-size: 13px; margin-top: -2px;">
                Model placeholder inputs • structured for ML deployment
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1], gap="large")

    with c1:
        distance_km = st.number_input("Distance (km)", min_value=0.0, value=12.0, step=1.0)
        fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "Electric"])
    with c2:
        vehicle_type = st.selectbox("Vehicle Type", ["Car", "Bike", "Bus", "Truck", "Train", "Flight"])
        passengers = st.number_input("Passengers", min_value=1, value=1, step=1)
    with c3:
        payload_kg = st.number_input("Payload (kg)", min_value=0.0, value=0.0, step=10.0)
        avg_speed_kmph = st.number_input("Average Speed (km/h)", min_value=1.0, value=55.0, step=1.0)

    st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)

    run_col1, run_col2 = st.columns([0.25, 0.75], gap="large")
    with run_col1:
        run = st.button("Run Prediction", use_container_width=True)
    with run_col2:
        st.caption("Click **Run Prediction** to generate CO₂ estimate and result cards.")

    return run, {
        "distance_km": distance_km,
        "fuel_type": fuel_type,
        "vehicle_type": vehicle_type,
        "passengers": passengers,
        "payload_kg": payload_kg,
        "avg_speed_kmph": avg_speed_kmph,
    }

def render_loading():
    box = st.container()
    with box:
        st.markdown(
            """
            <div class="glass card" style="padding: 18px 18px; text-align:center;">
                <div class="card-title">Running model inference</div>
                <div class="card-note">Preparing features • Executing prediction • Rendering results</div>
                <div class="ring"></div>
                <div style="height: 10px;"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        prog = st.progress(0)
        for i in range(101):
            time.sleep(0.008)
            prog.progress(i)
        time.sleep(0.08)

def render_results(pred_kg, inputs):
    band, tint = risk_band(pred_kg)
    pretty = format_emission(pred_kg)

    st.markdown(
        """
        <div class="glass card" style="padding: 18px 18px;">
            <div class="card-title" style="font-size: 15px;">Result Display</div>
            <div style="color: rgba(255,255,255,0.60); font-size: 13px; margin-top: -2px;">
                Predicted emissions • summary metrics • interpretation
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)

    r1, r2, r3 = st.columns([1, 1, 1], gap="large")
    with r1:
        st.markdown(
            f"""
            <div class="glass card" style="padding: 18px 18px;">
                <div class="card-title">Predicted CO₂</div>
                <div class="card-value">{pretty}</div>
                <div class="card-note">Estimated based on inputs (dummy model)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with r2:
        st.markdown(
            f"""
            <div class="glass card" style="padding: 18px 18px; background: {tint};">
                <div class="card-title">Emission Band</div>
                <div class="card-value">{band}</div>
                <div class="card-note">Low / Moderate / High interpretation</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with r3:
        per_km = pred_kg / max(inputs["distance_km"], 0.001)
        st.markdown(
            f"""
            <div class="glass card" style="padding: 18px 18px;">
                <div class="card-title">Intensity</div>
                <div class="card-value">{format_emission(per_km)}</div>
                <div class="card-note">Per km (normalized estimate)</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    with st.expander("View Input Summary", expanded=False):
        st.json(inputs)

def render_footer():
    st.markdown(
        f"""
        <div class="footer">
            CO₂ Emission Prediction • Streamlit UI • {datetime.now().strftime("%Y")} • Model-ready demo interface
        </div>
        """,
        unsafe_allow_html=True,
    )

def page_dashboard():
    render_hero()
    st.markdown('<div style="height: 14px;"></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1], gap="large")
    with c1:
        st.markdown(
            """
            <div class="glass card">
                <div class="card-title">Fast Setup</div>
                <div class="card-value" style="font-size: 22px;">Streamlit-first</div>
                <div class="card-note">Optimized layout with glass cards and transitions.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="glass card">
                <div class="card-title">Inference Flow</div>
                <div class="card-value" style="font-size: 22px;">Feature → Predict</div>
                <div class="card-note">Dummy logic now, plug your ML model anytime.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        last = st.session_state.last_pred
        last_txt = "—" if last is None else format_emission(last)
        st.markdown(
            f"""
            <div class="glass card">
                <div class="card-title">Last Result</div>
                <div class="card-value" style="font-size: 22px;">{last_txt}</div>
                <div class="card-note">Most recent prediction in this session.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_footer()

def page_predict():
    render_hero()
    st.markdown('<div style="height: 14px;"></div>', unsafe_allow_html=True)

    run, inputs = render_input_section()

    if run:
        render_loading()
        pred_kg = dummy_predict(
            distance_km=inputs["distance_km"],
            fuel_type=inputs["fuel_type"],
            vehicle_type=inputs["vehicle_type"],
            passengers=int(inputs["passengers"]),
            payload_kg=inputs["payload_kg"],
            avg_speed_kmph=inputs["avg_speed_kmph"],
        )
        st.session_state.last_pred = pred_kg
        st.session_state.history.append(
            {
                "ts": datetime.now().isoformat(timespec="seconds"),
                "inputs": inputs,
                "pred_kg": pred_kg,
            }
        )
        render_results(pred_kg, inputs)
    else:
        st.markdown(
            """
            <div class="glass card" style="padding: 18px 18px;">
                <div class="card-title">Waiting for prediction</div>
                <div class="card-note">Fill inputs and click <b>Run Prediction</b> to see results here.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_footer()

def page_insights():
    render_hero()
    st.markdown('<div style="height: 14px;"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="glass card" style="padding: 18px 18px;">
            <div class="card-title" style="font-size: 15px;">Insights</div>
            <div style="color: rgba(255,255,255,0.60); font-size: 13px; margin-top: -2px;">
                Session history • quick summaries • model-ready analytics
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown(
            """
            <div class="glass card">
                <div class="card-title">No predictions yet</div>
                <div class="card-note">Run a prediction in the Predict page to populate insights.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_footer()
        return

    total = sum(item["pred_kg"] for item in st.session_state.history)
    avg = total / len(st.session_state.history)
    best = min(item["pred_kg"] for item in st.session_state.history)
    worst = max(item["pred_kg"] for item in st.session_state.history)

    a, b, c, d = st.columns([1, 1, 1, 1], gap="large")
    with a:
        st.markdown(
            f"""
            <div class="glass card">
                <div class="card-title">Total CO₂</div>
                <div class="card-value" style="font-size: 22px;">{format_emission(total)}</div>
                <div class="card-note">Sum of session predictions</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with b:
        st.markdown(
            f"""
            <div class="glass card">
                <div class="card-title">Average</div>
                <div class="card-value" style="font-size: 22px;">{format_emission(avg)}</div>
                <div class="card-note">Mean emission per run</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c:
        st.markdown(
            f"""
            <div class="glass card">
                <div class="card-title">Best (Lowest)</div>
                <div class="card-value" style="font-size: 22px;">{format_emission(best)}</div>
                <div class="card-note">Lowest emission scenario</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with d:
        st.markdown(
            f"""
            <div class="glass card">
                <div class="card-title">Worst (Highest)</div>
                <div class="card-value" style="font-size: 22px;">{format_emission(worst)}</div>
                <div class="card-note">Highest emission scenario</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.dataframe(
        [
            {
                "timestamp": item["ts"],
                "distance_km": item["inputs"]["distance_km"],
                "vehicle": item["inputs"]["vehicle_type"],
                "fuel": item["inputs"]["fuel_type"],
                "passengers": item["inputs"]["passengers"],
                "payload_kg": item["inputs"]["payload_kg"],
                "avg_speed": item["inputs"]["avg_speed_kmph"],
                "pred_kg": round(item["pred_kg"], 4),
            }
            for item in reversed(st.session_state.history)
        ],
        use_container_width=True,
        hide_index=True,
    )

    render_footer()

def page_about():
    render_hero()
    st.markdown('<div style="height: 14px;"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="glass card" style="padding: 18px 18px;">
            <div class="card-title" style="font-size: 15px;">About</div>
            <div style="color: rgba(255,255,255,0.60); font-size: 13px; margin-top: -2px;">
                A production-style Streamlit layout for CO₂ emission prediction demos.
            </div>
            <div style="height: 12px;"></div>
            <div class="divider"></div>
            <div style="color: rgba(255,255,255,0.70); font-size: 14px; line-height: 1.7;">
                This app includes a structured ML input form, a dummy prediction function (replaceable with your trained model),
                result cards, session insights, and a polished UI with animated background and glassmorphism styling.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_footer()

def main():
    inject_css()
    init_state()
    sidebar_nav()

    if st.session_state.page == "Dashboard":
        page_dashboard()
    elif st.session_state.page == "Predict":
        page_predict()
    elif st.session_state.page == "Insights":
        page_insights()
    else:
        page_about()

if __name__ == "__main__":
    main()

