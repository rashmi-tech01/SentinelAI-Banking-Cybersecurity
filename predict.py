import joblib
import pandas as pd

# Load trained model
model = joblib.load("model/fraud_model.pkl")


def predict_risk(amount, device, vpn, login_attempts):

    data = pd.DataFrame({
        "amount": [amount],
        "device": [device],
        "vpn": [vpn],
        "login_attempts": [login_attempts]
    })

    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0][1]

    risk_score = round(probability * 100)

    reasons = []

    if amount > 50000:
        reasons.append("High Transaction Amount")

    if device == 1:
        reasons.append("New Device Detected")

    if vpn == 1:
        reasons.append("VPN Usage Detected")

    if login_attempts > 3:
        reasons.append("Multiple Failed Login Attempts")

    if prediction == 1:
        result = "BLOCK TRANSACTION"
        status = "HIGH RISK"
    else:
        result = "APPROVE TRANSACTION"
        status = "LOW RISK"

        if not reasons:
            reasons = [
                "Known Device",
                "No VPN Detected",
                "Normal Transaction Amount",
                "Normal Login Activity"
            ]

    return {
        "risk_score": risk_score,
        "result": result,
        "status": status,
        "reasons": reasons
    }