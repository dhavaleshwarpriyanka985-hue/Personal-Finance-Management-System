from flask import render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from database.db import db, cursor


# -------------------- REGISTER --------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Check if email already exists
        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )

        user = cursor.fetchone()

        if user:
            return "Email already exists!"

        # Hash password
        hashed_password = generate_password_hash(password)

        # Insert new user
        cursor.execute(
            """
            INSERT INTO users(name, email, password)
            VALUES(?, ?, ?)
            """,
            (name, email, hashed_password)
        )

        db.commit()

        return redirect("/login")

    return render_template("register.html")


# -------------------- LOGIN --------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )

        user = cursor.fetchone()

        if user:

            # Verify password
            if check_password_hash(user["password"], password):

                session["user_id"] = user["id"]
                session["user_name"] = user["name"]
                session["email"] = user["email"]

                return redirect("/dashboard")

            else:
                return "Incorrect Password"

        else:
            return "User Not Found"

    return render_template("login.html")


# -------------------- LOGOUT --------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")