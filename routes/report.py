from flask import Blueprint, render_template
from database.db import cursor

report_bp = Blueprint('report', __name__)


@report_bp.route('/monthly_report')
def report():

    # Total Income
    cursor.execute(
        "SELECT SUM(amount) FROM income"
    )

    income = cursor.fetchone()[0] or 0

    # Total Expense
    cursor.execute(
        "SELECT SUM(amount) FROM expenses"
    )

    expense = cursor.fetchone()[0] or 0

    # Balance
    balance = income - expense

    # Highest Expense Category
    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    if result:
        highest_category = result[0]
        highest_amount = result[1]
    else:
        highest_category = "No Data"
        highest_amount = 0

    return render_template(
        "report.html",
        income=income,
        expense=expense,
        balance=balance,
        highest_category=highest_category,
        highest_amount=highest_amount
    )