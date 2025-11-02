import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# Import configuration from our config file
import config

def run_training():
    """
    Load data, train the model pipeline, and save it.
    """
    print("--- Starting training process ---")

    # 1. Load Data
    print(f"Loading data from {config.RAW_DATA_PATH}...")
    df = pd.read_csv(config.RAW_DATA_PATH)

    # 2. Data Cleaning & Preprocessing
    # A common issue in this dataset: 'TotalCharges' can be a space ' '
    # Convert 'TotalCharges' to numeric, coercing errors to NaN
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

    # Drop customerID as it's not a feature
    df = df.drop('customerID', axis=1)

    # Convert target variable to binary
    df[config.TARGET_COLUMN] = df[config.TARGET_COLUMN].apply(lambda x: 1 if x == 'Yes' else 0)

    # 3. Split Data
    print("Splitting data into training and testing sets...")
    X = df.drop(config.TARGET_COLUMN, axis=1)
    y = df[config.TARGET_COLUMN]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Define Preprocessing Pipelines for different feature types
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')), # Handle missing TotalCharges
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore')) # Ignore categories not seen in training
    ])

    # 5. Create the master preprocessor with ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, config.NUMERICAL_FEATURES),
            ('cat', categorical_transformer, config.CATEGORICAL_FEATURES)
        ],
        remainder='passthrough' # Keep other columns if any
    )

    # 6. Define the final model pipeline
    print("Defining the model pipeline...")
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(random_state=42, max_iter=1000))
    ])

    # 7. Train the model
    print("Training the model...")
    model_pipeline.fit(X_train, y_train)

    # 8. Evaluate the model
    y_pred = model_pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy on Test Set: {accuracy:.4f}")

    # 9. Save the pipeline
    print(f"Saving model pipeline to {config.MODEL_PATH}...")
    joblib.dump(model_pipeline, config.MODEL_PATH)
    print("--- Training process finished successfully! ---")

if __name__ == "__main__":
    run_training()