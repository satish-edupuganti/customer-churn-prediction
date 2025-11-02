import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Customer Churn Prediction updated",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- App Title ---
st.title("Customer Churn Prediction 🤖")
st.write("Enter customer details to predict whether they will churn or not.")
st.write("This UI sends a request to a FastAPI backend for prediction.")

# --- API Endpoint ---
# Make sure your FastAPI server is running!
# API_ENDPOINT = "http://127.0.0.1:8000/predict"
# API_ENDPOINT = "http://churn-api:8000/predict"

import os

# Get the API endpoint from an environment variable, with a default for local running
API_ENDPOINT = os.getenv("API_ENDPOINT", "http://127.0.0.1:8000/predict")


# --- Input Form ---
st.header("Customer Details")

# Create two columns for a cleaner layout
col1, col2 = st.columns(2)

with col1:
    tenure = st.number_input("Tenure (months)", min_value=0, max_value=100, value=24)
    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
    payment_method = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
    monthly_charges = st.slider("Monthly Charges ($)", 18.0, 120.0, 55.20, 0.1)
    total_charges = st.number_input("Total Charges ($)", min_value=0.0, value=1397.47, format="%.2f")

with col2:
    gender = st.selectbox("Gender", ["Male", "Female"])
    senior_citizen = st.selectbox("Senior Citizen", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])
    phone_service = st.selectbox("Phone Service", ["Yes", "No"])
    multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
    internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])


# Group the rest of the inputs
st.subheader("Services Information")
col3, col4, col5 = st.columns(3)
with col3:
    online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
    online_backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
    device_protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
with col4:
    tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])
    streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
    streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])


# --- Prediction Logic ---
if st.button("Predict Churn", type="primary"):
    # Create the input dictionary
    input_data = {
        "gender": gender,
        "SeniorCitizen": senior_citizen,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges if total_charges > 0 else None # Handle zero total charges
    }

    st.write("Sending the following data to the API:")
    st.json(input_data)

    try:
        # Send the POST request to the FastAPI endpoint
        response = requests.post(API_ENDPOINT, json=input_data, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        # Display the prediction result
        result = response.json()
        prediction = result['prediction']
        
        st.subheader("Prediction Result")
        if prediction == 1:
            st.error("Prediction: **Customer will CHURN** 😞")
        else:
            st.success("Prediction: **Customer will NOT CHURN** 😊")

    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the API. Please make sure the FastAPI server is running. Error: {e}")
