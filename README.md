# Scoobie-App

Scoobie-App is a full-stack web application featuring a React frontend, a Python (Flask) backend, and a PostgreSQL database. The project demonstrates a complete DevOps lifecycle, including automated testing, security scanning, containerization, and continuous deployment to a Kubernetes cluster running on AWS.

## Core Technologies

- **Frontend**: React.js
- **Backend**: Python with Flask
- **Database**: PostgreSQL
- **Containerization**: Docker
- **Orchestration**: Kubernetes (Minikube)
- **Cloud Provider**: AWS (EC2)
- **CI/CD**: GitHub Actions (with a self-hosted runner)

---

## CI/CD Pipeline

The project is configured with a complete CI/CD pipeline using GitHub Actions, which automates the entire process from code commit to deployment. The pipeline is split into several workflows for clarity and separation of concerns.  
**A self-hosted GitHub Actions runner is configured on the AWS EC2 instance, giving the pipeline direct access to the Docker and Kubernetes environment.**

### 1. `ci.yml` (Continuous Integration)

This workflow runs on every push and pull request to the `main` branch to ensure code quality and security.

- **Linting**: `flake8` for Python and `ESLint` for React.
- **Unit Testing**: `pytest` for the backend and `Jest`/`React Testing Library` for the frontend.
- **SAST (Static Analysis)**: `bandit` scans the Python code for common security issues.
- **SCA (Software Component Analysis)**: `npm audit` and `pip-audit` scan dependencies for known vulnerabilities.

### 2. `build-and-push.yml` (Build Artifacts)

Triggered after the CI workflow succeeds on a push to `main`.

- Builds Docker images for the frontend (Nginx + React) and backend (Flask + Gunicorn).
- Pushes the versioned images to Docker Hub.

### 3. `deploy.yml` (Continuous Deployment)

Triggered after the build workflow succeeds.

- Applies all Kubernetes manifests from the `/kubernetes` directory.
- Performs a `rollout restart` of the deployments to force Kubernetes to pull the new images, ensuring zero-downtime updates.

### 4. `dast.yml` (Dynamic Security Scan)

A manually triggered workflow for on-demand security testing.

- Uses **OWASP ZAP** to run a baseline DAST scan against the live, running application.
- Uploads a detailed HTML report of any findings as a workflow artifact.

---

## Deployment Architecture

The application is designed to be deployed on a single AWS EC2 instance running a Minikube cluster.

- **GitHub Actions Runner**: A self-hosted runner is installed on the EC2 instance, giving the CI/CD pipeline direct access to the Docker and Kubernetes environment.
- **Kubernetes**: All components (frontend, backend, database) run as pods within a dedicated `scoobie-app` namespace.
  - The database uses a `StatefulSet` with a `PersistentVolume` mapped to the EC2 host's filesystem for data persistence.
  - The frontend is exposed to the internet via a `NodePort` service.

---

## Local Development

### Prerequisites

- Python 3.10+
- Node.js & npm
- Docker & Docker Compose
- A running PostgreSQL database.

### Setting Up the Environment

For local development, you need to provide the database credentials to the backend via environment variables. Create a file named `.env` in the `backend-api-python/` directory:

```env
# backend-api-python/.env
POSTGRES_USER="scoobie_user"
POSTGRES_PASSWORD="yourStrongPassword"
POSTGRES_DB="scoobie_db"
POSTGRES_HOST="localhost"
```

### Running the Backend

```bash
# Navigate to the backend directory
cd backend-api-python/

# Install dependencies
pip install -r requirements.txt

# Run the app (it will load variables from .env if python-dotenv is installed)
python app.py
```

### Running the Frontend

```bash
# Navigate to the frontend directory
cd frontend-app/

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will open at [http://localhost:3000](http://localhost:3000) and proxy API calls to the