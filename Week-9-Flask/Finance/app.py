import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
        user_id=session["user_id"]
    )

    cash = db.execute(
        "SELECT cash FROM users WHERE id = :user_id",
        user_id=session["user_id"]
    )[0]["cash"]

    total_value = cash

    for stock in stocks:
        quote = lookup(stock["symbol"])

        stock_value = quote["price"] * stock["total_shares"]

        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["value"] = stock_value

        total_value += stock_value

    return render_template(
        "index.html",
        stocks=stocks,
        cash=cash,
        total_value=total_value
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    if request.method == "POST":

        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Symbol is required", 400)
        symbol = symbol.upper()

        shares = request.form.get("shares")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Must be a positive number of shares")

        shares = int(shares)

        quote = lookup(symbol)
        if not quote:
            return apology("Symbol not found")

        price = quote["price"]
        total_cost = shares * price

        cash = db.execute(
            "SELECT cash FROM users WHERE id = :user_id",
            user_id=session["user_id"]
        )[0]["cash"]

        if cash < total_cost:
            return apology("You don't have enough cash")

        db.execute(
            "UPDATE users SET cash = cash - :total_cost WHERE id = :user_id",
            total_cost=total_cost,
            user_id=session["user_id"]
        )

        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
            user_id=session["user_id"],
            symbol=symbol,
            shares=shares,
            price=price
        )

        flash(f"Bought {shares} shares of {symbol}")
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():

    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = :user_id ORDER BY timestamp DESC",
        user_id=session["user_id"]
    )

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        if not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    if request.method == "POST":

        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Invalid symbol", 400)

        symbol = symbol.upper()

        quote = lookup(symbol)
        if not quote:
            return apology("Invalid symbol", 400)

        return render_template("quote.html", quote=quote)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("Username is required", 400)

        if not request.form.get("password"):
            return apology("Password is required", 400)

        if not request.form.get("confirmation"):
            return apology("You must confirm your password", 400)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match", 400)

        try:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                request.form.get("username"),
                generate_password_hash(request.form.get("password"))
            )
        except:
            return apology("Username already exists", 400)

        rows = db.execute(
            "SELECT id FROM users WHERE username = ?",
            request.form.get("username")
        )

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0",
        user_id=session["user_id"]
    )

    if request.method == "POST":

        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Symbol is required")

        symbol = symbol.upper()

        shares = request.form.get("shares")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("Must be a positive number of shares")

        shares = int(shares)

        for stock in stocks:
            if stock["symbol"] == symbol:

                if stock["total_shares"] < shares:
                    return apology("You don't have enough shares")

                quote = lookup(symbol)
                if not quote:
                    return apology("Symbol not found")

                price = quote["price"]
                total_sale = shares * price

                db.execute(
                    "UPDATE users SET cash = cash + :total_sale WHERE id = :user_id",
                    total_sale=total_sale,
                    user_id=session["user_id"]
                )

                db.execute(
                    "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                    user_id=session["user_id"],
                    symbol=symbol,
                    shares=-shares,
                    price=price
                )

                flash(f"Sold {shares} shares of {symbol}")
                return redirect("/")

        return apology("Symbol not found")

    return render_template("sell.html", stocks=stocks)
