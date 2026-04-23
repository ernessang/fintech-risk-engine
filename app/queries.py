import json

LOG_FILE = "transactions.log"


def read_logs():
    logs = []
    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                logs.append(json.loads(line))
    except FileNotFoundError:
        return []
    return logs


def filter_logs(error=None, merchant=None, decision=None):
    logs = read_logs()
    results = []

    for log in logs:
        res = log.get("result", {})

        if error and res.get("error") != error:
            continue

        if merchant and log["transaction"]["merchant"] != merchant:
            continue

        if decision and res.get("decision") != decision:
            continue

        results.append(log)

    return results


def compute_metrics():
    logs = read_logs()

    total = len(logs)
    declines = 0
    errors = 0
    approves = 0

    for log in logs:
        res = log.get("result", {})

        if "error" in res:
            errors += 1
        elif res.get("decision") == "DECLINE":
            declines += 1
        elif res.get("decision") == "APPROVE":
            approves += 1

    return {
        "total": total,
        "declines": declines,
        "errors": errors,
        "approves": approves,
        "approval_rate": round(approves / total, 2) if total > 0 else 0
    }
