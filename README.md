customer-churn-prediction/
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # For GitHub Actions CI/CD pipeline
├── app/
│   ├── api/
│   │   ├── Dockerfile          # Instructions to containerize the FastAPI app
│   │   └── main.py             # The FastAPI application code
│   └── ui/
│       └── app.py              # The Streamlit UI application code
├── artifacts/
│   └── .gitkeep                # To store trained models, scalers, encoders
├── data/
│   ├── raw/
│   │   └── .gitkeep            # For the original, untouched dataset
│   └── processed/
│       └── .gitkeep            # For cleaned and preprocessed data
├── notebooks/
│   └── 1-exploratory-data-analysis.ipynb # Jupyter notebook for EDA
├── src/
│   └── churn_predictor/
│       ├── __init__.py         # Makes 'churn_predictor' a Python package
│       ├── config.py           # For storing constants and configuration
│       ├── pipeline.py         # To orchestrate the full ML pipeline
│       ├── preprocess.py       # Data cleaning and feature engineering functions
│       └── train.py            # Model training and evaluation code
├── tests/                      # For our unit and integration tests
│   ├── __init__.py
│   └── test_pipeline.py
├── .gitignore                  # To specify which files Git should ignore
├── README.md                   # Project documentation
├── requirements.txt            # List of Python libraries needed for the project
└── venv/                       # The virtual environment folder (if you created it)


Of course. This is an excellent idea. Having a complete log of all the terminal commands is like having a recipe book for your entire project. It's incredibly valuable for reproducing your work or starting a new project.

Here is a sequential, commented log of all the key commands we executed from start to finish.

---

### **Project Command Log: End-to-End Churn Prediction App**

#### **Phase 1: Local Project & Environment Setup**
*(Run on your local machine)*

1.  **Create Project Structure**
    *   **Command:** `mkdir customer-churn-prediction && cd customer-churn-prediction`
    *   **Purpose:** To create the main project folder and navigate into it.

2.  **Create Virtual Environment**
    *   **Command:** `python3 -m venv venv`
    *   **Purpose:** To create an isolated Python environment (`venv`) for our project, so its libraries don't conflict with other projects.

3.  **Activate Virtual Environment**
    *   **Command (Mac/Linux):** `source venv/bin/activate`
    *   **Command (Windows):** `venv\Scripts\activate`
    *   **Purpose:** To "enter" the isolated environment. Your terminal prompt will change to show `(venv)`.

4.  **Install Python Libraries**
    *   **Command:** `pip install -r requirements.txt`
    *   **Purpose:** To install all the Python packages listed in the `requirements.txt` file (like Pandas, Scikit-learn, FastAPI, etc.).

5.  **Initialize Git Repository**
    *   **Command:** `git init && git add . && git commit -m "Initial commit" && git remote add origin <URL> && git push -u origin main`
    *   **Purpose:** To initialize a Git repository, save your initial code, and push it to GitHub for the first time.

#### **Phase 2: Model Training**
*(Run on your local machine)*

1.  **Run the Training Script**
    *   **Command:** `python -m src.churn_predictor.train`
    *   **Purpose:** To execute our training script as a Python module. The `-m` flag is crucial because it allows our script to correctly import other files from our `src` package (like `config.py`), solving the `ModuleNotFoundError`.

#### **Phase 3: Running the Application Locally (without Docker)**
*(Run on your local machine, each in a separate terminal)*

1.  **Start the FastAPI Backend Server**
    *   **Command:** `uvicorn app.api.main:app --reload`
    *   **Purpose:** To start the Uvicorn web server, which runs our FastAPI application. The `--reload` flag automatically restarts the server whenever we save a code change.

2.  **Start the Streamlit Frontend UI**
    *   **Command:** `streamlit run app/ui/app.py`
    *   **Purpose:** To start the Streamlit server, which runs our user interface and makes it available in a web browser.

#### **Phase 4: Containerizing with Docker**
*(Run on your local machine)*

1.  **Build a Docker Image**
    *   **Command:** `docker build -t churn-prediction-api -f app/api/Dockerfile .`
    *   **Purpose:** To build a Docker image from a `Dockerfile`. `-t` tags (names) the image. `-f` specifies the path to the Dockerfile. The final `.` defines the build context (the entire project folder).

2.  **Clean Docker System (Critical for Debugging)**
    *   **Command:** `docker system prune -a -f`
    *   **Purpose:** To completely clean the Docker system by removing all stopped containers, unused images, and the entire build cache. This was essential for solving our image size issues.

3.  **Inspect an Image's Layers**
    *   **Command:** `docker history churn-prediction-api`
    *   **Purpose:** To see the size of each layer in an image. This helped us identify which `COPY` or `RUN` command was causing our image to be too large.

4.  **Get a Shell Inside a Container (for Debugging)**
    *   **Command:** `docker exec -it <container_name_or_id> /bin/sh`
    *   **Purpose:** To open an interactive shell inside a *running* container, allowing us to look around its filesystem and debug issues.

5.  **Find Large Files Inside a Container**
    *   **Command:** `du -sh /usr/local/lib/python3.9/site-packages/* | sort -rh | head -n 15`
    *   **Purpose:** (Run *inside* a container shell). To list the 15 largest directories in the `site-packages` folder, helping us identify which Python libraries were taking up the most space.

#### **Phase 5: AWS Setup & Pushing Images to ECR**
*(Run on your local machine)*

1.  **Configure AWS CLI Credentials**
    *   **Command:** `aws configure`
    *   **Purpose:** To securely save your IAM user's `Access Key ID` and `Secret Access Key`, allowing your terminal to communicate with your AWS account.

2.  **Verify AWS CLI Identity**
    *   **Command:** `aws sts get-caller-identity`
    *   **Purpose:** To confirm that your AWS CLI is configured correctly and see which user it's authenticated as.

3.  **Log Docker into Amazon ECR**
    *   **Command:** `aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account_id>.dkr.ecr.<region>.amazonaws.com`
    *   **Purpose:** To authenticate your local Docker client with your private Amazon ECR. This is required before you can push images.

4.  **Tag an Image for ECR**
    *   **Command:** `docker tag <local_image_name>:latest <ecr_repository_uri>:latest`
    *   **Purpose:** To give your local image a second name that matches the ECR repository's URI, telling Docker where to upload it.

5.  **Push an Image to ECR**
    *   **Command:** `docker push <ecr_repository_uri>:latest`
    *   **Purpose:** To upload your tagged Docker image from your local machine to your private repository in Amazon ECR.

#### **Phase 6: Manual Deployment on the EC2 Server**
*(Run inside the EC2 SSH session)*

1.  **Connect to the EC2 Instance**
    *   **Command:** `ssh -i /path/to/your/key.pem ubuntu@<public_ip_address>`
    *   **Purpose:** To securely connect to the command line of your Ubuntu server running on AWS.

2.  **Update the Server**
    *   **Command:** `sudo apt update && sudo apt upgrade -y`
    *   **Purpose:** To update the server's list of available software and install any security updates.

3.  **Install Docker and Add User to Group**
    *   **Command:** `sudo usermod -aG docker ubuntu`
    *   **Purpose:** To add your user (`ubuntu`) to the `docker` group, allowing you to run `docker` commands without `sudo`. (Requires logging out and back in to take effect).

4.  **Create/Edit a File**
    *   **Command:** `nano docker-compose.yml`
    *   **Purpose:** To use the `nano` text editor to create or edit a file, in this case, our application's deployment blueprint.

5.  **Run the Application with Docker Compose**
    *   **Command:** `docker-compose up -d`
    *   **Purpose:** To read the `docker-compose.yml` file and start all defined services (our API and UI) in detached (`-d`) mode, running them in the background.

6.  **Update the Deployed Application**
    *   **Command:** `docker-compose pull && docker-compose up -d`
    *   **Purpose:** To pull the newest versions of the images from ECR and then restart the services with the updated images.

7.  **Check Running Containers**
    *   **Command:** `docker ps`
    *   **Purpose:** To list all currently running Docker containers.

8.  **Check Container Logs**
    *   **Command:** `docker logs <container_name>`
    *   **Purpose:** To view the live or past output (logs) from a specific container. This was essential for debugging the API startup errors.

9.  **Check Server Disk Space**
    *   **Command:** `df -h`
    *   **Purpose:** To see the disk usage. This helped us diagnose the `no space left on device` error.

#### **Phase 7: Triggering the CI/CD Pipeline**
*(Run on your local machine)*

1.  **The Final Command**
    *   **Command:** `git push`
    *   **Purpose:** After configuring the `.github/workflows/ci-cd.yml` file, this is the only command you need to run to trigger the entire automated build and deployment process.

---

Save this log. It is the complete story of your project's creation. You can now confidently start a new chat with the summary, knowing you have all the critical code and commands backed up.