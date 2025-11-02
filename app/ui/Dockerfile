# --- Stage 1: The Builder ---
FROM python:3.9-slim AS builder

WORKDIR /app

COPY app/ui/requirements.txt .
# RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt
RUN pip wheel --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# --- Stage 2: The Final Image ---
FROM python:3.9-slim

WORKDIR /app

# Copy the installed packages from the builder stage
COPY --from=builder /app/wheels /wheels
# RUN pip install --no-cache /wheels/*
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org --no-cache /wheels/*

# Copy only the UI application code
COPY ./app/ui ./app/ui

# Expose the port and set the command to run the Streamlit app
EXPOSE 8501
CMD ["streamlit", "run", "app/ui/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]