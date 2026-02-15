🌿 CO₂ Emission Prediction using Machine Learning

A machine learning web application that predicts vehicle CO₂ emissions based on engine and fuel characteristics.
This project demonstrates an end-to-end ML pipeline including preprocessing, model training, and deployment using Streamlit.

🚀 Project Overview

This project predicts CO₂ emissions of vehicles using a regression model trained on vehicle specifications such as engine size, cylinders, fuel type, and fuel consumption.

The system:

Performs data preprocessing

Encodes categorical features

Scales numerical features

Trains regression model

Deploys using Streamlit

Users can input vehicle details and get real-time CO₂ emission predictions.

🧠 Machine Learning Workflow

Data preprocessing and cleaning

Handling categorical features using OneHotEncoder

Feature scaling using RobustScaler

Model training using regression algorithm

Model serialization using Joblib

Deployment using Streamlit

🛠️ Technologies Used

Python

Pandas & NumPy

Scikit-learn

Matplotlib

Streamlit

Joblib

📊 Features of Application

Real-time CO₂ prediction

Interactive Streamlit UI

Model insights and visualizations

Feature impact graphs

Clean and responsive dashboard

Fallback prediction mode

📁 Project Structure
CO2-Emission-Prediction/
│
├── app.py               # Streamlit application
├── model.ipynb          # Model training notebook
├── model.pkl            # Trained ML model
├── scaler.pkl           # Scaler object
├── encoder.pkl          # OneHotEncoder
├── features.pkl         # Feature column order
├── first_project.csv    # Dataset
└── README.md

▶️ How to Run the Project
1. Clone repository
git clone https://github.com/yourusername/co2-emission-prediction.git
cd co2-emission-prediction

2. Install dependencies
pip install streamlit pandas numpy scikit-learn matplotlib joblib

3. Run application
streamlit run app.py


App will open in browser:

http://localhost:8501

📈 Model Insights

The model shows:

Larger engine size → higher CO₂ emission

Higher fuel consumption → more emissions

More cylinders → more emissions

Higher MPG → lower emissions

Electric vehicles → lowest emissions

🎯 Future Improvements

Add model accuracy metrics

Add feature importance visualization

Deploy on cloud (Streamlit cloud)

Add multiple ML models comparison

Add download prediction report

👨‍💻 Author

Shibin T
Machine Learning Enthusiast | AI Developer
