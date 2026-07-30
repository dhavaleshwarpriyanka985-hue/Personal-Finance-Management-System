from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "my_secret_key"

# ---------------- DATABASE CONNECTION ----------------

db = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="MySQL@123",
    database="finance_db"
)

cursor = db.cursor()

# ---------------- HOME ----------------

@app.route('/')
def home():
    return render_template("index.html")


# ---------------- REGISTER ----------------

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        sql = "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)"
        cursor.execute(sql, (name, email, password))
        db.commit()

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cursor.fetchone()

        if user:

            session["user_id"] = user[0]
            session["email"] = user[2]

            return redirect("/dashboard")

        else:
            return "Invalid Email or Password"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------

@app.route('/dashboard')
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    # Total Income
    cursor.execute(
        "SELECT COALESCE(SUM(amount),0) FROM income WHERE user_id=%s",
        (user_id,)
    )
    total_income = cursor.fetchone()[0]

    # Total Expense
    cursor.execute(
        "SELECT COALESCE(SUM(amount),0) FROM expense WHERE user_id=%s",
        (user_id,)
    )
    total_expense = cursor.fetchone()[0]

    # Budget
    cursor.execute(
        """
        SELECT monthly_budget
        FROM budget
        WHERE user_id=%s
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

    balance = total_income - total_expense
    remaining_budget = budget - total_expense

    # Income History
    cursor.execute(
        """
        SELECT id,title,amount,transaction_date,category
        FROM income
        WHERE user_id=%s
        ORDER BY transaction_date DESC
        """,
        (user_id,)
    )

    income_data = cursor.fetchall()

    # Expense History
    cursor.execute(
        """
        SELECT id,title,amount,transaction_date,category
        FROM expense
        WHERE user_id=%s
        ORDER BY transaction_date DESC
        """,
        (user_id,)
    )

    expense_data = cursor.fetchall()

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


# ---------------- ADD INCOME ----------------

@app.route('/add_income', methods=['POST'])
def add_income():

    user_id = session["user_id"]

    title = request.form["title"]
    amount = request.form["amount"]
    transaction_date = request.form["transaction_date"]
    category = request.form["category"]

    cursor.execute(
        """
        INSERT INTO income
        (user_id,title,amount,transaction_date,category)
        VALUES(%s,%s,%s,%s,%s)
        """,
        (user_id, title, amount, transaction_date, category)
    )

    db.commit()

    return redirect("/dashboard")


# ---------------- ADD EXPENSE ----------------

@app.route('/add_expense', methods=['POST'])
def add_expense():

    user_id = session["user_id"]

    title = request.form["title"]
    amount = request.form["amount"]
    transaction_date = request.form["transaction_date"]
    category = request.form["category"]

    cursor.execute(
        """
        INSERT INTO expense
        (user_id,title,amount,transaction_date,category)
        VALUES(%s,%s,%s,%s,%s)
        """,
        (user_id, title, amount, transaction_date, category)
    )

    db.commit()

    return redirect("/dashboard")


# ---------------- DELETE INCOME ----------------

@app.route('/delete_income/<int:id>')
def delete_income(id):

    user_id = session["user_id"]

    cursor.execute(
        "DELETE FROM income WHERE id=%s AND user_id=%s",
        (id, user_id)
    )

    db.commit()

    return redirect("/dashboard")


# ---------------- DELETE EXPENSE ----------------

@app.route('/delete_expense/<int:id>')
def delete_expense(id):

    user_id = session["user_id"]

    cursor.execute(
        "DELETE FROM expense WHERE id=%s AND user_id=%s",
        (id, user_id)
    )

    db.commit()

    return redirect("/dashboard")


# ---------------- SET BUDGET ----------------

@app.route('/set_budget', methods=['POST'])
def set_budget():

    user_id = session["user_id"]
    budget = request.form["budget"]

    cursor.execute(
        """
        INSERT INTO budget(user_id, monthly_budget)
        VALUES(%s,%s)
        """,
        (user_id, budget)
    )

    db.commit()

    return redirect("/dashboard")


# ---------------- LOGOUT ----------------

@app.route('/logout')
def logout():

    session.clear()

    return redirect("/")

#---------------search--------------
@app.route('/search')
def search():

    keyword = request.args.get("keyword")

    cursor.execute(
        "SELECT title, amount, transaction_date, category FROM income WHERE title LIKE %s",
        ("%" + keyword + "%",)
    )
    income_results = cursor.fetchall()

    cursor.execute(
        "SELECT title, amount, transaction_date, category FROM expense WHERE title LIKE %s",
        ("%" + keyword + "%",)
    )
    expense_results = cursor.fetchall()

    return render_template(
        "search.html",
        income_results=income_results,
        expense_results=expense_results,
        keyword=keyword
    )


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)