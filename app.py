#=============imports of various files, zingine za ku install kama vile Flask

import sqlite3
from functools import wraps


from flask import (Flask, render_template, request, redirect,
                   session, url_for, flash)
from werkzeug.security import check_password_hash, generate_password_hash #==security==

from database import (init_databases, insert_customers, get_customer_by_email, get_all_customers, get_stats,
                      get_staff_by_membership)
from automation import analyze_message, reprocess_all_customers

from datetime import timedelta


#============the whole flask controlled by "app"================
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False #==not in session all time
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=1) #=====Baada  ya dakika 1 it logout(session over
app.secret_key = "my_app_secret_key"

init_databases()


#======================access control==================
def staff_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get("role") != "staff":
            flash("Staff login required.")
            return redirect(url_for("staff_login"))
        return view(*args, **kwargs)
    return wrapped


def customer_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get("role") != "customer":
            flash("Please log in first.")
            return redirect(url_for("customer_login"))
        return view(*args, **kwargs)
    return wrapped


#===================The first page to all(Home page)===========
@app.route("/")
def home():
    return render_template("index.html")

#===================Enable customer to put their information into database==============
@app.route("/customer_registration", methods=["GET", "POST"])
def customer_registration():
    if request.method == "POST":
        message = request.form["message"]
        category, priority = analyze_message(message)
        try:
            insert_customers(
                request.form["first_name"].strip(),
                request.form["middle_name"].strip(),
                request.form["last_name"].strip(),
                request.form["email"].strip().lower(),
                generate_password_hash(request.form["password"]),
                message,
                category,
                priority,
            )
        except sqlite3.IntegrityError:
            flash("That email is already registered.")
            return render_template("customer_registration.html")
        flash("Registration completed. Please log in.")
        return redirect(url_for("customer_login"))
    return render_template("customer_registration.html")



#====================customer login, inatumia customer_id ====================
@app.route("/customer_login", methods=["GET", "POST"])
def customer_login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        customer = get_customer_by_email(email)
        if customer and check_password_hash(customer["hash_password"],
                                            request.form["password"]):
            session.clear()
            session["role"] = "customer"
            session["customer_id"] = customer["id"]
            return redirect(url_for("customer_dashboard"))

        flash("Invalid email or password.")
    return render_template("customer_login.html")


#==============function ya staff login, inatumia staff_id================
@app.route("/staff_login", methods=["GET", "POST"])
def staff_login():
    if request.method == "POST":
        staff = get_staff_by_membership(request.form["membership_number"].strip())
        if staff and check_password_hash(staff["hash_password"],
                                         request.form["password"]):
            session.clear()
            session["role"] = "staff"
            session["staff_id"] = staff["id"]
            return redirect(url_for("admin_dashboard"))
        flash("Invalid membership number or password.")
    return render_template("staff_login.html")


#====================Admini pekee ataona users in hi or has dashboard while logged in================
@app.route("/admin_dashboard")
@staff_required
def admin_dashboard():
    total, pending, high = get_stats()
    return render_template("admin_dashboard.html",
                           customers=get_all_customers(),
                           total_customers=total,
                           pending_customers=pending,
                           high_priority=high)


@app.route("/customer_dashboard")
def customer_dashboard():
    if "customer_id" in session:
        return render_template("customer_dashboard.html")

    return redirect(url_for("customer_login"))


@app.route("/reprocess", methods=["POST"])
@staff_required
def reprocess():
    reprocess_all_customers()
    flash("All customers reprocessed.")
    return redirect(url_for("admin_dashboard"))


# ---------- It logout both staff and customer ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)