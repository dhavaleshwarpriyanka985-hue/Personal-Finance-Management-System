from flask import request, redirect, render_template, session
from app import app
from database.db import db, cursor


# ==========================
# ADD INCOME
# ==========================

@app.route('/add_income', methods=['POST'])
def add_income():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    title = request.form["title"]
    amount = request.form["amount"]
    transaction_date = request.form["transaction_date"]
    category = request.form["category"]

    sql = """
    INSERT INTO income
    (user_id, title, amount, transaction_date, category)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        user_id,
        title,
        amount,
        transaction_date,
        category
    )

    cursor.execute(sql, values)
    db.commit()

    return redirect("/dashboard")


# ==========================
# ADD EXPENSE
# ==========================

@app.route('/add_expense', methods=['POST'])
def add_expense():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    title = request.form["title"]
    amount = request.form["amount"]
    transaction_date = request.form["transaction_date"]
    category = request.form["category"]

    sql = """
    INSERT INTO expense
    (user_id, title, amount, transaction_date, category)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        user_id,
        title,
        amount,
        transaction_date,
        category
    )

    cursor.execute(sql, values)
    db.commit()

    return redirect("/dashboard")


# ==========================
# DELETE INCOME
# ==========================

@app.route('/delete_income/<int:id>')
def delete_income(id):

    cursor.execute(
        "DELETE FROM income WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect("/dashboard")


# ==========================
# DELETE EXPENSE
# ==========================

@app.route('/delete_expense/<int:id>')
def delete_expense(id):

    cursor.execute(
        "DELETE FROM expense WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect("/dashboard")


# ==========================
# EDIT INCOME
# ==========================

@app.route('/edit_income/<int:id>', methods=['GET', 'POST'])
def edit_income(id):

    if request.method == "POST":

        title = request.form["title"]
        amount = request.form["amount"]
        transaction_date = request.form["transaction_date"]
        category = request.form["category"]

        cursor.execute("""
        UPDATE income
        SET title=%s,
            amount=%s,
            transaction_date=%s,
            category=%s
        WHERE id=%s
        """,
        (
            title,
            amount,
            transaction_date,
            category,
            id
        ))

        db.commit()

        return redirect("/dashboard")

    cursor.execute(
        "SELECT * FROM income WHERE id=%s",
        (id,)
    )

    income = cursor.fetchone()

    return render_template(
    "edit_income.html",
    income=income
)

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    # Total Income
    cursor.execute(
        "SELECT SUM(amount) FROM income WHERE user_id=%s",
        (user_id,)
    )
    total_income = cursor.fetchone()[0] or 0

    # Total Expense
    cursor.execute(
        "SELECT SUM(amount) FROM expense WHERE user_id=%s",
        (user_id,)
    )
    total_expense = cursor.fetchone()[0] or 0

    balance = total_income - total_expense

    # Income History
    cursor.execute("""
        SELECT id, title, amount, transaction_date, category
        FROM income
        WHERE user_id=%s
    """, (user_id,))
    income_data = cursor.fetchall()

    # Expense History
    cursor.execute("""
        SELECT id, title, amount, transaction_date, category
        FROM expense
        WHERE user_id=%s
    """, (user_id,))
    expense_data = cursor.fetchall()

    cursor.execute(
    "SELECT monthly_budget FROM budget WHERE user_id=%s ORDER BY id DESC LIMIT 1",
    (user_id,)
)

    budget = cursor.fetchone()

    if budget:
        budget = budget[0]
    else:
        budget = 0

    remaining_budget = budget - total_expense

    return render_template(
    "dashboard.html",
    income=total_income,
    expense=total_expense,
    balance=balance,
    budget=budget,
    remaining_budget=remaining_budget,
    income_data=income_data,
    expense_data=expense_data
)

   