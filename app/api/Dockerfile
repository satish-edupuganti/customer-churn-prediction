# --- Stage 1: The Builder ---
# This stage installs dependencies and compiles our code.
FROM python:3.9-slim AS builder

# Set the working directory
WORKDIR /app

# Install build dependencies if any (we don't have many, but good practice)
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Copy only the requirements file and install packages
# This creates a layer with just the dependencies, which is efficient
COPY app/api/requirements.txt .
# RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt
RUN pip wheel --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# --- Stage 2: The Final Image ---
# This stage creates the lean, final image for production.
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the installed packages from the builder stage
COPY --from=builder /app/wheels /wheels
# RUN pip install --no-cache /wheels/*
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org --no-cache /wheels/*

# Copy only the necessary application code and artifacts
# This is much more specific and efficient than copying the whole 'app' folder
COPY ./src ./src
COPY ./app/api ./app/api
COPY ./artifacts ./artifacts

# Expose the port and set the command to run the application
EXPOSE 8000
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]