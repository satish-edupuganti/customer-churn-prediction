from pydantic import BaseModel, Field
from typing import Optional

# This Pydantic model defines the structure of the input data for prediction
# It ensures that incoming requests have the correct fields and data types.
# Optional[...] means the field is not required.
# Field(..., example=...) provides example values for the auto-generated documentation.

class ChurnInput(BaseModel):
    gender: str = Field(..., example="Male")
    SeniorCitizen: int = Field(..., example=0, description="0 for No, 1 for Yes")
    Partner: str = Field(..., example="Yes")
    Dependents: str = Field(..., example="No")
    tenure: int = Field(..., example=24)
    PhoneService: str = Field(..., example="Yes")
    MultipleLines: str = Field(..., example="No")
    InternetService: str = Field(..., example="DSL")
    OnlineSecurity: str = Field(..., example="Yes")
    OnlineBackup: str = Field(..., example="No")
    DeviceProtection: str = Field(..., example="Yes")
    TechSupport: str = Field(..., example="No")
    StreamingTV: str = Field(..., example="No")
    StreamingMovies: str = Field(..., example="Yes")
    Contract: str = Field(..., example="Month-to-month")
    PaperlessBilling: str = Field(..., example="Yes")
    PaymentMethod: str = Field(..., example="Electronic check")
    MonthlyCharges: float = Field(..., example=55.20)
    TotalCharges: Optional[float] = Field(None, example=1397.47)

# This defines the structure of the prediction response
class PredictionOutput(BaseModel):
    prediction: int = Field(..., example=0, description="0 for 'No Churn', 1 for 'Churn'")