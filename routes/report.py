from flask import Blueprint, render_template, session, redirect
import mysql.connector

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQL@123",
    database="finance_db",
    port=3307
)

cursor = db.cursor()

report_bp = Blueprint("report", __name__)

@report_bp.route("/report")
def report():

    # Check if user is logged in
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    # ----------------------------
    # Total Income
    # ----------------------------
    cursor.execute(
        "SELECT SUM(amount) FROM income WHERE user_id=%s",
        (user_id,)
    )

    income = cursor.fetchone()[0]

    if income is None:
        income = 0

    # ----------------------------
    # Total Expense
    # ----------------------------
    cursor.execute(
        "SELECT SUM(amount) FROM expense WHERE user_id=%s",
        (user_id,)
    )

    expense = cursor.fetchone()[0]

    if expense is None:
        expense = 0

    # ----------------------------
    # Balance
    # ----------------------------
    balance = income - expense

    # ----------------------------
    # Highest Expense Category
    # ----------------------------
    cursor.execute("""
        SELECT category,
               SUM(amount) AS total
        FROM expense
        WHERE user_id=%s
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1
    """, (user_id,))

    result = cursor.fetchone()

    if result:
        highest_category = result[0]
        highest_amount = result[1]
    else:
        highest_category = "No Data"
        highest_amount = 0

    # ----------------------------
    # AI Suggestion
    # ----------------------------
    if expense == 0:
        suggestion = "Start tracking your expenses."

    elif expense > income:
        suggestion = "Your expenses are higher than your income. Reduce unnecessary spending."

    elif expense > income * 0.80:
        suggestion = "Your expenses are close to your income. Try to save at least 20%."

    elif balance > income * 0.30:
        suggestion = "Excellent! You are saving more than 30% of your income."

    else:
        suggestion = "Maintain your spending and continue saving regularly."

    # ----------------------------
    # Render Report Page
    # ----------------------------
    return render_template(
        "report.html",
        income=income,
        expense=expense,
        balance=balance,
        highest_category=highest_category,
        highest_amount=highest_amount,
        suggestion=suggestion
    )