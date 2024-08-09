# Text Summarization and Translation Application

## Overview

This project provides a text summarization application with the capability to translate summaries into various languages. The application is built using FastAPI and packaged in a Docker container for easy deployment.

## Features

- Summarizes text based on user-defined parameters.
- Translates summaries into multiple languages.
- Provides API documentation through Swagger UI.
- Easily deployable using Docker.

## Getting Started

### Prerequisites

- Docker (installed on your machine)
- Basic understanding of REST APIs

## Installation

### 1. Clone the Repository

   ```bash
   git clone https://github.com/ninja03jod/Text_Summarization_With_Language_Trans
   cd Text_Summarization_With_Language_Trans
   ```

### 2. Build the Docker Image
```bash
docker build -t summarization-translation .
```

### 3. Run the Docker Container
```bash
docker run -d -p 8000:8000 summarization-translation
```

### 4. Access the FastAPI Application
`API Documentation`: API documentation is accessible via Swagger UI at `/docs` endpoint. You can view it at `http://localhost:8000/docs` when running the application.

#### Running Only Fastapi
```bash
uvicorn app/main:app --reload
```

### 5. Pulling a Pre-built Docker Image
```bash
docker pull 840804/summarization-translation
```
```
docker run -d -p 8000:8000 840804/summarization-translation
```

### Contact
For questions or issues, please contact saadbagwan447@gmail.com


### Explanation:
- **Clone the Repository**: Instructions to get the code from your version control system.
- **Build the Docker Image**: How to build the Docker image from the `Dockerfile`.
- **Run the Docker Container**: Instructions to start the container and map the ports.
- **Pulling a Pre-built Docker Image**: How to pull and run an existing Docker image if it's hosted on Docker Hub.
- **API Endpoints**: Example endpoints for interacting with the FastAPI application.
