# CryptoTracker - Portfolio Service

A Flask-based microservice for the CryptoTracker application that manages user cryptocurrency portfolios, including holdings management and net worth calculation.

## Overview
The Portfolio Service is responsible for:

- Managing user cryptocurrency portfolios
- Adding and removing coin holdings
- Calculating total net holdings for users
- Authenticating users via the User Service
- Providing portfolio endpoints for other CryptoTracker services

## Technology Stack
- **Language:** Python 3.14
- **Framework:** Flask 3.1
- **ORM:** Flask-SQLAlchemy 3.1.1
- **WSGI Server:** Gunicorn 21.2.0
- **Database:** PostgreSQL 18

## Local Development

### Installation
```bash
# Clone the repository
git clone https://github.com/Crypto-Tracker-App/portfolio-service.git
cd portfolio-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration
Create a `.env` file in the project root:

```
POSTGRES_USER=dev_user
POSTGRES_PASSWORD=dev_password
POSTGRES_DB=dev_db
DB_PORT=5432
DB_HOST=localhost
USER_SERVICE_URL=http://localhost:13000/api/user/me
```

### Running with Docker Compose
```bash
# Start PostgreSQL and the application
docker-compose up

# The application will be available at http://localhost:5000
```

### Running Locally
```bash
# Run database migrations
alembic upgrade head

# Start the Flask development server
python wsgi.py
```

## API Endpoints

### Get Total Net Holding
**GET** `/api/portfolio/total`

Returns the total net holding for the authenticated user.

**Response:**
```json
{
	"status": "success",
	"user_id": "user123",
	"total_net_holding": 123.45
}
```

### Add Holding
**POST** `/api/portfolio/add`

Add a coin holding for the authenticated user.

**Request Body:**
```json
{
	"coin_id": "bitcoin",
	"amount": 1.5
}
```

**Response:**
```json
{
	"status": "success",
	"holding": {
		"coin_id": "bitcoin",
		"amount": 1.5
	}
}
```

### Remove Holding
**POST** `/api/portfolio/remove`

Remove a coin holding for the authenticated user.

**Request Body:**
```json
{
	"coin_id": "bitcoin"
}
```

**Response:**
```json
{
	"status": "success",
	"message": "holding removed"
}
```

## Deployment

### Azure Cloud Architecture
The Portfolio Service is designed to run on Azure using:
- Azure Kubernetes Service (AKS)
- Azure Container Registry (ACR)
- Azure Monitor

### Docker
The application is containerized using Docker with a Python 3.14 base image.

```bash
# Build Docker image
docker build -t portfolio-service:latest .

# Run container locally
docker run -p 5000:5000 \
	-e POSTGRES_USER=dev_user \
	-e POSTGRES_PASSWORD=dev_password \
	-e POSTGRES_DB=dev_db \
	-e DB_HOST=postgres \
	-e DB_PORT=5432 \
	-e USER_SERVICE_URL=http://user-service:13000/api/user/me \
	portfolio-service:latest
```

The application runs on port 5000 using Gunicorn.

### Azure Container Registry
```bash
# Login to Azure
az login

# Login to Azure Container Registry
az acr login --name <your-acr-name>

# Tag image for ACR
docker tag portfolio-service:latest cryptotracker.azurecr.io/portfolio-service:latest

# Push image to ACR
docker push cryptotracker.azurecr.io/portfolio-service:latest
```

### Azure Kubernetes Service Deployment
```bash
# Connect to AKS cluster
az aks get-credentials --resource-group <resource-group> --name <aks-cluster-name>

# Create Kubernetes namespace (optional)
kubectl create namespace crypto-tracker

# Deploy to AKS
kubectl apply -f k8s/ -n crypto-tracker

# Verify deployment
kubectl get pods -n crypto-tracker
kubectl get services -n crypto-tracker

# Check logs
kubectl logs -f deployment/portfolio-service -n crypto-tracker
```

## Project Structure
```
portfolio-service/
├── wsgi.py                     # Flask application entry point
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container image definition
├── app/
│   ├── __init__.py             # Flask app factory
│   ├── config.py               # Application configuration
│   ├── api/                    # API endpoints
│   │   └── portfolio.py        # Portfolio endpoints
│   ├── models/                 # Database models
│   │   └── portfolio.py        # Portfolio and Holding models
│   ├── services/               # Business logic
│   │   └── portfolio_service.py# Portfolio service logic
│   └── utils/                  # Utilities and helpers
│       ├── json.py             # JSON serialization utilities
│       └── logger.py           # Logging utilities
├── k8s/                        # Kubernetes manifests
```

## Environment Variables
| Variable           | Description                        | Required | Default      |
|--------------------|------------------------------------|----------|--------------|
| POSTGRES_USER      | PostgreSQL username                | Yes      | postgres     |
| POSTGRES_PASSWORD  | PostgreSQL password                | Yes      | postgres     |
| POSTGRES_DB        | PostgreSQL database name           | Yes      | portfolio_db |
| DB_PORT            | PostgreSQL port                    | No       | 5432         |
| DB_HOST            | PostgreSQL host                    | No       | localhost    |
| USER_SERVICE_URL   | User service URL for auth          | Yes      | -            |
| SERVICE_NAME       | Service identifier for logging     | No       | portfolio-service |
| SERVICE_VERSION    | Service version for logging        | No       | 1.0.0        |
| ENVIRONMENT        | Deployment environment             | No       | development  |
| EXTERNAL_LOG_LEVEL | Log level for external libraries   | No       | WARNING      |
| LOG_REQUEST_COMPLETION | Request logging mode           | No       | errors       |

### Azure-Specific Configuration
Sensitive data should be managed via Azure Key Vault or Kubernetes Secrets. Non-sensitive configuration can be managed via Kubernetes ConfigMaps..

**Example Kubernetes Secret:**
```yaml
apiVersion: v1
kind: Secret
metadata:
	name: portfolio-service-secrets
type: Opaque
stringData:
	POSTGRES_PASSWORD: <your-db-password>
	USER_SERVICE_URL: <user-service-url>
```

---

For more information, see the [k8s/](k8s/) directory for deployment manifests.
# Portfolio-service