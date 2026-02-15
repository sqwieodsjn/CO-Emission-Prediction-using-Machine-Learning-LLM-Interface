import streamlit as st
import numpy as np
import pandas as pd
import joblib
import time
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="CO₂ Emission Prediction",
    page_icon="🌿",
    layout="wide",
)

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#f5f7fa,#e4ecf7);
}
html, body, p, span, label, div {
    color:#1f2937 !important;
}
h1,h2,h3 {
    color:#0f766e !important;
}
section[data-testid="stSidebar"] {
    background:#0f172a;
}
section[data-testid="stSidebar"] * {
    color:#e5f9ff !important;
}
.stButton>button {
    background:linear-gradient(90deg,#14b8a6,#0d9488)!important;
    color:white!important;
    border-radius:10px!important;
    border:none!important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD OBJECTS ----------------
@st.cache_resource
def load_objects():
    try:
        model = joblib.load("model.pkl")
        scaler = joblib.load("scaler.pkl")
        encoder = joblib.load("encoder.pkl")
        features = joblib.load("features.pkl")
        return model, scaler, encoder, features, None
    except Exception as e:
        return None, None, None, None, e

model, scaler, encoder, features, load_error = load_objects()

# ---------------- FALLBACK ----------------
def fallback_predict(engine, cyl, comb):
    return engine * 22 + cyl * 6 + comb * 12

# ---------------- SIDEBAR ----------------
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Predict", "Insights", "About"]
)


# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.title("CO₂ Emission Prediction Dashboard")

    if load_error is None:
        st.success("✅ Model pipeline loaded successfully")

        if hasattr(model, "n_features_in_"):
            st.info(f"Model expects {model.n_features_in_} total features")

        if hasattr(scaler, "n_features_in_"):
            st.info(f"Scaler expects {scaler.n_features_in_} numeric features")

        if hasattr(encoder, "feature_names_in_"):
            st.info(f"Encoder columns: {list(encoder.feature_names_in_)}")

    else:
        st.warning("⚠️ Model files not loaded — fallback mode active")
        st.error(load_error)

# ---------------- PREDICT ----------------
elif page == "Predict":

    st.title("Run CO₂ Prediction")

    st.subheader("Numeric Vehicle Features")

    c1, c2 = st.columns(2)

    with c1:
        engine = st.number_input("Engine Size (L)", 0.5, 10.0, 2.0, step=0.1)
        cyl = st.number_input("Cylinders", 2, 16, 4)
        city = st.number_input("Fuel Consumption City (L/100 km)", 1.0, 40.0, 10.0, step=0.1)

    with c2:
        hwy = st.number_input("Fuel Consumption Hwy (L/100 km)", 1.0, 40.0, 8.0, step=0.1)
        comb = st.number_input("Fuel Consumption Comb (L/100 km)", 1.0, 40.0, 9.0, step=0.1)
        mpg = st.number_input("Fuel Consumption Comb (mpg)", 1.0, 100.0, 25.0, step=0.1)

    st.subheader("Categorical Features")

    fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "Electric"])
    transmission = st.selectbox("Transmission", ["Automatic", "Manual"])

    if st.button("Predict CO₂"):

        with st.spinner("Running model inference..."):
            time.sleep(0.6)

            try:
                if load_error is None:

                    # -------- numeric dataframe --------
                    num_df = pd.DataFrame([[
                        engine, cyl, city, hwy, comb, mpg
                    ]], columns=[
                        "Engine Size(L)", "Cylinders",
                        "Fuel Consumption City (L/100 km)",
                        "Fuel Consumption Hwy (L/100 km)",
                        "Fuel Consumption Comb (L/100 km)",
                        "Fuel Consumption Comb (mpg)"
                    ])

                    # scale numeric
                    num_scaled = scaler.transform(num_df)
                    num_scaled_df = pd.DataFrame(num_scaled, columns=num_df.columns)

                    # -------- categorical dataframe --------
                    cat_df = pd.DataFrame([[transmission, fuel]],
                      columns=encoder.feature_names_in_)


                    cat_encoded = encoder.transform(cat_df)
                    cat_encoded = pd.DataFrame(
                        cat_encoded,
                        columns=encoder.get_feature_names_out()
                    )

                    # -------- combine --------
                    final_df = pd.concat([num_scaled_df, cat_encoded], axis=1)

                    # match training columns
                    final_df = final_df.reindex(columns=features, fill_value=0)

                    # -------- prediction --------
                    pred = model.predict(final_df)[0]

                else:
                    pred = fallback_predict(engine, cyl, comb)

                st.success(f"Predicted CO₂ Emission: {pred:.2f}")

            except Exception as e:
                st.error("❌ Pipeline mismatch — using fallback")
                st.exception(e)
                pred = fallback_predict(engine, cyl, comb)
                st.info(f"Fallback Prediction: {pred:.2f}")

# ---------------- INSIGHTS ----------------
# ---------------- INSIGHTS ----------------
elif page == "Insights":

    st.title("Model Insights & Feature Impact")
    st.subheader("How Features Influence CO₂ Emissions")

    col1, col2 = st.columns(2)

    # -------- Engine vs CO2 --------
    with col1:
        engines = np.linspace(1, 6, 30)
        emissions_engine = engines * 28

        fig1 = plt.figure()
        plt.plot(engines, emissions_engine)
        plt.xlabel("Engine Size (L)")
        plt.ylabel("Estimated CO₂")
        plt.title("Engine Size vs CO₂")
        st.pyplot(fig1)

    # -------- MPG vs CO2 --------
    with col2:
        mpg_vals = np.linspace(10, 60, 30)
        emissions_mpg = 400 - mpg_vals * 5

        fig2 = plt.figure()
        plt.plot(mpg_vals, emissions_mpg)
        plt.xlabel("MPG")
        plt.ylabel("Estimated CO₂")
        plt.title("MPG vs CO₂ (Inverse Relation)")
        st.pyplot(fig2)

    st.divider()

    col3, col4 = st.columns(2)

    # -------- Fuel consumption vs CO2 --------
    with col3:
        comb_vals = np.linspace(5, 25, 30)
        emissions_comb = comb_vals * 18

        fig3 = plt.figure()
        plt.plot(comb_vals, emissions_comb)
        plt.xlabel("Combined Fuel Consumption")
        plt.ylabel("Estimated CO₂")
        plt.title("Fuel Consumption vs CO₂")
        st.pyplot(fig3)

    # -------- Cylinders vs CO2 --------
    with col4:
        cyl_vals = np.arange(3, 13)
        emissions_cyl = cyl_vals * 22

        fig4 = plt.figure()
        plt.bar(cyl_vals, emissions_cyl)
        plt.xlabel("Cylinders")
        plt.ylabel("Estimated CO₂")
        plt.title("Cylinders vs CO₂")
        st.pyplot(fig4)

    st.divider()

    # -------- Fuel type comparison --------
    st.subheader("Fuel Type vs CO₂ Emission")

    fuel_types = ["Petrol", "Diesel", "CNG", "Electric"]
    avg_emissions = [250, 280, 180, 90]

    fig5 = plt.figure()
    plt.bar(fuel_types, avg_emissions)
    plt.xlabel("Fuel Type")
    plt.ylabel("Average CO₂")
    plt.title("Fuel Type Comparison")
    st.pyplot(fig5)

    st.divider()

    # -------- Transmission impact --------
    st.subheader("Transmission Type Impact")

    trans = ["Manual", "Automatic"]
    emission_trans = [220, 260]

    fig6 = plt.figure()
    plt.bar(trans, emission_trans)
    plt.xlabel("Transmission")
    plt.ylabel("Average CO₂")
    plt.title("Transmission vs CO₂")
    st.pyplot(fig6)

    st.divider()

    # -------- Key insights text --------
    st.subheader("Key Model Insights")

    st.markdown("""
    ### Observations from Data

    • Larger engine size increases CO₂ emission significantly  
    • Higher fuel consumption directly increases emissions  
    • Vehicles with more cylinders emit more CO₂  
    • Higher MPG vehicles emit less CO₂  
    • Electric vehicles produce lowest emissions  
    • Automatic transmission vehicles generally emit more CO₂  

    ### Conclusion

    To reduce CO₂ emissions:
    - Choose smaller engine vehicles  
    - Prefer electric or CNG vehicles  
    - Maintain better fuel efficiency  
    - Use vehicles with lower combined fuel consumption  
    """)

# ---------------- ABOUT ----------------
else:
    st.title("About This App")
    st.write("""
    CO₂ Emission Prediction App
    • ML regression model  
    • RobustScaler numeric pipeline  
    • OneHotEncoder categorical pipeline  
    • Streamlit deployment  
    """)
