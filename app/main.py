from fastapi import FastAPI
from app.models import Transaction
from app.logic import analyze_transaction
from app.logger import log_transaction
from app.queries import filter_logs, compute_metrics

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Fintech Brain API is running"}


@app.post("/analyze-transaction")
def analyze(tx: Transaction):
    result = analyze_transaction(tx)
    log_transaction(tx, result)
    return result


@app.get("/logs")
def get_logs(error: str = None, merchant: str = None, decision: str = None):
    return filter_logs(error, merchant, decision)


@app.get("/metrics")
def get_metrics():
    return compute_metrics()
