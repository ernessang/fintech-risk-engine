import json
from datetime import datetime

LOG_FILE = "transactions.log"


def log_transaction(tx, result):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "transaction": {
            "amount": tx.amount,
            "country": tx.country,
            "merchant": tx.merchant,
            "tokenized": tx.tokenized
        },
        "result": result
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
