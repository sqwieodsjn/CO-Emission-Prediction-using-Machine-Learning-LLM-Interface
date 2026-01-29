# 🌿 CO₂ Emission Prediction using Machine Learning & LLM Interface

A Machine Learning based CO₂ Emission Prediction system built using **Linear Regression** with an interactive **Streamlit UI** and an LLM-style user interface for intelligent, user-friendly emission estimation.

This project predicts carbon dioxide emissions based on transport and trip-related features such as distance, fuel type, vehicle type, passengers, payload, and speed.

---

## 🚀 Project Overview

This project combines:

* ✅ Machine Learning (Linear Regression)
* ✅ Feature Encoding & Scaling
* ✅ Model Serialization
* ✅ Interactive Streamlit Web App
* ✅ LLM-style structured UI for prediction
* ✅ Clean glassmorphism dashboard design

Users can enter trip details and instantly get:

* CO₂ emission prediction
* Emission intensity per km
* Risk band (Low / Moderate / High)
* Session insights & summaries

---

## 🧠 ML Workflow

The ML pipeline includes:

1. Data collection & preprocessing
2. Exploratory Data Analysis
3. Feature Encoding (categorical variables)
4. Feature Scaling
5. Linear Regression model training
6. Model evaluation
7. Model export using Pickle
8. Streamlit deployment interface

Saved artifacts:

* `model.pkl` → trained Linear Regression model
* `scaler.pkl` → feature scaler
* `encoder.pkl` → categorical encoder

---

## 📂 Project Structure

```
CO2-Emission-Prediction/
│
├── app.py                # Streamlit application
├── model.ipynb           # Model training notebook
├── test.ipynb            # Testing notebook
├── first_project.csv     # Dataset
│
├── model.pkl             # Trained ML model
├── scaler.pkl            # Feature scaler
├── encoder.pkl           # Encoder
│
└── README.md
```

---

## ⚙️ Features

* 🌍 CO₂ emission prediction
* 🚗 Multi-vehicle support
* ⛽ Fuel-type based impact
* 👥 Passenger & payload adjustment
* 📊 Emission intensity metrics
* 🟢 Risk band classification
* 📈 Session history insights
* 🎨 Modern animated Streamlit UI
* 🤖 LLM-style structured prediction flow

---

## 🛠️ Tech Stack

* Python
* Scikit-learn
* Pandas
* NumPy
* Streamlit
* Pickle
* Linear Regression
* Feature Scaling & Encoding

---

## ▶️ How to Run the Project

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

---

### 2️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

If requirements file not added yet:

```bash
pip install streamlit scikit-learn pandas numpy
```

---

### 3️⃣ Run Streamlit App

```bash
streamlit run app.py
```

---

## 📊 Model Details

* Algorithm: **Linear Regression**
* Target: CO₂ Emission
* Preprocessing:

  * Label/One-Hot Encoding
  * Feature Scaling
* Evaluation Metrics:

  * R² Score
  * MAE / MSE (from notebook evaluation)

---

## 🧪 Example Inputs

| Feature    | Example |
| ---------- | ------- |
| Distance   | 12 km   |
| Fuel Type  | Petrol  |
| Vehicle    | Car     |
| Passengers | 2       |
| Payload    | 50 kg   |
| Speed      | 55 km/h |

Output → Predicted CO₂ emission + risk band.

---

## 🔮 Future Improvements

* Replace dummy predictor fully with trained model inference
* Add real emission datasets
* Add model comparison (RF, XGBoost, SVR)
* Add LLM explanation layer for predictions
* Deploy on Streamlit Cloud / HuggingFace Spaces
* Add API endpoint

---

## 📌 Use Cases

* Smart transport planning
* Carbon footprint estimation
* Sustainability analytics
* Green mobility research
* Educational ML projects

---

## 👨‍💻 Author

**Shibin T (Devu)**
Machine Learning & Data Analytics Enthusiast
AI + Sustainability Projects
