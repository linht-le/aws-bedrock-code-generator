# Code Generation Chatbot

AI-powered chatbot for generating production-ready code using AWS Bedrock foundation models.

## Features

- AWS Bedrock integration with Amazon Nova Pro
- Complete code generation with documentation
- Interactive Streamlit UI
- Multi-language support
- FastAPI backend

## Tech Stack

- Backend: FastAPI, AWS Bedrock (boto3)
- Frontend: Streamlit
- Models: Amazon Nova Pro
- Python 3.12+

## Prerequisites

- Python 3.12+
- AWS Account with Bedrock access
- AWS credentials
- Valid payment method (Bedrock requires billing)

## Installation

```bash
make install
```

## Configuration

Create `.env` file:

```env
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
MODEL_ID=us.amazon.nova-pro-v1:0
```

Available models:

- `us.amazon.nova-pro-v1:0` - Amazon Nova Pro
- `us.amazon.nova-lite-v1:0` - Amazon Nova Lite

## Usage

Start backend:

```bash
make run-be
```

Start frontend:

```bash
make run-fe
```

Backend API: <http://localhost:8000>
Frontend UI: <http://localhost:8501>

## Project Structure

```sh
app/
├── api.py          # FastAPI routes
├── config.py       # Configuration
├── models.py       # Pydantic models
├── services.py     # AWS Bedrock service
└── main.py         # App initialization
streamlit_app.py    # Streamlit UI
pyproject.toml      # Dependencies
Makefile           # Commands
.env               # Config (create this)
```

## AWS Bedrock Setup

1. Add payment method in AWS Console
2. First API call enables the model automatically
3. Set budget alert (optional)

Cost: ~$0.01-$0.10 per session
