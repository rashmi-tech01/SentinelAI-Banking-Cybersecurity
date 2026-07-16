from flask import Flask, render_template, request
from database import create_table, save_transaction, get_dashboard_data
from predict import predict_risk
from report_generator import generate_report
from flask import send_file
from report_generator import generate_report
from database import create_table, save_transaction, get_dashboard_data, get_analytics_data
from database import (
    create_table,
    save_transaction,
    get_dashboard_data,
    get_analytics_data,
    get_all_transactions
)

# Create Flask Application
app = Flask(__name__)

# Create Database Table
create_table()


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Login Page
@app.route("/login")
def login():
    return render_template("login.html")


# About Page
@app.route("/about")
def about():
    return render_template("about.html")


# Dashboard Page
@app.route("/dashboard")
def dashboard():

    data = get_dashboard_data()

    return render_template(
        "dashboard.html",
        data=data
    )


# Transaction Page
@app.route("/transaction")
def transaction():
    return render_template("transaction.html")


# ML Prediction Route
@app.route("/predict", methods=["POST"])
def predict():

    amount = int(request.form["amount"])
    device = int(request.form["device"])
    vpn = int(request.form["vpn"])
    login_attempts = int(request.form["login_attempts"])

    # Call ML Prediction Function
    result = predict_risk(
        amount,
        device,
        vpn,
        login_attempts
    )

    # Save Transaction Data
    save_transaction(
        amount,
        "New Device" if device == 1 else "Known Device",
        "VPN" if vpn == 1 else "No VPN",
        login_attempts,
        result["risk_score"],
        result["result"],
        result["status"]
    )
    generate_report(
    amount,
    result["risk_score"],
    result["result"],
    result["status"],
    result["reasons"]
) 
    # Generate PDF Report
    pdf_path = generate_report(
    amount,
    result["risk_score"],
    result["result"],
    result["status"],
    result["reasons"]
)

    # Show Result Page
    return render_template(
    "result.html",
    risk_score=result["risk_score"],
    result=result["result"],
    status=result["status"],
    reasons=result["reasons"]
)
@app.route("/analytics")
def analytics():

    blocked, approved, avg_risk = get_analytics_data()

    return render_template(
        "analytics.html",
        blocked=blocked,
        approved=approved,
        avg_risk=avg_risk
    )

@app.route("/history")
def history():

    transactions = get_all_transactions()

    return render_template(
        "history.html",
        transactions=transactions
    )

@app.route("/download-report")
def download_report():

    return send_file(
        "reports/Fraud_Report.pdf",
        as_attachment=True
    )

# Run Application
if __name__ == "__main__":
    app.run(debug=True)