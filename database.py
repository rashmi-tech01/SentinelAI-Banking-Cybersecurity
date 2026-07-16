import sqlite3


def create_table():

    conn = sqlite3.connect("sentinel.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount INTEGER,
        device TEXT,
        vpn TEXT,
        login_attempts INTEGER,
        risk_score INTEGER,
        result TEXT,
        status TEXT

    )
    """)

    conn.commit()
    conn.close()


def save_transaction(
    amount,
    device,
    vpn,
    login_attempts,
    risk_score,
    result,
    status
):

    conn = sqlite3.connect("sentinel.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transactions
    (
        amount,
        device,
        vpn,
        login_attempts,
        risk_score,
        result,
        status
    )

    VALUES (?,?,?,?,?,?,?)

    """,
    (
        amount,
        device,
        vpn,
        login_attempts,
        risk_score,
        result,
        status
    ))

    conn.commit()
    conn.close()


def get_dashboard_data():

    conn = sqlite3.connect("sentinel.db")
    cursor = conn.cursor()

    # Total Transactions
    cursor.execute("SELECT COUNT(*) FROM transactions")
    total_transactions = cursor.fetchone()[0]

    # Fraud Alerts
    cursor.execute(
        "SELECT COUNT(*) FROM transactions WHERE status='HIGH RISK'"
    )
    fraud_alerts = cursor.fetchone()[0]

    # Average Risk Score
    cursor.execute("SELECT AVG(risk_score) FROM transactions")
    avg_risk = cursor.fetchone()[0]

    if avg_risk is None:
        avg_risk = 0

    # Threat Level
    if avg_risk >= 60:
        threat = "HIGH"
    else:
        threat = "LOW"

    # Recent Transactions
    cursor.execute("""
        SELECT amount, device, risk_score, result
        FROM transactions
        ORDER BY id DESC
        LIMIT 5
    """)

    recent_transactions = cursor.fetchall()

    conn.close()

    return {
        "total_transactions": total_transactions,
        "fraud_alerts": fraud_alerts,
        "avg_risk": round(avg_risk),
        "threat": threat,
        "recent_transactions": recent_transactions
    }
def get_analytics_data():

    conn = sqlite3.connect("sentinel.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM transactions WHERE result='BLOCK TRANSACTION'")
    blocked = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions WHERE result='APPROVE TRANSACTION'")
    approved = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(risk_score) FROM transactions")
    avg = cursor.fetchone()[0]

    if avg is None:
        avg = 0

    conn.close()

    return blocked, approved, round(avg)
def get_all_transactions():

    conn = sqlite3.connect("sentinel.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            amount,
            device,
            vpn,
            login_attempts,
            risk_score,
            result,
            status
        FROM transactions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows