# Fintech Risk Engine

A FastAPI-based service that analyzes financial transactions, computes risk scores, and returns actionable insights for fraud detection and spending behavior.

## ✨ Features
- Risk scoring for transactions
- Rule-based fraud signals
- Clear decisions: APPROVE / REVIEW / DECLINE
- Simple REST API

## 🔌 Endpoints
- GET / → health check
- POST /analyze-transaction → analyze a transaction
- GET /logs → filter logs (optional)
- GET /metrics → basic metrics

## 🧪 Example

Request:
{
  "amount": 200,
  "country": "MX",
  "merchant": "CASINO",
  "tokenized": true
}

Response:
{
  "decision": "REVIEW",
  "risk_score": 0.3,
  "reasons": [
    "Tokenized (lower risk)",
    "High-risk merchant"
  ]
}

## ⚙️ Run locally

pip install -r requirements.txt
uvicorn app.main:app --reload

Open:
http://127.0.0.1:8000/docs
