from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from collections import defaultdict

app = Flask(__name__)

# -------------------
# Configuration
# -------------------
app.config["SECRET_KEY"] = "dev-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expense.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

# -------------------
# Database Models
# -------------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------
# Routes
# -------------------

@app.route("/")
@login_required
def dashboard():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()

    total = sum(exp.amount for exp in expenses)

    category_data = defaultdict(float)
    for exp in expenses:
        category_data[exp.category] += exp.amount

    return render_template(
        "dashboard.html",
        user=current_user,
        expenses=expenses,
        total=total,
        categories=list(category_data.keys()),
        values=list(category_data.values()),
    )

@app.route("/add_expense", methods=["POST"])
@login_required
def add_expense():
    new_expense = Expense(
        amount=float(request.form["amount"]),
        category=request.form["category"],
        description=request.form["description"],
        user_id=current_user.id,
    )
    db.session.add(new_expense)
    db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/delete_all", methods=["POST"])
@login_required
def delete_all():
    Expense.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        hashed = generate_password_hash(request.form["password"])
        user = User(username=request.form["username"], password=hashed)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("dashboard"))
        flash("Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# -------------------
# Main
# -------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
