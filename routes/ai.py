from flask import render_template, request, session, redirect
from app import app
from database.db import cursor


# ===========================
# AI EXPENSE ANALYSIS
# ===========================

@app.route("/ai_analysis")
def ai_analysis():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE user_id=?
        GROUP BY category
    """, (user_id,))

    data = cursor.fetchall()

    if not data:
        return render_template(
            "ai_analysis.html",
            message="No expense data available."
        )

    highest = max(data, key=lambda x: x[1])

    message = f"""
You spend the most on {highest[0]} (₹{highest[1]}).

Suggestion:
Try reducing your spending in this category.
"""

    return render_template(
        "ai_analysis.html",
        message=message
    )


# ===========================
# AI CHATBOT
# ===========================

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    answer = ""

    if request.method == "POST":

        question = request.form["question"].lower()

        # -----------------------------
        # Total Income
        # -----------------------------

        if "income" in question:

            cursor.execute("""
                SELECT SUM(amount)
                FROM income
                WHERE user_id=?
            """, (user_id,))

            income = cursor.fetchone()[0]

            if income is None:
                income = 0

            answer = f"Your total income is ₹{income}"

        # -----------------------------
        # Total Expense
        # -----------------------------

        elif "expense" in question:

            cursor.execute("""
                SELECT SUM(amount)
                FROM expenses
                WHERE user_id=?
            """, (user_id,))

            expense = cursor.fetchone()[0]

            if expense is None:
                expense = 0

            answer = f"Your total expense is ₹{expense}"

        # -----------------------------
        # Balance
        # -----------------------------

        elif "balance" in question:

            cursor.execute("""
                SELECT SUM(amount)
                FROM income
                WHERE user_id=?
            """, (user_id,))

            income = cursor.fetchone()[0]

            if income is None:
                income = 0

            cursor.execute("""
                SELECT SUM(amount)
                FROM expenses
                WHERE user_id=?
            """, (user_id,))

            expense = cursor.fetchone()[0]

            if expense is None:
                expense = 0

            balance = income - expense

            answer = f"Your current balance is ₹{balance}"

        # -----------------------------
        # Saving Tips
        # -----------------------------

        elif "save" in question or "saving" in question:

            answer = """
Try these tips to save more money:

• Follow the 50-30-20 budgeting rule.
• Reduce unnecessary shopping.
• Track daily expenses.
• Set a monthly budget.
• Save at least 20% of your income.
"""

        # -----------------------------
        # Highest Expense Category
        # -----------------------------

        elif "highest" in question or "category" in question:

            cursor.execute("""
                SELECT category, SUM(amount)
                FROM expenses
                WHERE user_id=?
                GROUP BY category
                ORDER BY SUM(amount) DESC
                LIMIT 1
            """, (user_id,))

            result = cursor.fetchone()

            if result:
                answer = f"You spend the most on {result[0]} (₹{result[1]})."
            else:
                answer = "No expense records found."

        # -----------------------------
        # Unknown Question
        # -----------------------------

        else:

            answer = """
Sorry, I don't understand that question.

Try asking:

• What is my income?
• What is my expense?
• What is my balance?
• Give me saving tips.
• Which category has the highest expense?
"""

    return render_template(
        "chatbot.html",
        answer=answer
    )