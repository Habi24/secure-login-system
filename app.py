from flask import Flask, render_template, request, session, redirect
import sqlite3
import bcrypt
import re

app = Flask(__name__)
app.secret_key = "secure_login_project"


@app.route("/")
def home():
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]

        # Input Validation

        if len(username) < 3:
            return "Username must contain at least 3 characters"

        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return "Username can contain only letters, numbers and underscore"

        if len(password) < 8:
            return "Password must be at least 8 characters long"

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users(username, password) VALUES (?, ?)",
                (username, hashed_password)
            )

            conn.commit()

            return "User Registered Successfully!"

        except sqlite3.IntegrityError:
            return "Username Already Exists!"

        finally:
            conn.close()

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]

        if not username or not password:
            return "All fields are required"

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            stored_password = user[2]

            # Convert string to bytes if needed
            if isinstance(stored_password, str):
                stored_password = stored_password.encode("utf-8")

            if bcrypt.checkpw(
                password.encode("utf-8"),
                stored_password
            ):

                session["user"] = username

                return redirect("/dashboard")

        return "Invalid Username or Password"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=session["user"]
    )


@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)

