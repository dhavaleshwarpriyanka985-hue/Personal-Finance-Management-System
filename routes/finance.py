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

    cursor.execute("""
        INSERT INTO income
        (user_id, title, amount, transaction_date, category)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        title,
        amount,
        transaction_date,
        category
    ))

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

    cursor.execute("""
        INSERT INTO expenses
        (user_id, title, amount, transaction_date, category)
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        title,
        amount,
        transaction_date,
        category
    ))

    db.commit()

    return redirect("/dashboard")


# ==========================
# DELETE INCOME
# ==========================

@app.route('/delete_income/<int:id>')
def delete_income(id):

    cursor.execute(
        "DELETE FROM income WHERE id=?",
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
        "DELETE FROM expenses WHERE id=?",
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
            SET title=?,
                amount=?,
                transaction_date=?,
                category=?
            WHERE id=?
        """, (
            title,
            amount,
            transaction_date,
            category,
            id
        ))

        db.commit()

        return redirect("/dashboard")

    cursor.execute(
        "SELECT * FROM income WHERE id=?",
        (id,)
    )

    income = cursor.fetchone()

    return render_template(
        "edit_income.html",
        income=income
    )


# ==========================
# EDIT EXPENSE
# ==========================

@app.route('/edit_expense/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):

    if request.method == "POST":

        title = request.form["title"]
        amount = request.form["amount"]
        transaction_date = request.form["transaction_date"]
        category = request.form["category"]

        cursor.execute("""
            UPDATE expenses
            SET title=?,
                amount=?,
                transaction_date=?,
                category=?
            WHERE id=?
        """, (
            title,
            amount,
            transaction_date,
            category,
            id
        ))

        db.commit()

        return redirect("/dashboard")

    cursor.execute(
        "SELECT * FROM expenses WHERE id=?",
        (id,)
    )

    expense = cursor.fetchone()

    return render_template(
        "edit_expense.html",
        expense=expense
    )
# ==========================
# DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    # Total Income
    cursor.execute(
        "SELECT SUM(amount) FROM income WHERE user_id=?",
        (user_id,)
    )

    total_income = cursor.fetchone()[0] or 0

    # Total Expense
    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE user_id=?",
        (user_id,)
    )

    total_expense = cursor.fetchone()[0] or 0

    balance = total_income - total_expense

    # Income History
    cursor.execute("""
        SELECT id, title, amount, transaction_date, category
        FROM income
        WHERE user_id=?
    """, (user_id,))

    income_data = cursor.fetchall()

    # Expense History
    cursor.execute("""
        SELECT id, title, amount, transaction_date, category
        FROM expenses
        WHERE user_id=?
    """, (user_id,))

    expense_data = cursor.fetchall()

    # Budget
    cursor.execute(
        """
        SELECT monthly_budget
        FROM budget
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
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


# ==========================
# SET BUDGET
# ==========================

@app.route('/set_budget', methods=['POST'])
def set_budget():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    budget = request.form["budget"]

    cursor.execute(
        """
        INSERT INTO budget(user_id, monthly_budget)
        VALUES(?, ?)
        """,
        (user_id, budget)
    )

    db.commit()

    return redirect("/dashboard")


# ==========================
# SEARCH
# ==========================

@app.route('/search', methods=['GET'])
def search():

    keyword = request.args.get("keyword", "")

    search_keyword = "%" + keyword + "%"

    cursor.execute(
        """
        SELECT title, amount, transaction_date, category
        FROM income
        WHERE title LIKE ?
        """,
        (search_keyword,)
    )

    income_results = cursor.fetchall()

    cursor.execute(
        """
        SELECT title, amount, transaction_date, category
        FROM expenses
        WHERE title LIKE ?
        """,
        (search_keyword,)
    )

    expense_results = cursor.fetchall()

    return render_template(
        "search.html",
        income_results=income_results,
        expense_results=expense_results,
        keyword=keyword
    )


# ==========================
# PREDICTION
# ==========================

@app.route('/prediction')
def prediction():

    cursor.execute(
        "SELECT SUM(amount) FROM expenses"
    )

    expense = cursor.fetchone()[0] or 0

    expense = float(expense)

    predicted_expense = round(expense * 1.10, 2)

    return render_template(
        "prediction.html",
        prediction=predicted_expense
    )