from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
import sys
from pathlib import Path

# Add the project root to the Python path
# This is a common pattern for making your source code importable
# when running an app from a subdirectory.
# project_root = Path(__file__).resolve().parent.parent.parent
# sys.path.append(str(project_root))
from app.api.schemas import ChurnInput, PredictionOutput
from src.churn_predictor import config # Now this import works

# Create a FastAPI app instance
app = FastAPI(title="Customer Churn Prediction API", version="1.0")

# --- Globals ---
# We load the model once when the application starts.
# This is efficient as it avoids reloading the model for every request.
try:
    model = joblib.load(config.MODEL_PATH)
    print(f"Model loaded successfully from {config.MODEL_PATH}")
except FileNotFoundError:
    print(f"Error: Model file not found at {config.MODEL_PATH}")
    model = None
except Exception as e:
    print(f"An error occurred while loading the model: {e}")
    model = None

# --- API Endpoints ---
@app.get("/")
def read_root():
    """A simple health check endpoint."""
    return {"status": "API is up and running!"}


@app.post("/predict", response_model=PredictionOutput)
def predict_churn(input_data: ChurnInput):
    """
    Predict customer churn based on input features.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not available. Please check server logs.")

    try:
        # Convert the Pydantic model to a dictionary
        input_dict = input_data.model_dump()

        # Convert the dictionary to a pandas DataFrame
        # The model pipeline expects a DataFrame as input
        input_df = pd.DataFrame([input_dict])

        # Ensure the column order matches the training data (optional but good practice)
        # Note: Our pipeline's ColumnTransformer handles this, but it's good to be explicit.
        # ordered_cols = config.NUMERICAL_FEATURES + config.CATEGORICAL_FEATURES
        # input_df = input_df[ordered_cols]

        # Make a prediction
        prediction = model.predict(input_df)

        # The model returns a numpy array, we extract the first element
        result = int(prediction[0])

        return {"prediction": result}

    except Exception as e:
        # This will catch any errors during prediction and return a helpful message
        raise HTTPException(status_code=500, detail=f"An error occurred during prediction: {str(e)}")