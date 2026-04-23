import requests

# CONFIG
RULES_CONFIG = {
    "high_amount": {"threshold": 1000, "weight": 0.4},
    "foreign_tx": {"allowed_country": "MX", "weight": 0.2},
    "velocity": {"min_tx": 3, "weight": 0.3},
}

# -------- IP API --------
def get_ip_risk(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}")
        data = res.json()

        risk = 0
        reasons = []

        if data.get("proxy", False):
            risk += 0.4
            reasons.append("Proxy/VPN detected")

        if data.get("countryCode", "MX") != "MX":
            risk += 0.2
            reasons.append("Foreign IP")

        return risk, reasons
    except:
        return 0, []

# -------- BIN API --------
def get_bin_risk(bin_number):
    try:
        res = requests.get(f"https://lookup.binlist.net/{bin_number}")
        data = res.json()

        risk = 0
        reasons = []

        country = data.get("country", {}).get("alpha2")

        if country and country != "MX":
            risk += 0.3
            reasons.append("Foreign card")

        return risk, reasons
    except:
        return 0, []

# -------- MOTOR --------
def analyze_transaction(tx, history=[]):

    score = 0
    reasons = []

    amount = tx.amount
    merchant = tx.merchant.upper()
    country = tx.country

    if amount > RULES_CONFIG["high_amount"]["threshold"]:
        score += RULES_CONFIG["high_amount"]["weight"]
        reasons.append("High amount")

    if country != RULES_CONFIG["foreign_tx"]["allowed_country"]:
        score += RULES_CONFIG["foreign_tx"]["weight"]
        reasons.append("Foreign transaction")

    if len(history[-5:]) >= RULES_CONFIG["velocity"]["min_tx"]:
        score += RULES_CONFIG["velocity"]["weight"]
        reasons.append("High velocity")

    # IP API
    ip = getattr(tx, "ip", "8.8.8.8")
    ip_score, ip_reasons = get_ip_risk(ip)

    score += ip_score
    reasons.extend(ip_reasons)

    # BIN API
    fake_bin = "45717360"
    bin_score, bin_reasons = get_bin_risk(fake_bin)

    score += bin_score
    reasons.extend(bin_reasons)

    score = min(score, 1.0)

    if score >= 0.75:
        decision = "DECLINE"
        code = "05"
    elif score >= 0.45:
        decision = "REVIEW"
        code = "10"
    else:
        decision = "APPROVE"
        code = "00"

    return {
        "decision": decision,
        "risk_score": round(score, 2),
        "response_code": code,
        "reason": reasons
    }
