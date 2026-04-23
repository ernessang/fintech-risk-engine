import random


def analyze_transaction(tx):

    risk_score = 0.0
    reason = []

    # 🔹 Regla 1: monto alto
    if tx.amount > 3000:
        risk_score += 0.4
        reason.append("High amount")

    # 🔹 Regla 2: tokenización
    if not tx.tokenized:
        risk_score += 0.3
        reason.append("Non-tokenized transaction")
    else:
        risk_score -= 0.1
        reason.append("Tokenized (lower risk)")

    # 🔹 Regla 3: país
    if tx.country not in ["MX", "US", "CA"]:
        risk_score += 0.3
        reason.append("Foreign transaction")

    # 🔹 Regla 4: merchant risk
    high_risk_merchants = ["CASINO", "BET", "CRYPTO"]
    if tx.merchant.upper() in high_risk_merchants:
        risk_score += 0.4
        reason.append("High risk merchant")

    # 🔹 Evitar score negativo
    if risk_score < 0:
        risk_score = 0

    # 🔥 NUEVO: simulación de errores tipo issuer
    error_chance = random.random()

    if error_chance < 0.15:
        return {
            "error": "NO_RESPONSE_FROM_ISSUER",
            "message": "Issuer did not respond in time",
            "response_code": "91"
        }

    elif error_chance < 0.25:
        return {
            "error": "ISSUER_TIMEOUT",
            "message": "Authorization timeout",
            "response_code": "68"
        }

    elif error_chance < 0.30:
        return {
            "error": "SYSTEM_ERROR",
            "message": "Internal server error",
            "response_code": "96"
        }

    # 🔹 Decisión normal
    if risk_score < 0.3:
        decision = "APPROVE"
        code = "00"
    elif risk_score < 0.7:
        decision = "REVIEW"
        code = "10"
    else:
        decision = "DECLINE"
        code = "05"

    return {
        "decision": decision,
        "response_code": code,
        "risk_score": round(risk_score, 2),
        "reason": reason
    }
