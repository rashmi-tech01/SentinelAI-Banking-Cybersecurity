from predict import predict_risk

risk = predict_risk(
    amount=95000,
    failed_login=5,
    new_device=1,
    vpn=1
)

print("Prediction:", risk)